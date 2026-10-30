#!/usr/bin/env python3
"""Codex/Orca Elixir fast feedback loop. Python 3.10+, standard library only.

Cooperative file locks coordinate commands using *this* wrapper, not processes
started directly by Orca or other tools. Does not delete or edit project data.
"""
import argparse
import contextlib
import fcntl
import hashlib
import json
import os
import re
import signal
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
from typing import Optional

# Match the v3 ACO resource-gate paths on macOS, so separate old/new wrappers
# cooperate rather than silently oversubscribing the machine.
DEFAULT_STATE = (Path.home() / "Library/Application Support/ai-coding-optimizer"
                 if sys.platform == "darwin" else Path.home() / ".cache/elixir-fastloop")
STATE = Path(os.environ.get("FASTLOOP_STATE_DIR", os.environ.get("ACO_STATE_DIR", str(DEFAULT_STATE)))).expanduser()
SOURCE_NAMES = ("lib", "src", "config", "apps", "priv", "test/support")
SOURCE_FILES = ("mix.exs", "mix.lock", ".tool-versions", ".mise.toml", "test/test_helper.exs")
EXCLUDE_PARTS = {"_build", "deps", "node_modules", ".git", ".elixir_ls", ".fetch", "_opam", "_checkouts", "static"}


def state_dir():
    if STATE.is_symlink():
        raise RuntimeError("State directory is a symlink; refusing to write")
    STATE.mkdir(parents=True, exist_ok=True, mode=0o700)
    return STATE


def cwd_dir(raw, validate_env=True):
    path = Path(raw).expanduser().resolve(strict=True)
    if not path.is_dir() or not (path / "mix.exs").is_file():
        raise ValueError("--cwd must be a real Elixir project directory containing mix.exs")
    if validate_env:
        if os.environ.get("MIX_OS_CONCURRENCY_LOCK", "").lower() in ("0", "false"):
            raise ValueError("Native Mix compilation locking is disabled; unset MIX_OS_CONCURRENCY_LOCK")
        if (path / "_build").is_symlink():
            raise ValueError("_build is a symlink; the compiler may be sharing compiled artifacts across worktrees")
        for name in ("MIX_BUILD_ROOT", "MIX_BUILD_PATH"):
            configured = os.environ.get(name)
            if configured:
                candidate = Path(configured).expanduser()
                target = (candidate if candidate.is_absolute() else path / candidate).resolve()
                if not target.is_relative_to(path):
                    raise ValueError(f"{name} points outside the worktree: {target}. Avoid shared build roots across Orca worktrees")
    return path


def key_for(cwd, env="test"):
    # MIX_BUILD_ROOT and MIX_DEPS_PATH are significant for compiling worktrees.
    val = f"{cwd}|{env}|{os.getenv('MIX_BUILD_PATH', '')}|{os.getenv('MIX_BUILD_ROOT', '')}|{os.getenv('MIX_DEPS_PATH', '')}"
    return hashlib.sha256(val.encode()).hexdigest()[:18]


def get_files(cwd):
    files = []
    for item in SOURCE_FILES:
        path = cwd / item
        if path.is_file() and not path.is_symlink():
            files.append(path)
    for item in SOURCE_NAMES:
        root = cwd / item
        if not root.exists() or root.is_symlink() or not root.is_dir():
            continue
        for base, dirs, filenames in os.walk(root, followlinks=False):
            dirs[:] = sorted(d for d in dirs if d not in EXCLUDE_PARTS and not (Path(base) / d).is_symlink())
            for name in sorted(filenames):
                path = Path(base) / name
                if path.is_file() and not path.is_symlink():
                    files.append(path)
    return sorted(set(files))


def fingerprint(cwd):
    h = hashlib.sha256()
    for path in get_files(cwd):
        h.update(str(path.relative_to(cwd)).encode() + b"\0")
        # Read file contents to detect changes even if mtime is unhelpful.
        with path.open("rb") as fp:
            while True:
                chunk = fp.read(1024 * 1024)
                if not chunk:
                    break
                h.update(chunk)
    return h.hexdigest()


def metadata_snapshot(cwd):
    snapshot = []
    for path in get_files(cwd):
        stat = path.stat()
        snapshot.append([str(path.relative_to(cwd)), stat.st_size, stat.st_mtime_ns, stat.st_ctime_ns])
    return snapshot


def stamp_path(cwd):
    return STATE / f"stamp_{key_for(cwd)}.json"


def built(cwd):
    # If the normal build directory is deleted, do not trust our stamp.
    root = Path(os.getenv("MIX_BUILD_ROOT", str(cwd / "_build")))
    if not root.is_absolute():
        root = cwd / root
    if "MIX_BUILD_PATH" in os.environ:
        target = Path(os.environ["MIX_BUILD_PATH"])
        root = target if target.is_absolute() else cwd / target
        return root.exists()
    return (root / "test").exists()


def warm_status(cwd, upgrade=False):
    if not built(cwd):
        return "test build missing"
    try:
        data = json.loads(stamp_path(cwd).read_text())
    except FileNotFoundError:
        return "warm stamp missing"
    except (ValueError, OSError):
        return "warm stamp unreadable"
    if data.get("env") != "test":
        return "warm stamp environment differs"
    try:
        if data.get("metadata") == metadata_snapshot(cwd):
            return "warm"
        if data.get("fingerprint") != fingerprint(cwd):
            return "source inputs changed"
        if upgrade:
            record_warm(cwd, data["fingerprint"])
    except OSError:
        return "source inputs unavailable"
    return "warm"


def is_warm(cwd, upgrade=False):
    return warm_status(cwd, upgrade=upgrade) == "warm"


def record_warm(cwd, digest):
    metadata = metadata_snapshot(cwd)
    if fingerprint(cwd) != digest or metadata_snapshot(cwd) != metadata:
        raise RuntimeError("Source changed before warm stamp could be recorded")
    parent = state_dir()
    content = {"worktree": str(cwd), "env": "test", "fingerprint": digest,
               "metadata": metadata, "compiled_at": time.time()}
    fd, name = tempfile.mkstemp(dir=parent, prefix="stamp_tmp_")
    try:
        with os.fdopen(fd, "w") as fp:
            json.dump(content, fp)
            fp.flush()
            os.fsync(fp.fileno())
        os.replace(name, stamp_path(cwd))
    finally:
        if os.path.exists(name):
            os.unlink(name)


@contextlib.contextmanager
def project_lock(cwd, shared=False):
    lock_dir = state_dir() / "locks"
    lock_dir.mkdir(parents=True, exist_ok=True)
    path = lock_dir / f"worktree-{hashlib.sha256(str(cwd).encode()).hexdigest()[:24]}.lock"
    with path.open("a+b") as fp:
        operation = fcntl.LOCK_SH if shared else fcntl.LOCK_EX
        try:
            fcntl.flock(fp, operation | fcntl.LOCK_NB)
        except BlockingIOError:
            print(f"[fastmix] Current worktree busy; waiting for {'test reader' if shared else 'compiler/test'} lock", flush=True)
            fcntl.flock(fp, operation)
        try:
            yield
        finally:
            fcntl.flock(fp, fcntl.LOCK_UN)


@contextlib.contextmanager
def global_slots(weight, slots):
    if weight < 1 or slots < 1 or weight > slots:
        raise ValueError("Invalid slot/weight: expected 1 <= weight <= slots")
    lock_dir = state_dir() / "locks"
    lock_dir.mkdir(parents=True, exist_ok=True)
    paths = [lock_dir / f"slot-{i}.lock" for i in range(slots)]
    allocator_path = lock_dir / "allocator.lock"
    begin = time.monotonic()
    last_print = 0.0
    while True:
        held = []
        # The shared allocator lock makes multi-token acquisition atomic,
        # including with the earlier ACO v3 scheduler.
        with allocator_path.open("a+b") as allocator:
            fcntl.flock(allocator, fcntl.LOCK_EX)
            try:
                for path in paths:
                    fp = path.open("a+b")
                    try:
                        fcntl.flock(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
                        held.append(fp)
                        if len(held) == weight:
                            break
                    except BlockingIOError:
                        fp.close()
                if len(held) < weight:
                    for fp in held:
                        fcntl.flock(fp, fcntl.LOCK_UN)
                        fp.close()
                    held = []
            finally:
                fcntl.flock(allocator, fcntl.LOCK_UN)
        if len(held) == weight:
            break
        elapsed = time.monotonic() - begin
        if elapsed > 1 and elapsed - last_print > 10:
            print(f"[fastmix] Waiting for global capacity ({weight}/{slots} slots), {elapsed:.0f}s elapsed", flush=True)
            last_print = elapsed
        time.sleep(0.25)
    try:
        yield
    finally:
        for fp in held:
            fcntl.flock(fp, fcntl.LOCK_UN)
            fp.close()


def child_env(schedulers, deps_partitions=0, partition=None, cwd=None):
    env = os.environ.copy()
    env["MIX_ENV"] = "test"
    if "ERL_FLAGS" not in env and schedulers is not None:
        env["ERL_FLAGS"] = f"+S {schedulers}:{schedulers}"
    elif "ERL_FLAGS" in env and schedulers is not None:
        print("[fastmix] Respecting your existing ERL_FLAGS; requested scheduler value not applied", flush=True)
    if deps_partitions:
        env["MIX_OS_DEPS_COMPILE_PARTITION_COUNT"] = str(deps_partitions)
    else:
        env.pop("MIX_OS_DEPS_COMPILE_PARTITION_COUNT", None)
    if partition is not None:
        env["MIX_TEST_PARTITION"] = str(partition)
    else:
        env.pop("MIX_TEST_PARTITION", None)
    if cwd is not None:
        # Custom test config must use ACO_TEST_DB_SUFFIX. We never change config automatically.
        env["ACO_TEST_DB_SUFFIX"] = hashlib.sha256(str(cwd).encode()).hexdigest()[:8]
    return env


def mix_bin(args):
    candidate = getattr(args, "mix_bin", None) or shutil.which("mix")
    if not candidate:
        raise RuntimeError("mix is not on PATH. Install/use your existing asdf Elixir toolchain")
    return str(candidate)


def run(argv, cwd, env):
    print("[fastmix] Running selected build/test command in the active workspace; arguments omitted from diagnostics", flush=True)
    start = time.monotonic()
    proc = None
    old = {}

    def forward(signum, _frame):
        if proc is not None and proc.poll() is None:
            try:
                os.killpg(proc.pid, signum)
            except ProcessLookupError:
                pass
        raise KeyboardInterrupt

    try:
        proc = subprocess.Popen(argv, cwd=cwd, env=env, start_new_session=True)
        for sig in (signal.SIGINT, signal.SIGTERM):
            old[sig] = signal.signal(sig, forward)
        code = proc.wait()
    except KeyboardInterrupt:
        print("[fastmix] Interrupted; stopping only the command launched by fastmix", file=sys.stderr)
        if proc is not None and proc.poll() is None:
            try:
                os.killpg(proc.pid, signal.SIGTERM)
                proc.wait(timeout=8)
            except ProcessLookupError:
                pass
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                proc.wait()
        code = 130
    finally:
        for sig, prev in old.items():
            signal.signal(sig, prev)
    print(f"[fastmix] Exit {code}, elapsed {time.monotonic()-start:.1f}s", flush=True)
    return code


def compile_locked(args, cwd, force=False):
    if not force and is_warm(cwd, upgrade=True):
        print("[fastmix] Test environment is warm; skipping redundant compile", flush=True)
        return 0
    prev = fingerprint(cwd)
    env = child_env(args.schedulers, args.deps_partitions)
    with global_slots(args.compile_weight, args.slots):
        rc = run([mix_bin(args), "compile"], cwd, env)
    if rc:
        return rc
    current = fingerprint(cwd)
    if current != prev:
        print("[fastmix] Source changed during compilation. No warm stamp recorded.", file=sys.stderr)
        return 3
    if not built(cwd):
        print("[fastmix] Build root not found after compile; cannot verify cache", file=sys.stderr)
        return 3
    record_warm(cwd, current)
    return 0


def default_slots():
    env = os.getenv("FASTLOOP_SLOTS")
    if env:
        return int(env)
    try:
        settings = json.loads((STATE / "settings.json").read_text())
        return int(settings.get("slots", 2))
    except (FileNotFoundError, ValueError, OSError):
        return 2


def add_common(parser):
    parser.add_argument("--cwd", default=".", help="Elixir project/worktree root")
    parser.add_argument("--schedulers", type=int, default=3, help="BEAM schedulers per test/compile process; default 3")
    parser.add_argument("--slots", type=int, default=default_slots(), help="Shared global heavy slots; MUST match for all Orca sessions")
    parser.add_argument("--compile-weight", type=int, default=2, help="Slots used for compilation; default all two")
    parser.add_argument("--deps-partitions", type=int, default=0, help="Optional Elixir 1.19+ dependency partitions, defaults off")
    parser.add_argument("--mix-bin", default=None, help=argparse.SUPPRESS)


def valid_args(args):
    if args.schedulers < 1 or args.schedulers > 12:
        raise ValueError("Use 1–12 BEAM schedulers here; recommend 2–4 initially")
    if not 1 <= args.compile_weight <= args.slots <= 12:
        raise ValueError("Require 1 <= compile-weight <= slots <= 12")
    if args.deps_partitions not in (0, 1, 2, 3, 4):
        raise ValueError("Dependency partitions must be 0–4; 0 means no override")


def cmd_compile(args):
    valid_args(args)
    cwd = cwd_dir(args.cwd)
    with project_lock(cwd):
        return compile_locked(args, cwd, args.force)


def cmd_test(args):
    valid_args(args)
    cwd = cwd_dir(args.cwd)
    tests = list(args.test_args)
    if tests and tests[0] == "--":
        tests.pop(0)
    forbidden = {"--force", "--no-compile", "--partitions", "--max-cases", "--max-requires"}
    if any(t.split("=")[0] in forbidden for t in tests):
        raise ValueError("Use wrapper --max-cases/--max-requires, not test-level force, partitions or no-compile")
    if args.test_db_suffix:
        if not re.fullmatch(r"[0-9]{1,8}", args.test_db_suffix):
            raise ValueError("--test-db-suffix must be 1–8 digits")
        config = cwd / "config/test.exs"
        if not config.is_file() or "MIX_TEST_PARTITION" not in config.read_text(encoding="utf-8", errors="replace"):
            raise ValueError("--test-db-suffix requires config/test.exs to use MIX_TEST_PARTITION")
    with project_lock(cwd):
        rc = compile_locked(args, cwd)
        if rc:
            return rc
        argv = [mix_bin(args), "test", "--no-compile", "--max-cases", str(args.max_cases), "--max-requires", str(args.max_requires)] + tests
        before = fingerprint(cwd)
        with global_slots(1, args.slots):
            rc = run(argv, cwd, child_env(args.schedulers, partition=args.test_db_suffix, cwd=cwd))
        if fingerprint(cwd) != before:
            print("[fastmix] WARNING: source changed during test; result is not a reliable validation", file=sys.stderr)
            return 3
        return rc


def approved_partition_config(cwd):
    path = cwd / "config/test.exs"
    if not path.exists():
        return False
    data = path.read_text(encoding="utf-8", errors="replace")
    return "MIX_TEST_PARTITION" in data and "ACO_TEST_DB_SUFFIX" in data


def cmd_shards(args):
    valid_args(args)
    cwd = cwd_dir(args.cwd)
    if args.partitions < 2 or args.partitions > args.slots:
        raise ValueError("--partitions must be between 2 and the global --slots limit")
    if not approved_partition_config(cwd):
        raise ValueError("config/test.exs must use both MIX_TEST_PARTITION and ACO_TEST_DB_SUFFIX to identify separate databases; see README")
    suffix = hashlib.sha256(str(cwd).encode()).hexdigest()[:8]
    print(f"[fastmix] Planned test partitions 1..{args.partitions}; per-worktree DB suffix {suffix}")
    print("[fastmix] Ensure partition-specific test databases EXIST and have matching migrations; this tool never creates or migrates databases.")
    if not args.execute:
        print("[fastmix] DRY RUN: use --execute --db-reviewed only after reviewing config and preparing test databases")
        return 0
    if not args.db_reviewed:
        raise ValueError("Refusing to start shards without --db-reviewed")
    with project_lock(cwd):
        rc = compile_locked(args, cwd)
        if rc:
            return rc
        # Project lock spans all shards so no wrapper compiler can invalidate this build.
        with global_slots(args.partitions, args.slots):
            log_dir = state_dir() / "logs" / key_for(cwd) / time.strftime("%Y%m%d-%H%M%S")
            log_dir.mkdir(parents=True, exist_ok=False)
            processes = []
            start = time.monotonic()
            try:
                source_at_start = fingerprint(cwd)
                for i in range(1, args.partitions + 1):
                    path = log_dir / f"partition-{i}.log"
                    out = path.open("wb")
                    env = child_env(args.schedulers, partition=i, cwd=cwd)
                    command = [mix_bin(args), "test", "--no-compile", "--partitions", str(args.partitions), "--max-cases", str(args.max_cases), "--max-requires", str(args.max_requires)]
                    proc = subprocess.Popen(command, cwd=cwd, env=env, stdout=out, stderr=subprocess.STDOUT)
                    out.close()
                    processes.append((i, proc, path))
                results = [(i, proc.wait(), path) for i, proc, path in processes]
            except KeyboardInterrupt:
                for _, proc, _ in processes:
                    if proc.poll() is None:
                        proc.terminate()
                for _, proc, _ in processes:
                    try:
                        proc.wait(timeout=8)
                    except subprocess.TimeoutExpired:
                        print(f"[fastmix] Child PID {proc.pid} still running; inspect manually", file=sys.stderr)
                return 130
            print(f"[fastmix] Shards elapsed {time.monotonic()-start:.1f}s")
            if fingerprint(cwd) != source_at_start:
                print("[fastmix] WARNING: source changed during partitioned tests; ignoring results", file=sys.stderr)
                return 3
            for i, code, path in results:
                print(f"[fastmix] Partition {i} exit {code}; log: {path}")
            return 0 if all(rc == 0 for _, rc, _ in results) else 2


def cmd_doctor(args):
    cwd = cwd_dir(args.cwd, validate_env=False)
    disk = shutil.disk_usage(cwd)
    print("Elixir/Phoenix worktree: current verified workspace (path omitted)")
    print("Machine logical CPU threads:", os.cpu_count())
    print("Disk available GiB:", round(disk.free / 1024**3, 1))
    print("Test files:", len(list((cwd / "test").rglob("*_test.exs"))) if (cwd / "test").exists() else 0)
    print("Build present:", built(cwd))
    status = warm_status(cwd)
    print("Warm test build stamp:", status == "warm", f"({status})")
    shard_isolation = approved_partition_config(cwd)
    print("Two-level shard database config present:", shard_isolation)
    if not shard_isolation:
        print("Shards disabled: review config/test.exs for both worktree and partition suffixes. A single focused test may use --test-db-suffix after reviewing its database name.")
    for var in ("ERL_FLAGS", "MIX_BUILD_ROOT", "MIX_BUILD_PATH", "MIX_DEPS_PATH", "MIX_OS_CONCURRENCY_LOCK"):
        if var in os.environ:
            print(f"{var}=<configured; value omitted>")
    if os.environ.get("MIX_OS_CONCURRENCY_LOCK", "").lower() in ("0", "false"):
        print("WARNING: Native Mix compilation lock is disabled. Re-enable it.")
    if shutil.which("elixir"):
        subprocess.run(["elixir", "--version"], check=False)
    print("Active Elixir/Mix processes (check PIDs before modifying anything):")
    if shutil.which("ps"):
        result = subprocess.run(["ps", "-axo", "pid,ppid,etime,%cpu,comm"], text=True, stdout=subprocess.PIPE, check=False)
        for line in result.stdout.splitlines():
            if any(s in line for s in ("beam.smp", "mix test", "mix compile", "elixir_ls")) and "fastmix.py" not in line:
                fields = line.split(None, 4)
                if len(fields) == 5:
                    print(" ".join(fields[:4]), Path(fields[4]).name)
    print("Note: 600 test cases are not the same as 600 test files; check ExUnit async settings.")
    return 0


def cmd_profile(args):
    valid_args(args)
    cwd = cwd_dir(args.cwd)
    with project_lock(cwd):
        with global_slots(args.compile_weight, args.slots):
            return run([mix_bin(args), "compile.elixir", "--profile", "time", "--long-compilation-threshold", "2"], cwd, child_env(args.schedulers))


def cli(argv=None):
    parser = argparse.ArgumentParser(description="Cooperative compile/test scheduling for Elixir 1.19 and Orca worktrees")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("doctor", help="Read-only environment diagnosis")
    p.add_argument("--cwd", default=".")
    p.set_defaults(fn=cmd_doctor)
    p = sub.add_parser("compile", help="Incremental test build with exclusive worktree lock")
    add_common(p)
    p.add_argument("--force", action="store_true", help="Repeat mix compile (does NOT run mix clean)")
    p.set_defaults(fn=cmd_compile)
    p = sub.add_parser("profile", help="Profile recompilation after a change, before a normal compile")
    add_common(p)
    p.set_defaults(fn=cmd_profile)
    p = sub.add_parser("test", help="Compile only if needed; then run targeted tests without recompiling")
    add_common(p)
    p.add_argument("--max-cases", type=int, default=3)
    p.add_argument("--max-requires", type=int, default=3)
    p.add_argument("--test-db-suffix", default=None, help="Explicit numeric MIX_TEST_PARTITION suffix for a reviewed single-test database")
    p.add_argument("test_args", nargs=argparse.REMAINDER, help="Use -- followed by test FILE / --stale / --failed")
    p.set_defaults(fn=cmd_test)
    p = sub.add_parser("shards", help="Partition full suite; DRY RUN by default; independent DBs mandatory")
    add_common(p)
    p.add_argument("--partitions", type=int, default=2)
    p.add_argument("--max-cases", type=int, default=2)
    p.add_argument("--max-requires", type=int, default=2)
    p.add_argument("--execute", action="store_true")
    p.add_argument("--db-reviewed", action="store_true")
    p.set_defaults(fn=cmd_shards)
    args = parser.parse_args(argv)
    try:
        if hasattr(args, "max_cases") and (args.max_cases < 1 or args.max_cases > 32 or args.max_requires < 1 or args.max_requires > 32):
            raise ValueError("max-cases and max-requires must both be between 1 and 32")
        return args.fn(args)
    except (RuntimeError, ValueError, OSError) as ex:
        print("fastmix ERROR:", type(ex).__name__, "(details omitted; check local configuration and command requirements)", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(cli())
