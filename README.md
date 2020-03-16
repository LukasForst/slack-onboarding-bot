# Slack on boarding bot
Slightly modified official onboarding bot from the official [Slack tutorial](https://github.com/slackapi/python-slackclient/tree/master/tutorial).
The only modification was, that the `BASE_URL` aka URL of the Slack backend is now being 
loaded from the environment.

Diff between this `app.py` and the one from the [official repo](https://github.com/slackapi/python-slackclient)
```bash
» diff -n python-slackclient/tutorial/PythOnBoardingBot/app.py PythOnBoardingBot/app.py                                                                                                                                                         1 ↵ lukas@Mefisto
a4 1
from slack.web.base_client import BaseClient
a20 2
BaseClient.BASE_URL = os.environ['BASE_URL']

```

Environment variables:
- `SLACK_SIGNING_SECRET` - obtain from the Slack account if running in Slack 
- `SLACK_BOT_TOKEN` - obtain from the Slack account if running in Slack
- `BASE_URL` - URL of the backend, can be either [Charon](https://github.com/wireapp/charon)
or Slack = `https://www.slack.com/api/`
