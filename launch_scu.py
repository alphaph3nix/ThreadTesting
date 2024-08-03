import concurrent.futures
import subprocess
import os
from logger_config import scu_logger
import pydicom


# Define the DICOM file to send
dcm_file = os.path.join(os.path.dirname(__file__), '..', 'DCM\\0020.DCM') 

def run_scu(scu_id,number_of_stores):
    result = subprocess.run(['python', 'scu.py', dcm_file, str(scu_id), f'scu{scu_id}',str(number_of_stores)], capture_output=True, text=True)
    return result.stdout

if __name__ == "__main__":
    scu_logger.info("********************************************************************************************************************************************************")
    data=pydicom.dcmread(dcm_file)
    print(type(data))
    print('NumberOfFrames' in data)
    
    print( data.NumberOfFrames)

    max_scu = 1
    number_of_stores=1
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_scu) as executor:
        futures = {executor.submit(run_scu, scu_id,number_of_stores): scu_id for scu_id in range(max_scu)}

        for future in concurrent.futures.as_completed(futures):
            scu_id = futures[future]
            try:
                data = future.result()
                print(f"SCU {scu_id} output:\n{data}")
            except Exception as exc:
                print(f"SCU {scu_id} generated an exception: {exc}")
