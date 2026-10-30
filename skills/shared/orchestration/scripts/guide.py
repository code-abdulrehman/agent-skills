#!/usr/bin/env python3
"""Read an installed Orca skill guide without starting tasks or changing app state."""
import argparse
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys

def resolve_cli(environment=None, platform=None, which=None):
    env = os.environ if environment is None else environment
    platform = sys.platform if platform is None else platform
    which = shutil.which if which is None else which
    explicit = env.get('ORCA_CLI_COMMAND')
    if explicit:
        # A configured executable is a single file/command name, never shell source.
        value = Path(explicit).expanduser()
        selected = str(value) if value.is_file() else which(explicit)
        if not selected or not os.access(selected, os.X_OK):
            raise ValueError('Configured Orca executable is unavailable; check ORCA_CLI_COMMAND locally')
        return selected
    command = 'orca-dev' if env.get('ORCA_DEV_REPO_ROOT') else ('orca-ide' if platform.startswith('linux') else 'orca')
    selected = which(command)
    if not selected:
        raise ValueError('Required Orca executable is unavailable; install/configure the intended Orca CLI')
    return selected

def guide_command(executable, guide, reference=None, references=False, full=False):
    if guide not in {'orchestration', 'orca-cli'}:
        raise ValueError('Unsupported guide identity')
    command = [executable, 'skills', 'get', guide]
    if reference:
        path = PurePosixPath(reference)
        if path.is_absolute() or '..' in path.parts or '\\' in reference or path.suffix != '.md' or not reference.startswith('references/'):
            raise ValueError('Use a relative references/*.md path reported by this Orca version')
        command += ['--reference', reference]
    elif references:
        command.append('--references')
    elif full:
        command.append('--full')
    return command

def main():
    default = Path(__file__).resolve().parent.parent.name
    if default not in {'orchestration', 'orca-cli'}:
        default = 'orchestration'
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--guide', choices=['orchestration', 'orca-cli'], default=default)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--reference')
    group.add_argument('--references', action='store_true')
    group.add_argument('--full', action='store_true')
    args = parser.parse_args()
    try:
        command = guide_command(resolve_cli(), args.guide, args.reference, args.references, args.full)
        result = subprocess.run(command, capture_output=True, text=True, timeout=45, shell=False)
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 2
    except (OSError, subprocess.TimeoutExpired):
        print('Orca guide could not be read; inspect the configured local CLI and its version', file=sys.stderr)
        return 2
    if result.returncode:
        # CLI errors can contain paths, runtime identifiers, or other local state.
        print('Orca guide command failed (exit %s); inspect help/permissions locally. No app restart or fallback was attempted.' % result.returncode, file=sys.stderr)
        return 2
    print(result.stdout, end='' if result.stdout.endswith('\n') else '\n')
    return 0

if __name__ == '__main__':
    sys.exit(main())
