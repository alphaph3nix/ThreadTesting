import os
import logging
from pynetdicom import AE, evt, AllStoragePresentationContexts, VerificationPresentationContexts
import logger_config
from handlers import handle_echo,handle_store,handle_association_requested

# Configure logging
logging.basicConfig(filename='pynet_scp.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# scp_logger.info("********************************************************************************************************************************************************")
# logging.info("********************************************************************************************************************************************************")

# loggers = logging.root.manager.loggerDict
# for name in sorted(loggers.keys()):
#     print(name)

handlers = [
    (evt.EVT_C_STORE, handle_store),
    (evt.EVT_C_ECHO, handle_echo),
    (evt.EVT_REQUESTED, handle_association_requested)  # Ensure EVT_REQUESTED is registered
]


ae_scp_c_store = AE(ae_title="scp_c_store")
ae_scp_c_store.supported_contexts = AllStoragePresentationContexts
# ae_scp_c_store._require_called_aet=True
ae_scp_c_store.start_server(('192.168.1.34', 11113), block=False, evt_handlers=[handlers[0]])
logging.info("Starting scp_c_store on port 11113")

ae_scp_c_echo = AE(ae_title="scp_c_echo")
ae_scp_c_echo.supported_contexts = VerificationPresentationContexts
# ae_scp_c_echo._require_called_aet=True
ae_scp_c_echo.start_server(('localhost', 11114), block=False, evt_handlers=[handlers[1]])
logging.info("Starting scp_c_echo on port 11114")

input("type to exist\n")


# Initialize the Application Entity (AE)
ae = AE(ae_title="test")
ae.supported_contexts = AllStoragePresentationContexts + VerificationPresentationContexts
ae._require_called_aet=True
ae._require_calling_aet=["ORTHANC"]
ae.start_server(('127.0.0.1', 11112), block=False, evt_handlers=handlers)
logging.info("Starting DICOM SCP on port 11112")

# input("type to exist\n")
# Add supported presentation contexts
# print("Starting DICOM SCP on port 11112")
# scp_logger.info("Starting DICOM SCP on port 11112")




# ae.require_calling_aet
