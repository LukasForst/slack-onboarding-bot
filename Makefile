docker-build:
	(cd src && docker build -t lukaswire/onboarding-bot .)

docker-run:
	(cd src && docker run --rm -p 3000:3000 lukaswire/onboarding-bot)

docker-deploy:
	(cd src && docker push lukaswire/onboarding-bot)

run-slack:
	docker-compose -f docker-compose.yml -f docker-compose.slack.yml up

run-wire:
	docker-compose -f docker-compose.yml -f docker-compose.wire.yml up
