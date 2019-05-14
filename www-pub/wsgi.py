#!/usr/bin/python3
import os

virtenv = os.environ['OPENSHIFT_PYTHON_DIR'] + '/virtenv/'
virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
try:
    with open(virtualenv) as f:
        code = compile(f.read(), virtualenv, 'exec')
        exec(code, global_vars, local_vars)
except IOError:
     pass
#
# IMPORTANT: Put any additional includes below this line.  If placed above this
# line, it's possible required libraries won't be in your searchable path
#

import os
os.chdir(os.environ['OPENSHIFT_REPO_DIR'])

from server import app as application

