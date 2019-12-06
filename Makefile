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
	@echo "        instruct all containers to clear raffle tickets notifications
	

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
	@./scripts/dailies.sh

.PHONY: delete_notifications
delete_notifications:
	@./scripts/delete_notifications.sh

.PHONY: stop
stop:
	@docker kill mousehunt_bot
