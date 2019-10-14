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
	@docker build . -t mousehunt

.PHONY: run
run:
	@xhost +local:${USER}
	@docker run -d \
		--rm \
		--name mousehunt_bot \
		--shm-size 6g \
		--net host \
		-v /tmp/.X11-unix:/tmp/.X11-unix \
		-e DISPLAY=unix${DISPLAY} \
		--env-file .env \
		mousehunt

.PHONY: shell
shell:
	@docker exec -ti mousehunt_bot bash
