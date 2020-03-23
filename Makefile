# Common docker builds
docker-build:
	(cd src && docker build -t lukaswire/onboarding-bot .)

docker-run:
	(cd src && docker run --rm -p 3000:3000 lukaswire/onboarding-bot)

docker-deploy:
	(cd src && docker push lukaswire/onboarding-bot)

# Slack run
run-slack:
	docker-compose -f docker-compose.yml -f docker-compose.slack.yml up

# Wire run
install-cli-req:
	pip install -r cli/requirements.txt

register-bot:
	python cli/cli.py --config $$(pwd)/config.json --env $$(pwd)/.env.wire.secret

start-charon:
	docker-compose -f docker-compose.yml -f docker-compose.wire.yml up -d charon

run-wire: start-charon register-bot
	docker-compose -f docker-compose.yml -f docker-compose.wire.yml up -d; \
	docker-compose -f docker-compose.yml -f docker-compose.wire.yml  logs --follow

stop-wire:
	docker-compose -f docker-compose.yml -f docker-compose.wire.yml stop