import subprocess
from logger_config import debug_logger
import logging 

logging.basicConfig(filename='echo_scu.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# debug_logger()

def send_cecho():
    
    addr = '127.0.0.1'
    port = 104
    aec = 'PACS'  #called aet (aet of scp)
    # Adding verbose and debug flags to the command
    command = ['python', '-m', 'pynetdicom', 'echoscu', '-ll', 'info', '-aec', aec, addr, str(port)]

    result = subprocess.run(command, capture_output=True, text=True)
    logging.info(result)
    print(result)

if __name__ == "__main__":
    send_cecho()
