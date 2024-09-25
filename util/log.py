import logging
import util.string_format as string_format
import util.file as file

def track(contrato, message, level = logging.ERROR):
    filename = './files/logs/' + string_format.normalizar_nome_arquivo('log_'+ contrato +'.txt')
    file.checkAndCreateFolder(filename)
    logger = logging.getLogger()
    if logger.hasHandlers():
        logger.handlers.clear()
    logging.basicConfig(
        filename=filename,
        filemode='a',  # append mode
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=level
    )
    # Log the message at the correct level
    if level == logging.DEBUG:
        logger.debug(message)
    elif level == logging.INFO:
        logger.info(message)
    elif level == logging.WARNING:
        logger.warning(message)
    elif level == logging.ERROR:
        logger.error(message)
    elif level == logging.CRITICAL:
        logger.critical(message)