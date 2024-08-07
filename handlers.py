
import os
import logging
from logger_config import scp_logger
from pydicom.dataset import Dataset

# Base directory to store received DICOM files
STORE_DIRECTORY = 'DCM_Saved'
# Ensure the storage directory exists
if not os.path.exists(STORE_DIRECTORY):
    os.makedirs(STORE_DIRECTORY)

def handle_association_requested(event):
    print("association handler called")
    # # print_contexts(event)
    # print(f'{event.assoc.acse.acceptor._address}\n')

    # print(f'{event.assoc.acse.requestor._address}\n')

    # print(check_requestor_contexts_in_acceptor_contexts(event.assoc.requestor.requested_contexts,event.assoc.acceptor.supported_contexts))
    # print(event.assoc.requestor.supported_contexts)
    

        # if context.abstract_syntax == Verification:
        #     delegate_to_echo_scp(event)
        #     return
        # elif context.abstract_syntax == CTImageStorage:
        #     delegate_to_store_scp(event)
        #     return
    # event.assoc.acse.send_reject(0x01,0x01,0x03)
    # # event.assoc.acse.send_reject(0x01,0x01,0x03)
    # """Handle an association request event."""
    # calling_aet = event.assoc.requestor.ae_title  # The AE title of the SCU
    # called_aet = event.assoc.requestor.requested_aet  # The AE title specified by the SCU for the SCP

    # print(f'Received association request: SCU: {calling_aet} to SCP: {called_aet}')
    # scp_logger.info(f'Received association request: SCU: {calling_aet} to SCP: {called_aet}')

    # # Check the calling AE title
    # if calling_aet != "testSCU":
    #     print(f"Rejecting association from {calling_aet}")
    #     scp_logger.info(f"Rejecting association from {calling_aet}")
    #     event.assoc.reject(reason=0x01)  # reject for calling AET mismatch
    #     return

    # # Check the called AE title
    # if called_aet != "OUR_SCP_AET":
    #     print(f"Rejecting association, expected AE title 'OUR_SCP_AET' but got '{called_aet}'")
    #     scp_logger.info(f"Rejecting association, expected AE title 'OUR_SCP_AET' but got '{called_aet}'")
    #     event.assoc.reject(reason=0x03)  # reject for called AET mismatch
    #     return

    # print(f"Association accepted from {calling_aet} to {called_aet}")
    # scp_logger.info(f"Association accepted from {calling_aet} to {called_aet}")

def handle_echo(event):
    print("echo handler called")
    return 0x0000

def handle_store(event):
    """Handle a C-STORE request."""
    # print(event.assoc.requestor.mode)                                                                                                             
    print("store handler called")
    ds = event.dataset
    ds.file_meta = event.file_meta
    calling_aet = event.assoc.requestor.ae_title.strip()
    calling_ip = event.assoc.requestor.address.strip()
    scp_logger.info(f"SCP: Received C-STORE request from (\"{calling_aet}\" at {calling_ip})")

    # Create a directory for the calling AET if it doesn't exist
    aet_directory = os.path.join(STORE_DIRECTORY, calling_aet)
    if not os.path.exists(aet_directory):
        os.makedirs(aet_directory)

    # Create a unique filename based on SOP Instance UID and AET
    filename = f"{calling_aet}_{ds.SOPInstanceUID}.dcm"
    filepath = os.path.join(aet_directory, filename)

    # Save the DICOM file
    ds.save_as(filepath, write_like_original=False)
    scp_logger.info(f"Stored DICOM file: {filepath}")

    return 0x0000  # Success status

def handle_n_action(event):
    print("N-ACTION handler called")
    ds = event.action_information
    print(f"Received N-ACTION request from SCU: {ds}")

    # Construct the N-EVENT-REPORT dataset
    event_report_ds = Dataset()
    event_report_ds.TransactionUID = ds.TransactionUID
    event_report_ds.ReferencedSOPSequence = ds.ReferencedSOPSequence
    event_report_ds.EventTypeID = 1  # Success

    return 0x0000, event_report_ds
    # is_stored = True  # Simuler que l'image a été stockée avec succès
    # ds= event.dataset
    # # Créer une réponse N-EVENT-REPORT
    # response_ds = Dataset()
    # response_ds.ReferencedSOPClassUID = ds.ReferencedSOPClassUID
    # response_ds.ReferencedSOPInstanceUID = ds.ReferencedSOPInstanceUID

    # if is_stored:
    #     print("Instance stockée avec succès.")
    #     return (0x0000, response_ds)  # OK
    # else:
    #     print("Échec du stockage de l'instance.")
    #     return (0x0110, response_ds)  # Échec

# usefull functions
def print_contexts(event):
    print('scu contexts') 
    print(event.assoc.requestor.requested_contexts)
    # for context in event.assoc.requestor.requested_contexts:
    #     print(context)
    print('********************************\n********************************\n********************************') 
    print(event.assoc.acceptor.supported_contexts)
    # print('scp contexts') 
    # for context in event.assoc.acceptor.supported_contexts:
    #     print(context)

def check_requestor_contexts_in_acceptor_contexts(A, B):
    set_B = set(B)  # Convert B to a set for fast lookup
    return all(element in set_B for element in A)


