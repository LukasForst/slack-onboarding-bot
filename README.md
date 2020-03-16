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

To run inside docker-compose environment, one must create `.env` file with following variables.
```bash
# secret for slack
SLACK_SIGNING_SECRET= 
# obtained either from slack, or from Roman
SLACK_BOT_TOKEN= 
# from slack
BOT_TOKEN= 
```

Then just simply run:
- to connect to Wire
```bash
make run-wire
```
- to connect to Slack
```bash
make run-slack
```