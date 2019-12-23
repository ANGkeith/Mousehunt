help:
	@echo "    post_init"
	@echo "        generate .env file. Insert your credentials here"
	@echo "    "
	@echo "    init"
	@echo "        initialize docker-compose and .env_<username> files"
	@echo "    "
	@echo "    build"
	@echo "        build the docker image"
	@echo "    "
	@echo "    run"
	@echo "        run the docker image"
	@echo "    "
	@echo "    dailies"
	@echo "        instruct all containers to start sending raffles and daily gifts"
	@echo "    "
	@echo "    delete_notifications"
	@echo "        instruct all containers to clear raffle tickets notifications"
	@echo "    "
	@echo "    collect_dailies"
	@echo "        instruct all containers to accept gift of the day"
	@echo "    "
	@echo "    afk_mode"
	@echo "        when there is king's reward, will refresh and wait for fix"
	@echo "    "
	@echo "    refresh"
	@echo "        will force a refresh"
	@echo "    gui"
	@echo "        launch a firefox session for each image"

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

.PHONY: afk_mode
afk_mode:
	@./scripts/find_and_replace.sh afk_mode

.PHONY: refresh
refresh:
	@./scripts/find_and_replace.sh refresh

.PHONY: gui
gui:
	@./scripts/launch_browser.sh
