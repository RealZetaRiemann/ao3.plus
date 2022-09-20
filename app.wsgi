#! /usr/bin/python

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/home/ronia/ao3graph')
from app import app as application
#application.secret_key = secrets.token_bytes(32)                                        # check for tampering
