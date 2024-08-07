import logging
import os
from pydicom import dcmread
from pydicom.dataset import Dataset
from pynetdicom import AE, StorageCommitmentPresentationContexts, evt
from pynetdicom.sop_class import StorageCommitmentPushModel
from logger_config import scu_logger

logging.basicConfig(filename='pynet_scu.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def handle_n_event_report(event):
    """Handle an N-EVENT-REPORT request from the SCP."""
    event_report_ds = event.dataset
    print('Received Storage Commitment N-EVENT-REPORT')
    scu_logger.info('Received Storage Commitment N-EVENT-REPORT')
    scu_logger.info(f'N-EVENT-REPORT dataset: {event_report_ds}')

def send_n_action(dcm_file):
    ae = AE()
    ae.requested_contexts = StorageCommitmentPresentationContexts

    handlers = [(evt.EVT_N_EVENT_REPORT, handle_n_event_report)]

    try:
        # Establish association with SCP
        assoc = ae.associate('127.0.0.1', 11112, ae_title="test", evt_handlers=handlers)
        # assoc = ae.associate('192.168.1.230', 105, ae_title="test", evt_handlers=handlers)
        print(f'assoc.is_established: {assoc.is_established}')
        print(f'assoc.is_rejected: {assoc.is_rejected}')
        if assoc.is_established:
            dataset = dcmread(dcm_file)

            action_ds = Dataset()
            action_ds.TransactionUID = "1.2.3"
            action_ds.ReferencedSOPSequence = [Dataset()]
            action_ds.ReferencedSOPSequence[0].ReferencedSOPClassUID = dataset.SOPClassUID
            action_ds.ReferencedSOPSequence[0].ReferencedSOPInstanceUID = dataset.SOPInstanceUID
            action_ds.ActionTypeID = 1  # Action Type ID can be adjusted as needed

            # Send N-ACTION request
            status = assoc.send_n_action(
                action_ds,
                action_type=action_ds.ActionTypeID,
                class_uid=StorageCommitmentPushModel,
                instance_uid=dataset.SOPInstanceUID
            )

            # Check if status is a Dataset or tuple
            if isinstance(status, Dataset):
                print(f"Storage Commitment request status: 0x{status.Status:04x}")
                scu_logger.info(f'Storage Commitment request status: 0x{status.Status:04x}')
            elif isinstance(status, tuple):
                print(f"Received status as tuple: {status}")
                scu_logger.info(f'Received status as tuple: {status}')
            else:
                print("Unknown response type")
                scu_logger.error('Unknown response type')

            # Release the association after all operations are complete
            assoc.release()
        else:
            print("Association rejected, aborted or never connected")
            scu_logger.error('Association rejected, aborted or never connected')

    except Exception as e:
        print(f"Error: {e}")
        scu_logger.error(f'Error: {e}')

if __name__ == "__main__":
    dcm_file = os.path.join(os.path.dirname(__file__), '..', 'DCM', '0015.DCM')
    send_n_action(dcm_file)
