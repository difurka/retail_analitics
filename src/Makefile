all: start

prepare_data:
	bash ./prepare_data.sh

start: prepare_data
	docker-compose up -d

stop:
	docker-compose down

rebuild: prepare_data
	docker-compose up --build

clean:
	rm -rf db
	rm -rf logs
	rm -rf export
	rm -rf backend

clean_restart: prepare_data
	rm -rf db
	docker-compose down
	docker-compose up -d --build
