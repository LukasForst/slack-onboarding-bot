# Slack on boarding bot
Slightly modified official onboarding bot from the official [Slack tutorial](https://github.com/slackapi/python-slackclient/tree/master/tutorial).
The only modification was, that the `BASE_URL` aka URL of the Slack backend is now being 
loaded from the environment.

Diff between this `app.py` and the one from the [official repo](https://github.com/slackapi/python-slackclient)
```bash
» diff -n python-slackclient/tutorial/PythOnBoardingBot/app.py slack-onboarding-bot/src/app.py
15c15
< slack_web_client = WebClient(base_url=os.environ['BACKEND'], token=os.environ['SLACK_BOT_TOKEN'])
---
> slack_web_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])
```

## Targeting Slack Api

To run inside docker-compose environment targeting Slack backend, 
one must create `.env.slack.secret` file with following variables.
```bash
SLACK_SIGNING_SECRET=
SLACK_BOT_TOKEN=
```
How to obtain these values from Slack is specified in the [official guide](https://github.com/slackapi/python-slackclient/blob/master/tutorial/04-running-the-app.md).

To start the bot simply run.
```bash
make run-slack
```

## Targeting Wire API
Preparation:
* Register your bot in Roman
* Start the bot and Charon
```bash
make run-wire
```
* Register bot in Charon - use endpoint registration using Swagger UI
