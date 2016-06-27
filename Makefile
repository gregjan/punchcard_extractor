name = $(shell basename `pwd`)
repo = ncsa
localhost = $(shell ip -4 addr show eth0 | grep -Po 'inet \K[\d.]+')

container: Dockerfile entrypoint.sh *.py
	docker build -t $(name) .

push:
	docker tag -f $(name) $(repo)/$(name)
	docker push $(repo)/$(name):latest

run:
	docker run -t -i -e "RABBITMQ_URI=amqp://guest:guest@$(localhost)/%2f" $(name)

shell:
	docker run -t -i -e "RABBITMQ_URI=amqp://guest:guest@$(localhost)/%2f" $(name) /bin/bash

compose:
	docker run --rm -i -t --link bdextractortemplate_rabbitmq_1:rabbitmq $(name)