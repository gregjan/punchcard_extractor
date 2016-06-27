# Introduction

This README describes how to develop and test a Brown Dog extractor tool, based on the template project in this repository.
It also explains how you can contribute your new tool to the Brown Dog Tools Catalogue.
Brown Dog Extractor Tools are used to analyze files and extract metadata out of it.
For example, one existing extractor uses the OpenCV software to process photographs, finding any human faces that are in a picture.
You can find these and other extractor examples in the Brown Dog code repository.
This repository contains a template project only. You can clone this repository to your local system and build it right away.
However, until you add your custom extraction code the extractor will only report a tag of "Hello, World" for any given file.

# Brown Dog Runtime Environment

The Brown Dog environment includes several services that work together to deliver the Brown Dog API.
These include the Clowder web application, which hosts the API, a RabbitMQ message broker and extractor tools running on separate hosts.
Brown Dog extractors are message-based network services that process data files in response to RabbitMQ messages.
The client-facing Brown Dog API receives data from a client and passes messages to the extractor message topic.
Any extractors that are subscribed to the topic will receive the message and decide for themselves if they can process the data,
usually by looking at the MIME type. When an extractor starts or finishes working on a file it posts status and results back onto a message queue.
All communication between the Brown Dog servers and the extractor tools is handled by messaging.

# Step-by-Step Instructions

Following these instructions you should be able to install and run the template extractor, run tests using sample files,
and develop you own extractor program based on template extractor.

## Create Project from Template

There are some basic software dependencies to install, after which Docker will handle the rest.
Docker Compose is run from within a python virtual environment for your project.
Docker Compose will start and connect several Docker containers together to create an extractor runtime environment.
It will also deploy your own project code into a Docker container that is connected to this runtime environment.

1. Install prerequisite software. The installation methodology will depend up on your operating system:
 - VirtualBox (or an equivalent Docker-compatible virtualization environment)
 - Docker Engine (instructions specific to your operating system can be found here https://docs.docker.com/engine/installation/)
 - Docker Compose (for MAC and Windows, this is installed along with Docker Engine. For other operating systems, you might have to do additional steps.)
 - Python and PIP
 - Git

2. Clone this extractor template project from the repository, substituting your extractor project name below. 
This clones the template project into a directory with name \<project_name\>:

        $ git clone https://opensource.ncsa.illinois.edu/bitbucket/scm/bd/bd-extractor-template.git <project_name>

## Create Extractor Runtime Environment
- Install Docker Compose (if not already installed)
    
        $ pip install docker-compose
    
- Start up the extractor runtime environment using Docker Compose. This starts docker containers for Clowder, MongoDB, 
and RabbitMQ. The running container names will be of the format *\<project_name_with_only_alphabets\>\_\<container\>\_\<count\>*, 
where *\<project_name_with_only_alphabets\>* is basically the name of the folder to which the extractor template was 
cloned ( *\<project_name\>* ) with spaces, hyphens and other special characters removed, *\<container\>* is the unique 
name of the container that is provided in the docker-compose.yml file, and *\<count\>* specifies the instance number of 
the docker container. For example, the first instance of a Mongo container started from a directory *extractor-template* 
will be named *extractortemplate_mongo_1*. 

        $ docker-compose up -d
    
## Create a Clowder Account
    
- Clowder web application will be running at http://\<docker-machine-ip\>:9000 where \<docker-machine-ip\> can be found by running the following command.
This assumes that you are running a single Docker machine. If not, please choose the appropriate IP address. In Linux, \<docker-machine-ip\> is 127.0.0.1 or localhost.:
    
        $ docker-machine ip
        
    - Point your browser to the Clowder web application
    - Sign up for an account by entering an email address. Please note down the email address that you use.
    - View the logs for the Clowder container to get registration link:

            $ docker logs <project_name_with_only_alphabets>_clowder_1 | grep signup

    - Find the Clowder registration link in the log output. Point your browser at that link to complete registration, choosing a password.
    - NOTE: User registrations are stored in the MongoDB container. They will remain as long as that container is not replaced with a new one.

- Log in to Clowder web application using the username and password created in the above step 

## Build and Start Example Extractor

1. Issue a Docker build command from the project folder:

        $ docker build -t example-extractor .

This command will take longer the first time, as all dependencies are downloaded and installed into the container. 
You can run the command again and it will only perform the steps in the Dockerfile that have changed.

2. Run the Example Extractor:

        $ docker run --rm -i -t --link <project_name_with_only_alphabets>_rabbitmq_1:rabbitmq example-extractor

This command starts your extractor container and links it to the RabbitMQ container's shared ports.

## Test Example Extractor

The example extractor provided in this folder is a word count extractor that uses `wc` command to count the number of words, lines and characters in a text file. 
To test this extractor, upload a text file to Clowder web application. You will have to create a Dataset first and then upload the file into it.
After uploading the text file, you can go to the file view page and see the metadata generated by the word count extractor.

## Add Sample Input Files and Create Tests

At this point you have seen the template extractor deployed and working within your local runtime environment.
Now it's time to add your sample input files and create the custom code.
We recommend that you develop your extractor in a test-driven manner, by first adding input sample files,
then modify the test script to validate the extractor results are correct.

1. Select a few representative sample files and add them to the "sample_files" folder.
2. Edit the tests.py script to add tests for your sample files. You can remove the template example file and tests.
3. Run the new tests:

        $ ./tests.py
4. The tests will fail of course, but you can look at the output logged to the console to see why they failed.

## Stop Example Extractor
 
You can stop the example extractor by either stopping the extractor container from Docker desktop client or by pressing CTRL+C from the Docker terminal running the extractor.

## Develop Extractor Code

Now that we have sample files and failing tests, we can start to write code to make those tests pass.
You'll also presumably modify your test code too, as you learn more about your extractor output.

1. Edit extractor.py to add your data processing code in the commented areas.
2. To install your software dependencies, provide necessary instructions in Dockerfile using the RUN command. 
You will need to add a line in Dockerfile to switch to the root user (```USER root```) for getting proper permissions. 
For e.g., to install ImageMagick package using apt-get, add the following commands to Dockerfile: 
        
        USER root
        RUN apt-get update && apt-get install -y \ 
                imagemagick
PIP or other package managers can also be used to install dependencies and is the choice of the developer.
        
3. In particular, make sure you edit the MIME type filter (link to line) so that your extractor will only run on relevant input files.
4. Redeploy the code into the runtime environment by rebuilding the extractor container and running it:

        $ docker build -t example-extractor .
        $ docker run --rm -i -t --link <project_name_with_only_alphabets>_rabbitmq_1:rabbitmq example-extractor

5. Run tests.py again:

        $ ./tests.py

6. Repeat 1 - 3 until tests pass!
7. Try adding some more sample files and tests.

## Contribute the Extractor Tool to the Brown Dog Service

### JSON-LD Metadata Requirements

The Brown Dog service returns extracted metadata in the form of JSON-LD[JSON-LD](http://json-ld.org/), a JSON-based format to serialize [Linked Data](https://en.wikipedia.org/wiki/Linked_data). One important property of JSON-LD is that every value stored in the document is universally identified using a URI. In learning about JSON-LD, since JSON-LD is a concrete RDF syntax, one could start by reading about [RDF](https://www.w3.org/RDF/). But JSON-LD can also be thought of as a way of taking an existing JSON document and annotating with a @context that defines every key in the JSON document.  

For example, here is a response that includes just one extractor graph in JSON-LD:

```javascript
{
  "@context": [
    "https://clowder.ncsa.illinois.edu/clowder/contexts/metadata.jsonld",
    {
    "cat": "https://clowder.ncsa.illinois.edu/metadata#",
    "extractor_id": {
      "@id": "cat:extractor/id",
      "@type": "@id"
    },
    "user_id": {
      "@id": "cat:user/id",
      "@type": "@id"
    },
    "created_at": {
      "@id": "http://purl.org/dc/terms/created",
      "@type": "http://www.w3.org/2001/XMLSchema#dateTime"
    },
    "agent": {
      "@id": "http://www.w3.org/ns/prov#Agent"
    },
    "user": "cat:user",
    "extractor": "cat:extractor",
    "content": {
      "@id": "https://clowder.ncsa.illinois.edu/metadata#content"
    },
    "cal": "https://bd-api.ncsa.illinois.edu/dts/api/extractors/ncsa.cv.caltech101#"
  }],
  "cat:created_at": "Mon Mar 07 09:30:14 CST 2016",
  "cat:agent": {
    "@type": "cat:extractor",
    "cat:name": "ncsa.cv.caltech101",
    "@id": "https://bd-api.ncsa.illinois.edu/dts/api/extractors/ncsa.cv.caltech101"
  },
  "cat:content": {
    "cal:basic_caltech101_score": [
      "-0.813741"
    ],
    "cal:basic_caltech101_category": [
      "BACKGROUND_Google"
    ]
  }
}
```

When writing an extractor to post extracted metadata to Clowder, the document you post has to be in the following format:

```javascript
{
  "@context": ["https://clowder.ncsa.illinois.edu/contexts/metadata.jsonld", 
      {... any ...}
  ],
  "attachedTo": {"resourceType": "file", "id": parameters["${file_id}"]},
  "agent": {
      "@type": "cat:extractor",
      "extractor_id": "https://clowder.ncsa.illinois.edu/clowder/api/extractors/${extractor_id}"
  },
  "content": {... metadata specific to the extraction ...}
}
```

A context definition specific to the contents of the "content" sub-document needs to be added to the context definition, along with the content sub-document, the file_id and the extractor_id.


## Stop Docker Containers

    docker-compose stop

Or manually stop individual containers using a Docker desktop client (e.g. Kitematic).
