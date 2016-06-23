name = $(shell basename `pwd`)
localhost = $(shell ip -4 addr show eth0 | grep -Po 'inet \K[\d.]+')

container: Dockerfile entrypoint.sh *.py
	docker build -t $(name) .

run:
	docker run -t -i -e "RABBITMQ_URI=amqp://guest:guest@$(localhost)/%2f" $(name)

shell:
	docker run -t -i -e "RABBITMQ_URI=amqp://guest:guest@$(localhost)/%2f" $(name) /bin/bash

compose:
	docker run --rm -i -t --link bdextractortemplate_rabbitmq_1:rabbitmq $(name)
