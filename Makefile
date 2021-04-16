build:
	@echo "Build patroni docker container image"
	@docker-compose build -q
start:
	@echo "Start cluster"
	@docker-compose up -d --remove-orphans

stop:
	@echo "Stop cluster"
	@docker-compose stop

destroy:
	@echo "Destroy cluster"
	@docker-compose stop && docker-compose rm -f

recreate:
	@echo "Destroy and recreate cluster"
	@docker-compose stop && docker-compose rm -f && docker-compose up -d --remove-orphans

status:
	@echo "------------------------------ Docker status ------------------------------"
	@docker-compose ps 
	@printf "\n------------------------------ Consul status ------------------------------\n"
	@docker-compose exec patroni01 consul members 2>/dev/null
	@printf "\n------------------------------ Patroni status -----------------------------\n"
	@docker-compose exec patroni01 patronictl -c /etc/patroni/postgres.yml list 2>/dev/null
