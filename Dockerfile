# FROM clowder/python-base
FROM ncsa/clowder-extractors-python-base
MAINTAINER Sandeep Satheesan <sandeeps@illinois.edu>

# Setup environment variables. These are passed into the container. You can change
# these to your setup. If RABBITMQ_URI is not set, it will try and use the rabbitmq
# server that is linked into the container. MAIN_SCRIPT is set to the script to be
# executed by entrypoint.sh

ENV RABBITMQ_URI="" \
    RABBITMQ_EXCHANGE="clowder" \
    RABBITMQ_VHOST="%2F" \
    RABBITMQ_QUEUE="wordCount" \
    MAIN_SCRIPT="wordcount.py"

# Switch to clowder, copy files and be ready to run
USER clowder

# command to run when starting docker
COPY entrypoint.sh *.py /home/clowder/
ENTRYPOINT ["/home/clowder/entrypoint.sh"]
CMD ["extractor"]