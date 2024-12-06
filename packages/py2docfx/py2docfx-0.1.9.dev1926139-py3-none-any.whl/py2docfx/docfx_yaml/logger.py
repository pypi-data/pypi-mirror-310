import os
import logging
import subprocess

def get_log_level():
    if os.environ.get('LOG_LEVEL') == 'WARNING':
        return logging.WARNING
    elif os.environ.get('LOG_LEVEL') == 'INFO':
        return logging.INFO
    
    return logging.ERROR

def setup_log_handlers(logger, log_file_name):
    file_handler = logging.FileHandler(filename=log_file_name, mode='a')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    
    stream_handeler = logging.StreamHandler()
    stream_handeler.setLevel(get_log_level())
    
    logger.addHandler(file_handler)
    logger.addHandler(stream_handeler)
    
    return logger

def get_logger(logger_name: str):
    file_name = os.path.join("logs", "log.txt")
    
    file_logger = logging.getLogger(logger_name)
    file_logger.setLevel(logging.INFO)
    
    if file_logger.hasHandlers():
        return file_logger
    
    file_logger = setup_log_handlers(file_logger, file_name)

    return file_logger

def get_package_logger(logger_name:str):
    package_name = os.environ.get('PROCESSING_PACKAGE_NAME')
    file_name = os.path.join("logs", "package_logs", f"{package_name}.txt")
    
    file_logger = logging.getLogger(logger_name)
    file_logger.setLevel(logging.INFO)

    if file_logger.hasHandlers():
        return file_logger

    file_logger = setup_log_handlers(file_logger, file_name)
    
    return file_logger

def log_subprocess_ouput(subprocess_out: subprocess.CompletedProcess, logger: logging.Logger):
    if subprocess_out.stdout:
        logger.info(subprocess_out.stdout)
    if subprocess_out.stderr:
        msgs = subprocess_out.stderr.split('\n')
        for msg in msgs:
            if msg is None or msg == "":
                continue
            if "WARNING:" in msg:
                logger.warning(msg)
            elif "ERROR:" in msg:
                logger.error(msg)
            else:
                logger.info(msg)
    if subprocess_out.returncode != 0:
        logger.error(f"Subprocess failed with return code {subprocess_out.returncode}")
        raise RuntimeError()
