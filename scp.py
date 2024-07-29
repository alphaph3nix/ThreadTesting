import os
import logging
from pynetdicom import AE, evt, AllStoragePresentationContexts

# Directory to store received DICOM files
STORE_DIRECTORY = 'DCM_Saved'

# Ensure the storage directory exists
if not os.path.exists(STORE_DIRECTORY):
    os.makedirs(STORE_DIRECTORY)

# Configure logging
logging.basicConfig(filename='scp.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('SCP_Logger')

def handle_store(event):
    """Handle a C-STORE request."""
    ds = event.dataset
    ds.file_meta = event.file_meta
    aet = event.assoc.requestor.ae_title
    
    # Create a unique filename based on SOP Instance UID and AET
    filename = f"{aet}_{ds.SOPInstanceUID}.dcm"
    filepath = os.path.join(STORE_DIRECTORY, filename)

    # Save the DICOM file
    ds.save_as(filepath, write_like_original=False)
    logger.info(f"Stored DICOM file: {filepath}")
    
    return 0x0000  # Success status

handlers = [(evt.EVT_C_STORE, handle_store)]

# Initialize the Application Entity (AE)
ae = AE()

# Add supported presentation contexts
ae.supported_contexts = AllStoragePresentationContexts

# Start SCP on port 11112
logger.info("Starting DICOM SCP on port 11112")
ae.start_server(('localhost', 11112), evt_handlers=handlers)
