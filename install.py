#!/usr/bin/env python3
"""Install local audited skill packages without overwriting existing skills."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parent

def identity(path):
    try:
        text = (path / 'SKILL.md').read_text(encoding='utf-8')
    except (OSError, UnicodeError):
        return None
    match = re.search(r'\A---\s*\n[\s\S]*?^name:\s*[\"\x27]?([a-z0-9-]+)[\"\x27]?\s*$', text, re.M)
    return match.group(1) if match else None

def existing(root):
    names = set()
    if not root.is_dir():
        return names
    # Include nested system/plugin-like registrations without following directory symlinks.
    for base, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', '.venv', '__pycache__'}]
        for name in dirs:
            p = Path(base) / name
            names.add(name)
            skill_name = identity(p)
            if skill_name:
                names.add(skill_name)
        if 'SKILL.md' in files:
            skill_name = identity(Path(base))
            if skill_name:
                names.add(skill_name)
    return names

def preflight(items):
    for item in items:
        name = item['name']
        if not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,63}', name):
            raise ValueError('Invalid catalog skill identity')
        raw = ROOT / item['path']
        source = raw.resolve()
        if ROOT not in source.parents or raw.is_symlink() or not source.is_dir():
            raise ValueError('Invalid catalog skill path')
        if identity(source) != name:
            raise ValueError('Catalog and SKILL.md identity differ: ' + name)
        actual = {}
        for base, dirs, files in os.walk(source, followlinks=False):
            if any((Path(base) / d).is_symlink() for d in dirs):
                raise ValueError('Symlinked skill directory rejected: ' + name)
            for filename in files:
                p = Path(base) / filename
                if p.is_symlink():
                    raise ValueError('Symlinked skill file rejected: ' + name)
                actual[p.relative_to(source).as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
        if actual != item['sha256']:
            raise ValueError('Skill integrity check failed: ' + name)

def targets(args):
    home = Path.home()
    configured = {
        'codex': Path(os.environ.get('CODEX_HOME', str(home / '.codex'))) / 'skills',
        'claude': Path(os.environ.get('CLAUDE_CONFIG_DIR', str(home / '.claude'))) / 'skills',
        'shared': home / '.agents' / 'skills',
    }
    if args.dest:
        return [('custom', Path(args.dest).expanduser().absolute())]
    if args.agent == 'auto':
        result = [(k, v) for k, v in configured.items() if v.parent.is_dir()]
        if not result:
            raise ValueError('No supported agent directory detected; choose --agent or --dest explicitly')
        return result
    return [(args.agent, configured[args.agent])]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--agent', choices=['auto', 'codex', 'claude', 'shared'], default='auto')
    group.add_argument('--dest', help='Explicit skill directory for another compatible agent')
    parser.add_argument('--skill', action='append', help='Install only this skill identity; repeatable')
    parser.add_argument('--variant', help='Exact catalog path of a preferred variant')
    parser.add_argument('--apply', action='store_true', help='Copy missing skills; default is dry run')
    parser.add_argument('--dry-run', action='store_true', help='Explicit preview (default)')
    args = parser.parse_args()
    if args.apply and args.dry_run:
        parser.error('--apply and --dry-run cannot be combined')
    data = json.loads((ROOT / 'catalog.json').read_text(encoding='utf-8'))
    if data.get('format') != 1:
        raise ValueError('Unsupported catalog version')
    items = sorted(data['skills'], key=lambda x: (x['name'], x['path']))
    if args.skill:
        unknown = set(args.skill) - {x['name'] for x in items}
        if unknown:
            raise ValueError('Unknown skill requested')
        items = [x for x in items if x['name'] in args.skill]
    if args.variant:
        items = [x for x in items if x['path'] == args.variant]
        if len(items) != 1:
            raise ValueError('--variant must match one catalog path')
    preflight(items)
    selected = targets(args)
    for label, target in selected:
        resolved = target.resolve()
        if resolved == ROOT or ROOT in resolved.parents or resolved in ROOT.parents:
            raise ValueError('Install destination must be outside the collection')
        if target.exists() and not target.is_dir():
            raise ValueError('Install destination is not a directory')
    totals = {'installed': 0, 'would_install': 0, 'skipped_existing': 0, 'skipped_variant': 0}
    for label, target in selected:
        known = existing(target)
        seen = set()
        for item in items:
            name = item['name']
            if name in seen:
                totals['skipped_variant'] += 1
                continue
            seen.add(name)
            dest = target / name
            if name in known or os.path.lexists(dest):
                totals['skipped_existing'] += 1
                continue
            if not args.apply:
                totals['would_install'] += 1
                continue
            target.mkdir(parents=True, exist_ok=True)
            try:
                dest.mkdir()  # Exclusive reservation: never replace a racing installer or a symlink.
            except FileExistsError:
                totals['skipped_existing'] += 1
                continue
            try:
                source = ROOT / item['path']
                for child in source.iterdir():
                    if child.is_dir():
                        shutil.copytree(child, dest / child.name, copy_function=shutil.copyfile)
                    else:
                        shutil.copyfile(child, dest / child.name)
                for rel in item['sha256']:
                    original = source / rel
                    copied = dest / rel
                    copied.chmod(0o755 if original.stat().st_mode & 0o111 else 0o644)
                    if hashlib.sha256(copied.read_bytes()).hexdigest() != item['sha256'][rel]:
                        raise ValueError('Installed copy integrity failed')
            except BaseException:
                shutil.rmtree(dest)  # Only this invocation's exclusively created directory.
                raise
            known.add(name)
            totals['installed'] += 1
    print(json.dumps({'mode': 'apply' if args.apply else 'dry-run', 'agents': [k for k, _ in selected], **totals}, sort_keys=True))

if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError) as error:
        # Avoid dumping local paths or credentials through exception messages.
        print('Installation stopped: ' + (str(error) if isinstance(error, ValueError) else type(error).__name__), file=sys.stderr)
        sys.exit(1)
