# Lutz Bot
Multipurpose Telegram Bot for Python group

### What does this project do?
 * Send links on command (chat rules, FAQs, libraries etc.)
 * Ban users and delete messages
 * Filter links
 * Remind dates
 * Daily statistics publication (how many banned, deleted, sent messages)
 * Search for the Zen of Python quotes (inline query)
 * Help users with googling their queries
 * Make faces when doubtful bloggers are mentioned
 * Etc. (functionality is growing up)

### Why is this project useful?
You can use this project as a pre-coded customizable bot.
Original (and currently working) bot Telegram username: @LutzPyBot

### How to deploy it?
 1. Clone repository on your linux server into `lutzpybot` user's home directory.
 2. Create virtual environment, activate virtual environment, install required packages from `requirements.txt`.
 3. Create `.env` file in `lutzbot` directory with 3 variables: `LUTZPYBOT` (Bot Token), `whitelist` (White usernames, comma separated), `whiteids` (White IDs, comma separated)
 4. Install `gunicorn` package additionally with `pip install gunicorn`
 5. Set webhook using Python interactive shell with `bot.set_webhook()` or manually according [Telegram Bot API Documentation](https://core.telegram.org/bots/api#setwebhook).
 6. Configure nginx as a reverse proxy.
 7. Configure the bot as a daemon.

### How to configure bot as a daemon?
1. Create daemon unit file in `/etc/systemd/system/lutz.service` with the content (replace `inferno` with your username):
```
[Unit]
Description=@Lutz Telegram Bot
After=network.target

[Service]
User=inferno
Group=inferno
WorkingDirectory=/home/inferno/lutzpybot
Environment="PATH=/home/inferno/lutzpybot/venv/bin"
ExecStart=/bin/bash -c 'source /home/inferno/lutzpybot/venv/bin/activate; gunicorn --bind unix:/tmp/lutz.sock wsgi:app' #Restart=on-failure

[Install]
WantedBy=multi-user.target
```
2. Enable and start with `systemctl enable lutz.service`, `systemctl enable lutz.service`.

### Where can I get more help, if I need it?
Bot is easily understandable reading in-code comments of the handler functions, additionally read [PyTelegramBotAPI documentation](url=https://github.com/eternnoir/pyTelegramBotAPI) for library help.


### How do I read logs of running Lutz bot daemon?
Continuous log reading on Linux:

```# journalctl --unit=lutz.service -f```


### Hot to interact with Lutz bot?
Bot can recieve commands and behave depending on chat situation.

Standard command pack for bot father includes:
* nobot - Telebot shouldn't be your first Python project
* nogui - GUI app shouldn't be your first Python project
* nometa - Don't ask meta questions
* neprivet - Don't hello
* bdmtss - Rimshot
* quote - Random quote
* add - Add quote
* g - Google it [Request text can be any text from replied message or arguments if there's text after `\g example`]
* rules - Chat rules
* faq - FAQ
* books - Pythonista's Library
* lutz - Send Lutz book