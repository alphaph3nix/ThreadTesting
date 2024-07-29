import logging

# Set up SCP logger
scp_logger = logging.getLogger('scp_logger')
scp_handler = logging.FileHandler('scp.log')
scp_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
scp_handler.setFormatter(scp_formatter)
scp_logger.addHandler(scp_handler)
scp_logger.setLevel(logging.INFO)

# Set up SCU logger
scu_logger = logging.getLogger('scu_logger')
scu_handler = logging.FileHandler('scu.log')
scu_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
scu_handler.setFormatter(scu_formatter)
scu_logger.addHandler(scu_handler)
scu_logger.setLevel(logging.INFO)
