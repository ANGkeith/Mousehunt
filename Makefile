help:
	@echo "    post_init"
	@echo "        generate .env file. Insert your credentials here"
	@echo "    init"
	@echo "        initialize docker-compose and .env_<username> files"
	@echo "    build"
	@echo "        build the docker image"
	@echo "    run"
	@echo "        run the docker image"
	@echo "    dailies"
	@echo "        instruct all containers to start sending raffles and daily gifts"
	@echo "    delete_notifications"
	@echo "        instruct all containers to clear raffle tickets notifications"
	@echo "    collect_dailies"
	@echo "        instruct all containers to accept gift of the day"

.PHONY: post_init
post_init:
	@./scripts/post_init.sh

.PHONY: init
init:
	@./scripts/generate_config.sh

.PHONY: build
build:
	@docker build . \
		--shm-size 6g \
		-t mousehunt

.PHONY: run
run:
	@./scripts/run.sh

.PHONY: dailies
dailies:
	@./scripts/find_and_replace.sh dailies
	
.PHONY: delete_notifications
delete_notifications:
	@./scripts/find_and_replace.sh delete_raffle_tickets

.PHONY: collect_dailies
collect_dailies:
	@./scripts/find_and_replace.sh collect_dailies
