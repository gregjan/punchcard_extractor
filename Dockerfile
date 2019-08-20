FROM clowder/pyclowder:2
MAINTAINER Greg Jansen <jansen@umd.edu>

# Setup environment variables. These are passed into the container. You can change
# these to your setup. If RABBITMQ_URI is not set, it will try and use the rabbitmq
# server that is linked into the container. MAIN_SCRIPT is set to the script to be
# executed by entrypoint.sh. REGISTRATION_ENDPOINTS should point to a central clowder
# instance, for example it could be https://clowder.ncsa.illinois.edu/clowder/api/extractors?key=secretKey

ENV RABBITMQ_URI="" \
    RABBITMQ_EXCHANGE="clowder" \
    RABBITMQ_QUEUE="umd.punchcard" \
    REGISTRATION_ENDPOINTS="https://clowder.ncsa.illinois.edu/extractors" \
    MAIN_SCRIPT="readcard.py"

# Install any programs needed
RUN apt-get update && apt-get -y install vim nano git netcat python-pip
RUN pip install numpy==1.16.4 Pillow punchcards docopt

# command to run when starting docker
COPY entrypoint.sh *.py extractor_info.json /home/clowder/
ENTRYPOINT ["/home/clowder/entrypoint.sh"]
CMD ["extractor"]
