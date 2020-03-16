docker-build:
	docker build -t lukaswire/onboarding-bot src

docker-run:
	docker run --rm -p 3000:3000 lukaswire/onboarding-bot

docker-deploy:
	docker push lukaswire/onboarding-bot

run-slack:
	BASE_URL=https://www.slack.com/api/ python3 app.py
