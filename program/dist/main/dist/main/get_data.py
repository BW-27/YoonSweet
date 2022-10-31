from datetime import datetime
import requests
import os.path
import re

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


def scrape_list_file_csv(list_url, list_filepath):
    for url, filepath in zip(list_url, list_filepath):
        try:
            logger.debug("requesting data from " + url)
            req = requests.get(url)
        except Exception as Arguments:
            logger.error(Arguments)
            logger.error("couldn't establish url connection request with " + url)
            logger.info("trying to find files in local storage")
            for check_filepath in list_filepath:
                if (not os.path.isfile(check_filepath)):
                    logger.error("couldn't load all required files")
                    return False
            logger.debug("loaded all required files")
            logger.info("moving to next step without updating files")
            return True
        try:
            logger.debug("trying to access file " + os.path.abspath(filepath))
            output = open(filepath, "wb")
        except Exception as Arguments:
            logger.error(Arguments)
            return False
        output.write(req.content)
        logger.debug("writing data to file " + os.path.abspath(filepath))
        output.close()
    return True

def get_song_info(song_number, filepath):
    try:
        list_fd = open(filepath, "r", encoding="utf-8")
    except Exception as Arguments:
        logger.error(Arguments)
        return

    for i in range(song_number):
        next(list_fd)
    line = list_fd.readline()
    if (not line):
        list_fd.close()
        return None
    line = re.split(r',(?![ ])', line)
    list_fd.close()
    
    song_artist = line[0].strip('\"')
    if (not song_artist):
        song_artist = "Unknown"
    song_name = line[1].strip('\"')
    if (not song_name):
        song_name = "Unknown"
    song_info = [song_artist, song_name]

    return (song_info)
