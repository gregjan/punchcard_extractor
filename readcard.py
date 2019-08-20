#!/usr/bin/env python

"""Example Clowder script."""

import logging

from pyclowder.extractors import Extractor
import pyclowder.files

from PIL import Image
from punchcards.normalize import find_card
from punchcards.punchcard import PunchCard


class PunchCardReader(Extractor):
    """Reads the line of text encoded in an image of a punchcard."""
    def __init__(self):
        Extractor.__init__(self)

        # add any additional arguments to parser
        # self.parser.add_argument('--max', '-m', type=int, nargs='?', default=-1,
        #                          help='maximum number (default=-1)')

        # parse command line and load default logging configuration
        self.setup()

        # setup logging for the exctractor
        logging.getLogger('pyclowder').setLevel(logging.DEBUG)
        logging.getLogger('__main__').setLevel(logging.DEBUG)

    def process_message(self, connector, host, secret_key, resource, parameters):
        # Process the file and upload the results

        logger = logging.getLogger(__name__)
        logger.debug("Starting to process..")
        inputfile = resource["local_paths"][0]
        file_id = resource['id']

        # call punchcards module
        image = Image.open(inputfile)
        logger.debug("Opened image...")
        image = find_card(image)

        result = {
            'punchcardspec': "None",
            'punchcardtext': ""
        }
        if image is not None:
            card = PunchCard(image, bright=127) # using neutral gray as threshold color
            # store results as metadata
            result = {
                'punchcardspec': "IBM Model 029 Punch Card",
                'punchcardtext': card.text
            }

        metadata = self.get_metadata(result, 'file', file_id, host)
        logger.debug(metadata)

        # upload metadata
        pyclowder.files.upload_metadata(connector, host, secret_key, file_id, metadata)


if __name__ == "__main__":
    extractor = PunchCardReader()
    extractor.start()
