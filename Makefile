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
	@./scripts/run.sh

.PHONY: shell
shell:
	@docker exec -ti mousehunt_bot bash

.PHONY: stop
stop:
	@docker kill mousehunt_bot
