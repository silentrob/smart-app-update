from __future__ import with_statement

from os import path, mkdir, devnull, getcwd, chdir
from twisted.internet.utils import getProcessOutputAndValue
from hashlib import md5
from uuid import uuid1

import ConfigParser
import errno

class CannotReadConfigError(Exception):
    """Unable to read config file"""

    def __str__(self):
        return '%s: %s' % (self.__doc__, ': '.join(self.args))

class ConfigFileDoesNotExistError(CannotReadConfigError):
    """Configuration does not exist"""

def read_config(file_name):
    cfg = ConfigParser.RawConfigParser()

    try:
        with open(path.expanduser(file_name)) as f:
            cfg.readfp(f)
    except (IOError, OSError), e:
        if e.errno == errno.ENOENT:
            raise ConfigFileDoesNotExistError(str(e))
        else:
            raise CannotReadConfigError(str(e))
    return cfg

class CommandFailed(Exception):
    """Raised when a shell command fails"""
    def __init__(self, value):
         self.value = value

    def __str__(self):
         return repr(self.value)

def cb(result):
    stdout, stderr, exitcode = result;
    if exitcode != 0:
        print("command executed and returned %d\n" % exitcode);
        print("stdout was %s\n" % stdout);
        print("stderr was %s\n" % stderr);

def call(cmd):
    cmd = [str(x) for x in cmd]
    executable = cmd.pop(0);
    output = getProcessOutputAndValue(executable, cmd);
    output.addCallback( cb );

def uuid():
    """
    generates a uuid, removes "-"'s
    """
    return str(uuid1()).replace('-', '')

def random_string(salt = "JoyentSalt"):
    m = md5()
    m.update(uuid())
    m.update(salt)
    return m.hexdigest()

def random_queue():
    return "smart+%s" % (random_string())

def update_or_create_repository(repository, projects_dir, git_user="git",
                                git_server="localhost"):
    project_path = path.join(projects_dir, repository[:-4])
    
    if path.exists(project_path):
        chdir(project_path)
        cmd = ["/opt/local/bin/git", "pull"]
    else:
        clone_uri = "%s@%s:%s" % (git_user, git_server, repository)
        cmd = ["/opt/local/bin/git", "clone", clone_uri, project_path]
    return call(cmd)

def process_config(config):
    return {
     'host': config.get('amqp', 'host'),
     'port': int(config.get('amqp', 'port')),
     'user_id': config.get('amqp', 'user_id'),
     'password': config.get('amqp', 'password'),
     'projects_dir': config.get('rsp', 'projects_dir'),
     'git_user': config.get('rsp', 'git_user'),
     'git_server': config.get('rsp', 'git_server'),
     'exchange': config.get('amqp', 'exchange'),
    }
