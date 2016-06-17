#!/usr/bin/env python
import subprocess
import logging
from config import *
import pyclowder.extractors as extractors


def main():
    global extractorName, messageType, rabbitmqExchange, rabbitmqURL    

    # Set logging
    logging.basicConfig(format='%(levelname)-7s : %(name)s -  %(message)s', level=logging.WARN)
    logging.getLogger('pyclowder.extractors').setLevel(logging.INFO)

    # Connect to rabbitmq
    extractors.connect_message_bus(extractorName=extractorName, messageType=messageType,
                                   processFileFunction=process_file, rabbitmqExchange=rabbitmqExchange,
                                   rabbitmqURL=rabbitmqURL)


# ----------------------------------------------------------------------
# Process the file and upload the results
def process_file(parameters):
    global extractorName

    print parameters
    
    inputfile = parameters['inputfile']

    # Call word count command
    result = subprocess.check_output(['wc', inputfile], stderr=subprocess.STDOUT)
    (lines, words, characters, filename) = result.split()

    # Store results as metadata
    metadata = dict()
    metadata["extractor_id"] = extractorName
    metadata['lines'] = lines
    metadata['words'] = words
    metadata['characters'] = characters

    # Upload metadata
    extractors.upload_file_metadata(mdata=metadata, parameters=parameters)


if __name__ == "__main__":
    main()