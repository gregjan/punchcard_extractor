#!/usr/bin/env python
import subprocess
import logging
from config import *
import pyclowder.extractors as extractors


def main():
    global extractorName, messageType, rabbitmqExchange, rabbitmqURL, registrationEndpoints

    # Set logging
    logging.basicConfig(format='%(levelname)-7s : %(name)s -  %(message)s', level=logging.WARN)
    logging.getLogger('pyclowder.extractors').setLevel(logging.INFO)
    logger = logging.getLogger('extractor')
    logger.setLevel(logging.DEBUG)

    # Setup
    extractors.setup(extractorName=extractorName,
                     messageType=messageType,
                     rabbitmqURL=rabbitmqURL,
                     rabbitmqExchange=rabbitmqExchange)

    # Register extractor info
    extractors.register_extractor(registrationEndpoints)

    # Connect to RabbitMQ
    extractors.connect_message_bus(extractorName=extractorName, messageType=messageType,
                                   processFileFunction=process_file, rabbitmqExchange=rabbitmqExchange,
                                   rabbitmqURL=rabbitmqURL)


# ----------------------------------------------------------------------
# Process the file and upload the results
def process_file(parameters):
    global extractorName
    
    inputfile = parameters['inputfile']

    # Call word count command
    result = subprocess.check_output(['wc', inputfile], stderr=subprocess.STDOUT)
    (lines, words, characters, filename) = result.split()

    # Context url
    context_url = 'https://clowder.ncsa.illinois.edu/contexts/metadata.jsonld'

    # Store results as metadata
    metadata = \
        {
            '@context': [
                context_url, {
                    'lines': 'http://clowder.ncsa.illinois.edu/' + extractorName + '#lines',
                    'words': 'http://clowder.ncsa.illinois.edu/' + extractorName + '#words',
                    'characters': 'http://clowder.ncsa.illinois.edu/' + extractorName + '#characters'
                }
            ],
            'attachedTo': {
                'resourceType': 'file', 'id': parameters["fileid"]
            },
            'agent': {
                '@type': 'cat:extractor',
                'extractor_id': 'https://clowder.ncsa.illinois.edu/clowder/api/extractors/' + extractorName
            },
            'content': {
                'lines': lines,
                'words': words,
                'characters': characters
            }
        }
    print metadata

    # Upload metadata
    extractors.upload_file_metadata_jsonld(mdata=metadata, parameters=parameters)


if __name__ == "__main__":
    main()
