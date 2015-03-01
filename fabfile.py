from fabric.api import local, run, env
import datetime, os
#env.hosts = ['host1', 'host2']
#/Users/ibelle/.virtualenvs/garak/bin/err.py

now = datetime.datetime.today()
timestamp = now.strftime("%Y%m%d%H%M")
venv_path = os.environ['VIRTUAL_ENV']
env.user = os.environ['USER']
env.sudo_user = env.user

def start_err(dameon=None):
    if not dameon:
        dameon=''

    local("err.py -c data/  -H %s" % dameon)