# launch_scu.py
import concurrent.futures
import subprocess

# Define the DICOM file to send
dcm_file = 'C:\\workspace\\learning\\python\\ThreadTesting\\DCM\\0015.DCM'

def run_scu(scu_id):
    result = subprocess.run(['python', 'scu.py', dcm_file, str(scu_id), f'scu{scu_id}'], capture_output=True, text=True)
    return result.stdout

if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(run_scu, scu_id): scu_id for scu_id in range(100)}

        for future in concurrent.futures.as_completed(futures):
            scu_id = futures[future]
            try:
                data = future.result()
                print(f"SCU {scu_id} output:\n{data}")
            except Exception as exc:
                print(f"SCU {scu_id} generated an exception: {exc}")
