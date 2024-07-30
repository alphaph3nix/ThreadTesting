import os
import logging
from logger_config import scp_logger
from pynetdicom import AE, evt, AllStoragePresentationContexts
 #for logger = logging.getLogger('scp_logger') to work

# Directory to store received DICOM files
STORE_DIRECTORY = 'DCM_Saved'

# Ensure the storage directory exists
if not os.path.exists(STORE_DIRECTORY):
    os.makedirs(STORE_DIRECTORY)

# Configure logging
logging.basicConfig(filename='pynet_scp.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
scp_logger.info("********************************************************************************************************************************************************")
logging.info("********************************************************************************************************************************************************")

def handle_store(event):
    """Handle a C-STORE request."""
    ds = event.dataset
    ds.file_meta = event.file_meta
    calling_aet = event.assoc.requestor.ae_title.strip()
    calling_ip = event.assoc.requestor.address.strip()
    scp_logger.info(f" SCP: Received C-ECHO request from (\"{calling_aet}\" at { calling_ip})")
    
    # Create a unique filename based on SOP Instance UID and AET
    filename = f"{calling_aet}_{ds.SOPInstanceUID}.dcm"
    filepath = os.path.join(STORE_DIRECTORY, filename)

    # Save the DICOM file
    ds.save_as(filepath, write_like_original=False)
    scp_logger.info(f"Stored DICOM file: {filepath}")
    
    
    return 0x0000  # Success status

handlers = [(evt.EVT_C_STORE, handle_store)]

# Initialize the Application Entity (AE)
ae = AE()

# Add supported presentation contexts
ae.supported_contexts = AllStoragePresentationContexts

# Start SCP on port 11112
scp_logger.info("Starting DICOM SCP on port 11112")
logging.info("Starting DICOM SCP on port 11112")

ae.start_server(('localhost', 11112), evt_handlers=handlers)
