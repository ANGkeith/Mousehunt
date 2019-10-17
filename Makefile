help:
	@echo "    init"
	@echo "        initialize configurations"
	@echo "    build"
	@echo "        build the docker image"
	@echo "    run"
	@echo "        run the docker image"
	@echo "    shell"
	@echo "        ssh into a container"

.PHONY: init
init:
	@./scripts/init.sh

.PHONY: build
build:
	@docker build . \
		--shm-size 6g \
		-t mousehunt

.PHONY: run
run:
	@docker build . \
		--shm-size 6g \
		-t mousehunt
	@xhost +local:${USER}
	@docker run -it \
		--rm \
		--name mousehunt_bot \
		--shm-size 6g \
		--net host \
		-v /tmp/.X11-unix:/tmp/.X11-unix \
		-e DISPLAY=unix${DISPLAY} \
		--device /dev/snd \
		--env-file .env \
		mousehunt

.PHONY: shell
shell:
	@docker exec -ti mousehunt_bot bash


.PHONY: stop
stop:
	@docker kill mousehunt_bot
