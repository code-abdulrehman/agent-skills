#!/usr/bin/env node
// Trusted local QA actions only. Use a separate temporary Chrome profile/port per role.
// Usage: node local_cdp_qa.mjs <port> <actions.json> --dedicated-profile
import fs from 'node:fs/promises';

const [portArg, actionsPath, dedicatedFlag, ...extra] = process.argv.slice(2);
const port = Number(portArg);
if (!Number.isInteger(port) || port < 1 || port > 65535 || !actionsPath ||
    dedicatedFlag !== '--dedicated-profile' || extra.length) {
  console.error('Usage: node local_cdp_qa.mjs <local-CDP-port> <actions.json> --dedicated-profile');
  process.exit(1);
}

class QAError extends Error {}

const origin = `http://127.0.0.1:${port}`;
const deadline = Date.now() + 120000;
let targetId;
let ws;
let nextId = 1;
let actionIndex = -1;
let basicAuth;
let fetchEnabled = false;
let fetchFailed = false;
let mainFrameId;
let openDialogType;
const authAttempts = new Set();
const pending = new Map();
const diagnostics = [];
const loaded = new Set();
const requestPaths = new Map();
// Only known static route words leave the browser; account IDs, tokens, queries,
// fragments, free text, input values and DOM IDs/names never enter the report.
const routeWords = new Set([
  'a', 'o', 'users', 'log_in', 'log_out', 'register', 'reset_password', 'settings',
  'admin', 'teams', 'tasks', 'projects', 'departments', 'reports', 'members',
  'new', 'edit', 'list', 'dashboard', 'profile', 'account', 'organizations', 'invite',
  'accounts', 'home', 'welcome', 'onboarding', 'create_organization', 'verify_email',
  'setting', 'restricted'
]);
function safePath(raw) {
  try {
    const url = new URL(raw, 'http://localhost');
    const parts = url.pathname.split('/').filter(Boolean);
    return '/' + parts.map((part, index) => {
      // Dynamic account/org and credential route values stay hidden even when
      // they happen to equal a known static route word.
      if (index > 0 && ['a', 'o', 'reset_password', 'verify_email'].includes(parts[index - 1])) {
        return '[redacted]';
      }
      return routeWords.has(part) ? part : '[redacted]';
    }).join('/');
  } catch { return '[redacted]'; }
}
function record(item) {
  if (diagnostics.length < 200) diagnostics.push(item);
}
function rejectPending() {
  for (const {reject, timer} of pending.values()) {
    clearTimeout(timer);
    reject(new QAError('Browser connection closed'));
  }
  pending.clear();
}
async function localFetch(path, options = {}) {
  return await fetch(origin + path, {...options, signal: AbortSignal.timeout(5000)});
}
async function send(method, params = {}) {
  if (!ws || ws.readyState !== WebSocket.OPEN) throw new QAError('Browser connection unavailable');
  if (fetchFailed && method !== 'Fetch.disable') throw new QAError('Browser authentication interception failed');
  const remaining = deadline - Date.now();
  if (remaining <= 0) throw new QAError('QA run time limit reached');
  const id = nextId++;
  return await new Promise((resolve, reject) => {
    const timer = setTimeout(() => {
      pending.delete(id);
      reject(new QAError(`Browser operation timed out: ${method}`));
    }, Math.min(10000, remaining));
    pending.set(id, {resolve, reject, timer});
    try { ws.send(JSON.stringify({id, method, params})); }
    catch {
      clearTimeout(timer);
      pending.delete(id);
      reject(new QAError('Browser send failed'));
    }
  });
}
async function evaluate(expression) {
  const result = await send('Runtime.evaluate', {expression, returnByValue: true, awaitPromise: true});
  if (result.exceptionDetails) throw new QAError('Browser expression failed');
  return result.result?.value;
}
async function waitFor(check, timeoutMs = 12000) {
  if (!Number.isFinite(timeoutMs) || timeoutMs < 1 || timeoutMs > 20000) {
    throw new QAError('Wait duration must be between 1 and 20000 ms');
  }
  const end = Math.min(Date.now() + timeoutMs, deadline);
  while (Date.now() < end) {
    try { if (await check()) return; }
    catch { if (!ws || ws.readyState !== WebSocket.OPEN) throw new QAError('Browser connection closed'); }
    await new Promise(resolve => setTimeout(resolve, 100));
  }
  throw new QAError('Browser wait timed out');
}
function localURL(raw) {
  const url = new URL(raw);
  if (!['http:', 'https:'].includes(url.protocol) ||
      !['localhost', '127.0.0.1'].includes(url.hostname) || url.username || url.password) {
    throw new QAError('Navigation requires a local HTTP URL without credentials');
  }
  return url;
}
function queryParams(query) {
  if (query === undefined) return '';
  if (query === null || typeof query !== 'object' || Object.getPrototypeOf(query) !== Object.prototype) {
    throw new QAError('Navigation query must be a plain object');
  }
  const params = new URLSearchParams();
  for (const [key, value] of Object.entries(query)) {
    if (!(value === null || typeof value === 'string' || typeof value === 'boolean' ||
          (typeof value === 'number' && Number.isFinite(value)))) {
      throw new QAError('Navigation query values must be strings or finite JSON primitives');
    }
    params.append(key, String(value));
  }
  return params.toString();
}
async function handleFetchEvent(msg) {
  if (msg.method === 'Fetch.requestPaused') {
    // Do not add Authorization headers. Unrelated requests continue unchanged.
    await send('Fetch.continueRequest', {requestId: msg.params.requestId});
  } else if (msg.method === 'Fetch.authRequired') {
    const {requestId, request, authChallenge} = msg.params;
    let approved = false;
    try {
      approved = Boolean(basicAuth) && authChallenge?.source === 'Server' &&
        authChallenge.scheme?.toLowerCase() === 'basic' &&
        new URL(request.url).origin === basicAuth.origin &&
        new URL(authChallenge.origin).origin === basicAuth.origin &&
        !authAttempts.has(requestId);
    } catch { /* malformed or unapproved challenge: cancel it */ }
    if (approved) authAttempts.add(requestId);
    const authChallengeResponse = approved ? {
      response: 'ProvideCredentials', username: basicAuth.username, password: basicAuth.password
    } : {response: 'CancelAuth'};
    await send('Fetch.continueWithAuth', {requestId, authChallengeResponse});
    record({kind: approved ? 'http-basic-provided' : 'http-auth-canceled'});
  }
}
async function navigate(url) {
  loaded.clear();
  const result = await send('Page.navigate', {url: localURL(url).toString()});
  if (result.errorText || result.isDownload) throw new QAError('Browser navigation failed');
  // A previous document may already be complete. Wait for the new loader's load
  // event before inspecting document.readyState. Events can precede the response.
  if (result.loaderId) await waitFor(async () => loaded.has(result.loaderId), 20000);
  await waitFor(() => evaluate('document.readyState === "complete"'));
}

try {
  const actions = JSON.parse(await fs.readFile(actionsPath, 'utf8'));
  if (!Array.isArray(actions) || actions.length > 200) throw new QAError('Expected at most 200 actions');
  const created = await localFetch('/json/new?about:blank', {method: 'PUT'});
  if (!created.ok) throw new QAError('Cannot create local Chrome target');
  const target = await created.json();
  if (typeof target.id !== 'string' || !/^[a-z0-9-]+$/i.test(target.id)) {
    throw new QAError('Invalid browser target ID');
  }
  targetId = target.id;
  const endpoint = new URL(target.webSocketDebuggerUrl);
  if (endpoint.protocol !== 'ws:' || !['localhost', '127.0.0.1'].includes(endpoint.hostname) ||
      endpoint.port !== String(port) || endpoint.username || endpoint.password) {
    throw new QAError('Browser returned a nonlocal debugger endpoint');
  }
  ws = new WebSocket(endpoint);
  ws.addEventListener('close', rejectPending);
  ws.addEventListener('error', rejectPending);
  ws.addEventListener('message', event => {
    let msg;
    try { msg = JSON.parse(event.data); } catch { return; }
    if (msg.id && pending.has(msg.id)) {
      const {resolve, reject, timer} = pending.get(msg.id);
      clearTimeout(timer);
      pending.delete(msg.id);
      msg.error ? reject(new QAError('Browser operation rejected')) : resolve(msg.result);
    }
    if (msg.method === 'Page.lifecycleEvent' && msg.params?.name === 'load') {
      loaded.add(msg.params.loaderId);
    }
    if (msg.method === 'Page.frameNavigated' && !msg.params?.frame?.parentId) {
      mainFrameId = msg.params.frame.id;
      record({kind: 'main-frame-navigation', path: safePath(msg.params.frame.url)});
    }
    if (msg.method === 'Page.navigatedWithinDocument' && msg.params?.frameId === mainFrameId) {
      record({kind: 'main-frame-navigation', path: safePath(msg.params.url)});
    }
    if (msg.method === 'Page.javascriptDialogOpening') {
      const type = msg.params?.type;
      openDialogType = ['alert', 'confirm', 'prompt', 'beforeunload'].includes(type) ? type : 'other';
      record({kind: 'javascript-dialog-opened', type: openDialogType});
    }
    if (msg.method === 'Page.javascriptDialogClosed') {
      openDialogType = undefined;
      record({kind: 'javascript-dialog-closed'});
    }
    if (msg.method === 'Runtime.exceptionThrown') record({kind: 'page-exception'});
    if (msg.method === 'Runtime.consoleAPICalled' && msg.params?.type === 'error') {
      record({kind: 'console-error'});
    }
    if (msg.method === 'Network.requestWillBeSent') {
      if (requestPaths.size >= 1000) requestPaths.clear();
      requestPaths.set(msg.params.requestId, safePath(msg.params.request?.url));
      if (msg.params.type === 'Document' && msg.params.frameId === mainFrameId) {
        record({kind: 'document-request', path: safePath(msg.params.request?.url)});
        if (msg.params.redirectResponse) {
          record({kind: 'document-redirect', status: msg.params.redirectResponse.status,
            from: safePath(msg.params.redirectResponse.url), to: safePath(msg.params.request?.url)});
        }
      }
    }
    if (msg.method === 'Network.responseReceived' && msg.params?.type === 'Document' &&
        msg.params.frameId === mainFrameId) {
      record({kind: 'document-response', status: msg.params.response.status,
        path: safePath(msg.params.response.url)});
    }
    if (msg.method === 'Network.responseReceived' && msg.params?.response?.status >= 400) {
      record({kind: 'http-error', status: msg.params.response.status,
        path: safePath(msg.params.response.url)});
    }
    if (msg.method === 'Network.loadingFailed') {
      record({kind: 'network-failure', canceled: Boolean(msg.params?.canceled),
        path: requestPaths.get(msg.params?.requestId) || '[redacted]'});
    }
    if (msg.method === 'Fetch.requestPaused' || msg.method === 'Fetch.authRequired') {
      void handleFetchEvent(msg).catch(() => {
        fetchFailed = true;
        record({kind: 'auth-interception-failure'});
      });
    }
  });
  await new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new QAError('Browser connection timed out')), 5000);
    const done = fn => () => { clearTimeout(timer); fn(); };
    ws.addEventListener('open', done(resolve), {once: true});
    ws.addEventListener('error', done(() => reject(new QAError('Browser connection failed'))), {once: true});
  });
  await send('Page.enable');
  mainFrameId = (await send('Page.getFrameTree')).frameTree.frame.id;
  await send('Page.bringToFront');
  await send('Page.setLifecycleEventsEnabled', {enabled: true});
  await send('Runtime.enable');
  await send('Network.enable');

  for (const [index, action] of actions.entries()) {
    actionIndex = index;
    if (!action || typeof action !== 'object') throw new QAError('Invalid action');
    const op = action.op;
    if (op === 'httpBasic') {
      if (fetchEnabled) throw new QAError('Configure HTTP Basic Auth only once per run');
      const url = localURL(action.origin);
      if (url.pathname !== '/' || url.search || url.hash) {
        throw new QAError('HTTP Basic Auth requires an origin without a path or query');
      }
      if (![action.usernameEnv, action.passwordEnv].every(name =>
        typeof name === 'string' && /^[A-Za-z_][A-Za-z0-9_]*$/.test(name))) {
        throw new QAError('HTTP Basic Auth requires credential environment variable names');
      }
      const username = process.env[action.usernameEnv];
      const password = process.env[action.passwordEnv];
      if (!username || !password) throw new QAError('HTTP Basic Auth credential environment variable is missing');
      basicAuth = {origin: url.origin, username, password};
      fetchEnabled = true;
      await send('Fetch.enable', {handleAuthRequests: true,
        patterns: [{urlPattern: '*', requestStage: 'Request'}]});
    } else if (op === 'navigate') {
      await navigate(action.url);
    } else if (op === 'navigateCurrentOrg') {
      if (typeof action.suffix !== 'string' || !/^\/[a-z0-9/_-]*$/i.test(action.suffix)) {
        throw new QAError('Invalid organization route suffix');
      }
      const search = queryParams(action.query);
      const url = localURL(await evaluate('location.href'));
      const match = url.pathname.match(/^\/a\/[^/]+\/o\/\d+(?=\/|$)/);
      if (!match) throw new QAError('Current tab has no organization context');
      url.pathname = match[0] + action.suffix;
      url.search = search;
      url.hash = '';
      await navigate(url);
    } else if (op === 'waitFor') {
      await waitFor(() => evaluate(`!!document.querySelector(${JSON.stringify(action.selector)})`), action.timeoutMs ?? 12000);
    } else if (op === 'fill') {
      const value = action.valueEnv ? process.env[action.valueEnv] : action.value;
      if (typeof value !== 'string') throw new QAError('Missing fill value or environment variable');
      const filled = await evaluate(`(() => {
        const el = document.querySelector(${JSON.stringify(action.selector)});
        if (!el || (el.type === 'password' && !${Boolean(action.valueEnv)})) return false;
        el.focus(); el.value = ${JSON.stringify(value)};
        el.dispatchEvent(new Event('input', {bubbles:true}));
        el.dispatchEvent(new Event('change', {bubbles:true})); return true;
      })()`);
      if (!filled) throw new QAError('Fill target missing or password requires valueEnv');
    } else if (op === 'click') {
      if (!await evaluate(`(() => {
        const el = document.querySelector(${JSON.stringify(action.selector)});
        if (!el || el.disabled) return false;
        ${action.defer === true ? 'setTimeout(() => el.click(), 0);' : 'el.click();'} return true;
      })()`)) throw new QAError('Click target unavailable');
    } else if (op === 'handleDialog') {
      if (typeof action.accept !== 'boolean' ||
          (action.ifPresent !== undefined && typeof action.ifPresent !== 'boolean')) {
        throw new QAError('Dialog handling requires an explicit accept boolean');
      }
      if (!openDialogType && action.ifPresent === true) continue;
      await waitFor(async () => Boolean(openDialogType), action.timeoutMs ?? 12000);
      await send('Page.handleJavaScriptDialog', {accept: action.accept});
    } else if (op === 'key') {
      const keyCodes = {Tab: 9, Escape: 27, Enter: 13, ArrowDown: 40, ArrowUp: 38};
      if (!Object.hasOwn(keyCodes, action.key)) throw new QAError('Unsupported keyboard key');
      const key = {key: action.key, code: action.key, windowsVirtualKeyCode: keyCodes[action.key],
        nativeVirtualKeyCode: keyCodes[action.key], modifiers: action.shift ? 8 : 0};
      await send('Input.dispatchKeyEvent', {type: 'keyDown', ...key});
      await send('Input.dispatchKeyEvent', {type: 'keyUp', ...key});
    } else if (op === 'viewport') {
      if (![action.width, action.height].every(n => Number.isInteger(n) && n >= 1 && n <= 10000)) {
        throw new QAError('Invalid viewport size');
      }
      await send('Emulation.setDeviceMetricsOverride', {
        width: action.width, height: action.height, deviceScaleFactor: action.scale ?? 1,
        mobile: Boolean(action.mobile)
      });
    } else if (op === 'screenshot') {
      const extraSelectors = action.redactSelectors === undefined ? [] : action.redactSelectors;
      if (!Array.isArray(extraSelectors) || !extraSelectors.every(selector =>
        typeof selector === 'string' && selector.trim().length > 0)) {
        throw new QAError('Invalid screenshot redaction selector');
      }
      await send('Page.bringToFront');
      const selectors = ['input', 'textarea', 'select', '[contenteditable]', '[data-private]', ...extraSelectors.map(selector => selector.trim())];
      // Hidden values are not enough: hide entire input controls and explicit
      // private content while capturing. Free page text still requires review.
      const styleId = await evaluate(`(() => {
        const selectors = ${JSON.stringify(selectors)};
        try {
          // Parse every selector before creating a style or capturing pixels.
          for (const selector of selectors) document.querySelector(selector);
        } catch { return false; }
        const style = document.createElement('style');
        document.head.append(style);
        try {
          // Separate rules keep optional selectors from invalidating defaults.
          for (const selector of selectors) {
            style.sheet.insertRule(selector + ' { visibility: hidden !important; }', style.sheet.cssRules.length);
          }
        } catch { style.remove(); return false; }
        window.__projectQaScreenshotStyle = style;
        return true;
      })()`);
      if (!styleId) throw new QAError('Cannot apply screenshot redactions');
      try {
        const image = await send('Page.captureScreenshot', {format: 'png', captureBeyondViewport: false});
        // wx avoids overwriting evidence or following an existing symlink.
        await fs.writeFile(action.path, Buffer.from(image.data, 'base64'), {mode: 0o600, flag: 'wx'});
      } finally {
        await evaluate('window.__projectQaScreenshotStyle?.remove(); delete window.__projectQaScreenshotStyle;');
      }
    } else if (op === 'pause') {
      const ms = action.ms ?? 500;
      if (!Number.isFinite(ms) || ms < 0 || ms > 5000) throw new QAError('Pause must be between 0 and 5000 ms');
      await new Promise(resolve => setTimeout(resolve, ms));
    } else if (op === 'assert') {
      if (typeof action.expression !== 'string' || !await evaluate(action.expression)) {
        throw new QAError('Browser assertion failed');
      }
    } else {
      throw new QAError('Unsupported browser operation');
    }
  }

  const raw = await evaluate(`({
    path: location.href,
    controls: [...document.querySelectorAll('button,input,select,a,textarea')].slice(0,150).map((el, index) => ({
      index, tag: el.tagName.toLowerCase(),
      type: el.tagName === 'INPUT' ? el.type : undefined,
      disabled: Boolean(el.disabled),
      href: el.tagName === 'A' ? el.href : undefined
    }))
  })`);
  const inputTypes = new Set(['text', 'password', 'email', 'number', 'checkbox', 'radio', 'submit', 'button', 'hidden', 'date', 'tel', 'url', 'search']);
  const snapshot = {
    path: safePath(raw.path),
    controls: raw.controls.map(control => ({
      index: control.index, tag: control.tag,
      type: control.type ? (inputTypes.has(control.type) ? control.type : 'other') : undefined,
      disabled: control.disabled,
      href: control.href ? safePath(control.href) : undefined
    }))
  };
  console.log(JSON.stringify({snapshot, browserDiagnostics: diagnostics}, null, 2));
} catch (error) {
  // Do not print browser messages, selectors, expressions, URLs or filled values.
  const reason = error instanceof QAError ? error.message :
    (['EEXIST', 'ENOENT', 'EACCES'].includes(error.code) ? error.code : 'Unexpected setup or operation failure');
  console.error(`Local QA helper failed${actionIndex >= 0 ? ` at action ${actionIndex}` : ' during setup'}: ${reason}.`);
  console.error(JSON.stringify({browserDiagnostics: diagnostics}));
  process.exitCode = 1;
} finally {
  // Stop providing credentials before disabling interception or closing the tab.
  basicAuth = undefined;
  authAttempts.clear();
  if (fetchEnabled && ws?.readyState === WebSocket.OPEN) {
    try { await send('Fetch.disable'); }
    catch {
      console.error('Could not confirm authentication interception cleanup.');
      process.exitCode = 1;
    }
  }
  if (fetchFailed) process.exitCode = 1;
  if (targetId) {
    try {
      const closed = await localFetch(`/json/close/${encodeURIComponent(targetId)}`);
      if (!closed.ok) throw new QAError('Target cleanup failed');
      const cleanupDeadline = Date.now() + 3000;
      let stillPresent = true;
      while (stillPresent && Date.now() < cleanupDeadline) {
        const listed = await localFetch('/json/list');
        if (!listed.ok) throw new QAError('Cannot verify target cleanup');
        stillPresent = (await listed.json()).some(target => target.id === targetId);
        if (stillPresent) await new Promise(resolve => setTimeout(resolve, 100));
      }
      if (stillPresent) throw new QAError('Created target did not close');
    } catch {
      console.error('Could not confirm cleanup of the target created by this run.');
      process.exitCode = 1;
    }
  }
  rejectPending();
  if (ws && ws.readyState < WebSocket.CLOSING) ws.close();
}
