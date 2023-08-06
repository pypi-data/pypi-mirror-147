import glob
import os
import os.path
import subprocess
import sys
from typing import Tuple, Generator

import git

from pymultigit.configs import ConfigOutput, ConfigDebug, ConfigGrep, ConfigPull, ConfigMain


def projects(sort: bool) -> Generator[Tuple[str, str], None, None]:
    """
    the method returns tuples of (project_name, project_dir)
    """
    if ConfigMain.use_glob:
        repos_list = [os.path.dirname(x) for x in glob.glob('*/.git')]
    else:
        repos_list = ConfigMain.folders
    if sort:
        repos_list.sort()
    for x in repos_list:
        yield x, x


def run(args, do_exit=True) -> Tuple[str, str, int]:
    with subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
        (res_out, res_err) = p.communicate()
        res_out = res_out.decode()
        res_err = res_err.decode()
        if p.returncode:
            print(f'errors while running [{args}]...')
            print(res_out, end='', file=sys.stderr)
            print(res_err, end='', file=sys.stderr)
            if do_exit:
                sys.exit(p.returncode)
    return res_out, res_err, p.returncode


def do_count(fnc, attr_name, not_attr_name, attr_plural, print_attr, print_not_attr) -> None:
    count = 0
    count_attr = 0
    for (project_name, project_dir) in projects(sort=ConfigMain.sort):
        count += 1
        repo = git.Repo(project_dir)
        attr = fnc(repo)
        if attr:
            count_attr += 1
        if attr:
            if print_attr:
                if ConfigOutput.terse:
                    print(project_name)
                else:
                    print(f'project [{project_name}] {attr_name}')
        else:
            if print_not_attr:
                if ConfigOutput.terse:
                    print(project_name)
                else:
                    print(f'project [{project_name}] {not_attr_name}')
    if ConfigOutput.stats:
        print(f'scanned [{count}] projects')
        print(f'[{count_attr}] projects {attr_plural}')


def do_for_all_projects(fnc) -> None:
    count = 0
    count_not_found = 0
    count_error = 0
    count_ok = 0
    orig_dir = os.getcwd()
    for (project_name, project_dir) in projects(sort=ConfigMain.sort):
        if ConfigDebug.verbose:
            print(f'doing [{project_name}] at [{project_dir}]...', end="")
            sys.stdout.flush()
        count += 1
        if os.path.isdir(project_dir):
            os.chdir(project_dir)
            ret = fnc(project_name, project_dir)
            if ret:
                count_error += 1
            else:
                count_ok += 1
            if ConfigDebug.verbose:
                print('OK')
            os.chdir(orig_dir)
        else:
            if ConfigDebug.verbose:
                print('NOT FOUND')
            count_not_found += 1
    if ConfigOutput.stats:
        print(f'scanned [{count}] projects')
        print(f'[{count_not_found}] not found')
        print(f'[{count_error}] error')
        print(f'[{count_ok}] ok')


def is_dirty(repo) -> bool:
    return repo.is_dirty()


def has_untracked_files(repo) -> bool:
    return len(repo.untracked_files) > 0


def non_synchronized_with_upstream(_repo: str) -> bool:
    return False


def do_build(_project_name: str, project_dir: str) -> None:
    makefile = os.path.join(project_dir, 'Makefile')
    bootstrap = os.path.join(project_dir, 'bootstrap')
    if os.path.isfile(makefile):
        pass
    if os.path.isfile(bootstrap):
        pass
    if ConfigOutput.stats:
        pass


def do_pull(_project_name: str, _project_dir: str) -> int:
    args = ['git', 'pull']
    if ConfigDebug.git_verbose:
        args.append('--verbose')
    if ConfigPull.pull_quiet:
        args.append('--quiet')
    return subprocess.call(args)


def do_grep(_project_name: str, project_dir: str) -> None:
    args = ['git', 'grep']
    if ConfigDebug.git_verbose:
        args.append('--verbose')
    if ConfigDebug.git_quiet:
        args.append('--quiet')
    args.append(ConfigGrep.regexp)
    if ConfigGrep.files is not None:
        args.extend([
            "--",
            ConfigGrep.files
        ])
    with subprocess.Popen(
        args,
        shell=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ) as pipe:
        for line in pipe.stdout:
            print(f"{project_dir}/{line.decode()}", end="")
        if pipe.returncode:
            raise subprocess.CalledProcessError(
                returncode=pipe.returncode,
                cmd=' '.join(args),
            )


def do_local_branch(_project_name: str, _project_dir: str) -> int:
    args = ['git', 'branch', '--show-current']
    if ConfigDebug.git_verbose:
        args.append('--verbose')
    if ConfigDebug.git_quiet:
        args.append('--quiet')
    return subprocess.call(args)


def do_remote_branch(_project_name: str, _project_dir: str) -> int:
    args = ['git', 'branch', '--remotes', '--show-current']
    if ConfigDebug.git_verbose:
        args.append('--verbose')
    if ConfigDebug.git_quiet:
        args.append('--quiet')
    return subprocess.call(args)


def do_clean(_project_name: str, _project_dir: str) -> int:
    args = ['git', 'clean', '-ffxd']
    if ConfigDebug.git_verbose:
        args.append('--verbose')
    if ConfigDebug.git_quiet:
        args.append('--quiet')
    return subprocess.call(args)


def do_status_msg(project_name: str, msg: str) -> int:
    (res_out, res_err, _) = run([
        'git',
        'status',
        # porcelain is guaranteed to have parsable output and not
        # change across git versions
        '--porcelain',
        # when using --porcelain branch information is not shown,
        # this flag makes it not so, the problem with it is that
        # it produces output which should be parsed and that is
        # why we do not used it and use the 'git rev-list' that follows...
        # '--branch'
        # '--short',
    ])
    if res_out != '' or res_err != '':
        print(msg.format(project_name=project_name))
        if ConfigDebug.verbose:
            print(res_out, end='')
            print(res_err, end='')
        return 1
    (res_out, res_err, _) = run([
        'git',
        'rev-list',
        '--left-only',
        '--count',
        '@...@{upstream}',
    ])
    if res_out != '0\n' or res_err != '':
        if ConfigOutput.terse:
            msg = project_name
        else:
            msg = f'project [{project_name}] is not synced'
        print(msg)
        if ConfigDebug.verbose:
            print(res_out, end='')
            print(res_err, end='')
        return 1
    return 0


def do_status(project_name: str, _project_dir: str) -> int:
    if ConfigOutput.terse:
        msg = f"{project_name}"
    else:
        msg = f"project [{project_name}] is dirty"
    return do_status_msg(project_name=project_name, msg=msg)


def do_dirty(project_name: str, project_dir: str) -> int:
    if ConfigOutput.terse:
        msg = project_name
    else:
        msg = f"project [{project_name}] at directory [{project_dir}]"
    return do_status_msg(project_name=project_name, msg=msg)


def do_print(project_name: str, project_dir: str) -> None:
    if ConfigDebug.verbose:
        print(project_name, project_dir)
    else:
        print(project_name)
