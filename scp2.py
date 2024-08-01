import logging

from pynetdicom import AE, evt, debug_logger
from pynetdicom.sop_class import Verification


def handle_open(event):
    """Print the remote's (host, port) when connected."""
    msg = 'Connected with remote at {}'.format(event.address)
    print(msg)

def handle_accepted(event, arg1, arg2):
    """Demonstrate the use of the optional extra parameters"""
    print("Extra args: '{}' and '{}'".format(arg1, arg2))

# If a 2-tuple then only `event` parameter
# If a 3-tuple then the third value should be a list of objects to pass the handler
handlers = [
    (evt.EVT_CONN_OPEN, handle_open),
    (evt.EVT_ACCEPTED, handle_accepted, ['optional', 'parameters']),
]

ae = AE()
ae.add_supported_context(Verification)
ae.start_server(("127.0.0.1", 11112), evt_handlers=handlers)