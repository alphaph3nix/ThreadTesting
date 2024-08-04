import os
import logging
from pynetdicom import AE, evt, AllStoragePresentationContexts, VerificationPresentationContexts
from logger_config import scp_logger
from handlers import handle_echo,handle_store,handle_association_requested

# Configure logging
logging.basicConfig(filename='pynet_scp.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
scp_logger.info("********************************************************************************************************************************************************")
logging.info("********************************************************************************************************************************************************")

# loggers = logging.root.manager.loggerDict
# for name in sorted(loggers.keys()):
#     print(name)

def configure_logger(name, filename):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        file_handler = logging.FileHandler(filename)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger

logger_store = configure_logger('pynetdicom.dimse_primitives', 'pynetdicom_C_STORE.log')
logger_assoc = configure_logger('pynetdicom.association', 'pynetdicom_assoc.log')
logger_acse = configure_logger('pynetdicom.acse', 'pynetdicom_acse.log')

handlers = [
    (evt.EVT_C_STORE, handle_store),
    (evt.EVT_C_ECHO, handle_echo),
    (evt.EVT_REQUESTED, handle_association_requested)  # Ensure EVT_REQUESTED is registered
]


# ae_scp_c_store = AE(ae_title="scp_c_store")
# ae_scp_c_store.supported_contexts = AllStoragePresentationContexts
# ae_scp_c_store.start_server(('localhost', 11112), block=False, evt_handlers=[handlers[0]])


# ae_scp_c_echo = AE(ae_title="scp_c_echo")
# ae_scp_c_echo.supported_contexts = VerificationPresentationContexts
# ae_scp_c_echo.start_server(('localhost', 11112), block=False, evt_handlers=[handlers[1]])


# Initialize the Application Entity (AE)
ae = AE(ae_title="test")
ae.supported_contexts = AllStoragePresentationContexts + VerificationPresentationContexts
# Add supported presentation contexts
# Start SCP on port 11112
# print("Starting DICOM SCP on port 11112")
# scp_logger.info("Starting DICOM SCP on port 11112")
# logging.info("Starting DICOM SCP on port 11112")

# ae._require_called_aet=True
# ae._require_calling_aet=["ORTHANC"]

# ae.require_calling_aet
ae.start_server(('127.0.0.1', 11112), block=False, evt_handlers=handlers)
input("type to exist\n")