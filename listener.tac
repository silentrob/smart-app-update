from twisted.internet.defer import inlineCallbacks
from twisted.internet import reactor
from twisted.internet.protocol import ClientCreator
from twisted.application import service

from txamqp.protocol import AMQClient
from txamqp.client import TwistedDelegate
from txamqp import spec

from gitosis_update_listener.listener import gotConnection
from gitosis_update_listener.helpers import process_config, read_config
from gitosis_update_listener import settings

config = process_config(read_config(settings.gitosis_config))
s = spec.load(settings.spec_file)

authentication = {"LOGIN": config['user_id'],
                  "PASSWORD": config['password']}

d = ClientCreator(reactor, AMQClient, delegate=TwistedDelegate(), vhost="/",
    spec=s).connectTCP(config['host'], config['port'])

d.addCallback(gotConnection, authentication)

application = service.Application("gitosis_update_listener")
