import logging
from pynetdicom import AE, evt, AllStoragePresentationContexts, VerificationPresentationContexts,StorageCommitmentPresentationContexts
import logger_config
from handlers import handle_echo,handle_store,handle_association_requested,handle_n_action

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
    (evt.EVT_REQUESTED, handle_association_requested),  # Ensure EVT_REQUESTED is registered
    (evt.EVT_N_ACTION, handle_n_action)
]

# Initialize the Application Entity (AE)
ae = AE(ae_title="test")
ae.supported_contexts = AllStoragePresentationContexts + VerificationPresentationContexts + StorageCommitmentPresentationContexts
# ae._require_called_aet=True
# ae._require_calling_aet=["ORTHANC"]
# ae.start_server(('127.0.0.1', 11112), block=False, evt_handlers=handlers)
ae.start_server(('192.168.1.34', 104), block=False, evt_handlers=handlers)
logging.info("Starting DICOM SCP on port 11112")
print("Starting DICOM SCP on port 11112")
input("type to exist\n")
