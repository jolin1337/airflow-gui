import subprocess
from log import logger

log = logger.getLogger(__name__)


def run_cmd(*vargs, **dargs):
    proc = subprocess.run(vargs, **dargs,
                          stdout=subprocess.PIPE,
                          universal_newlines=True)
    try:
        proc.check_returncode()
    except subprocess.CalledProcessError:
        log.error(proc.stdout)
        exit(1)
    return proc


def checkout(branch, new=False):
    cmd = ['git', 'checkout', branch]
    if new:
        cmd = cmd[:-1] + ['-b'] + cmd[-1:]
    return run_cmd(*cmd)


def add_all():
    return run_cmd('git', 'add', '-A')


def commit(msg, add_all=False):
    add_flag = ''
    if add_all:
        add_flag = 'a'
    return run_cmd('git', 'commit', f'-{add_flag}m', msg)


def push():
    return run_cmd('git', 'push') #TODO: Add current branch :')


def status():
    return run_cmd('git', 'status').stdout

def files_changed(sha):
    return run_cmd('git', 'show', '--stat', '--name-only', '--pretty=', '--raw', sha).stdout.split('\n')[:-1]
