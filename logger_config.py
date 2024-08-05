import logging

#function to config loggers
def configure_logger(name, filename):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        file_handler = logging.FileHandler(filename)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger

# Set up SCP logger
scp_logger = logging.getLogger('scp_logger')
scp_handler = logging.FileHandler('scp.log')
scp_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
scp_handler.setFormatter(scp_formatter)
scp_logger.addHandler(scp_handler)
scp_logger.setLevel(logging.INFO)
scp_logger.propagate=False

# Set up SCU logger
scu_logger = logging.getLogger('scu_logger')
scu_handler = logging.FileHandler('scu.log')
scu_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
scu_handler.setFormatter(scu_formatter)
scu_logger.addHandler(scu_handler)
scu_logger.setLevel(logging.INFO)
scu_logger.propagate=False


# # later add all pynetloggers if i want to not log on root logger (without )
# logger_store = configure_logger('pynetdicom.dimse_primitives', 'pynetdicom_C_STORE.log')
# logger_assoc = configure_logger('pynetdicom.association', 'pynetdicom_assoc.log')
# logger_acse = configure_logger('pynetdicom.acse', 'pynetdicom_acse.log')



