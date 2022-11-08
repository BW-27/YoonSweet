# logging module for debugging
import logging

# Create and configure logger
logging.basicConfig(filename="debug.log",
                    format="%(asctime)s %(message)s",
                    filemode="a")
# Creating an object
logger = logging.getLogger()
# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)


def type_url():
    try:
        url_fd = open("source/url", "r", encoding="utf-8")
    except Exception as Argument:
        logger.error(Argument)
        return None
    list_url = []
    list_url = url_fd.read().splitlines()
    url_fd.close()
    return list_url

def type_data_list_filepath():
    try:
        filepath_fd = open("source/data_list_filepath", "r", encoding="utf-8")
    except Exception as Argument:
        logger.error(Argument)
        return None
    list_filepath = []
    list_filepath = filepath_fd.read().splitlines()
    filepath_fd.close()
    return list_filepath

def type_url_list_filepath():
    try:
        filepath_fd = open("source/url_list_filepath", "r", encoding="utf-8")
    except Exception as Argument:
        logger.error(Argument)
        return None
    list_filepath = []
    list_filepath = filepath_fd.read().splitlines()
    filepath_fd.close()
    return list_filepath
