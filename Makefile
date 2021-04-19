build:
	@echo "Pull and build container images. This make take some time when running for first time."
	@docker-compose build
start:
	@echo "Start cluster"
	@docker-compose up -d --remove-orphans

stop:
	@echo "Stop cluster"
	@docker-compose stop

destroy:
	@echo "Force destroy cluster"
	@docker-compose down --remove-orphans

recreate:
	@echo "Destroy and recreate cluster"
	@docker-compose stop && docker-compose rm -f && docker-compose up -d --remove-orphans

status:
	@echo "============================== Docker status =============================="
	@docker-compose ps 
	@printf "\n============================== Consul status ==============================\n"
	@docker-compose exec consul01 consul members 2>/dev/null
	@printf "\n============================== Patroni status =============================\n"
	@docker-compose exec patroni01 patronictl -c /etc/patroni/postgres.yml list 2>/dev/null

switchover:
	@echo "Force patroni switchover to another node"
	@docker-compose exec patroni01 patronictl -c /etc/patroni/postgres.yml switchover --force

applogs:
	@docker-compose logs -f application01 application02
