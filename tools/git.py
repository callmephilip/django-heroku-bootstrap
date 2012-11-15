from fabric.api import *
from functools import wraps

def is_git_clean():
    git_status = local("git status", capture=True).lower()
    print "is_git_clean reports: %s" % git_status

    msgs = ["untracked files", "changes to be committed", "changes not staged for commit"]

    for msg in msgs:
        if git_status.find(msg) != -1:
            return False

    return  True

def check_git_state(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not is_git_clean():
            print "Cannot deploy: make sure your git is clean"
        else:
            return f(*args, **kwargs)
    return wrap