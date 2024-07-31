import logging
import os
import sys
import time
from pydicom import dcmread
from pynetdicom import AE, StoragePresentationContexts
from logger_config import scu_logger

MAX_RETRIES = 1
RETRY_DELAY = 2  # seconds
logging.basicConfig(filename='pynet_scu.log', level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def send_c_store(dcm_file, scu_id, aet,number_of_store):
    ae = AE(ae_title=aet)
    ae.requested_contexts = StoragePresentationContexts

    # retries = 0
    # while retries < MAX_RETRIES:
    try:
        # Establish association with SCP
        assoc = ae.associate('localhost', 11112,ae_title="yeah")

        if assoc.is_established:
            for i in range(number_of_stores):
                # Send C-STORE request
                dataset = dcmread(dcm_file)
                # Modify SOP Instance UID to ensure unique storage
                dataset.SOPInstanceUID = f"{i}"
                status = assoc.send_c_store(dataset)

                if status:
                    print(f"SCU {scu_id}: C-STORE request status: 0x{status.Status:04x}")
                    scu_logger.info(f'"{aet}" : <- C-STORE request status: 0x{status.Status:04x}')
                else:
                    print(f"SCU {scu_id}: Connection timed out, was aborted or received invalid response")
                    scu_logger.error(f'"{aet}": Connection timed out, was aborted or received invalid response')

            # Release the association after all stores are complete
            assoc.release()
            return
        else:
            print(f"SCU {scu_id}: Association rejected, aborted or never connected")
            scu_logger.error(f'"{aet}": Association rejected, aborted or never connected')

    except Exception as e:
        print(f"SCU {scu_id}: Association was rejected, retrying in {RETRY_DELAY} seconds... Error: {e}")
        scu_logger.error(f'"{aet}": Association was rejected, retrying in {RETRY_DELAY} seconds... Error: {e}')
    
        # Increment the retry count and wait before retrying
        # retries += 1
        # time.sleep(RETRY_DELAY)

    print(f"SCU {scu_id}: Failed to establish association after {MAX_RETRIES} retries")
    scu_logger.error(f'SCU {scu_id}: Failed to establish association after {MAX_RETRIES} retries')

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python scu.py <dcm_file> <scu_id> <aet>")
        sys.exit(1)

    dcm_file = sys.argv[1]
    scu_id = sys.argv[2]
    aet = sys.argv[3]
    number_of_stores=int(sys.argv[4])
   
    send_c_store(dcm_file, scu_id, aet,number_of_stores)
