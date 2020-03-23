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
It is a bit more tricky, but this is why the CLI is here for you.

#### Requirements
* python >= 3.6
* pip
* pip dependencies installed - to do that execute
```bash
make install-cli-req
```
* Roman account - to create roman account please execute following bash line and then check your mail.
```bash
python cli/roman.py --email your@mail.com --password arbitraryPassword --name 'Name of your amazing service'
```

#### Configuration
One must create `config.json` in the project root and fill the following template.
```json
{
  "email": "your@mail.com",
  "password": "arbitraryPassword",
  "service_name": "Name of your amazing service",
  "service_url": "<Charon URL>/roman/messages"
}
```
This configuration is then used for the bot registration in the Roman and in the Charon.

### Run Bot 
To start the bot up, please execute:
```bash
make run-wire
```

What it does:
1) Starts up Charon (running as Wire Proxy to Slack Bot) and Redis (for persistence)
1) Registers bot in Roman and Charon
    1) Uses provided `config.json` and registers the bot in Roman - if the `service_url` does not match, it updates it.
    1) Generates secret (`SLACK_SIGNING_SECRET`, `SLACK_BOT_TOKEN`) for the Slack Bot and writes that to the `.env.wire.secret`
    which is then used when the `docker-compose` starts up the bot
    1) Registers Slack Bot in the Charon
1) Starts the Slack Bot up in detached mode
1) Opens `docker-compose logs --follow`  

#### Extended configuration
If you want to manage where is every component running or set any additional configuration,
please specify that in the `config.json`:
```json
{
  "bot_summary": "Description of your bot.",
  "roman_url": "http://proxy.services.zinfra.io",
  "charon_url": "http://localhost:8080",
  "bot_url": "http://bot:3000/slack/events"
}
```
