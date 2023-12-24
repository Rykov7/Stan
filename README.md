# Stan
Multipurpose Asynchronous Telegram Bot for Python group

### What does this project do?
 * Send links on command (chat rules, FAQs, libraries etc.)
 * Ban users and delete messages
 * Remind dates
 * Report Daily statistics (how many banned, deleted, sent messages)
 * Search for the Zen of Python quotes (inline query)
 * Help users with googling their queries
 * Make faces when doubtful bloggers are mentioned
 * Etc.

### Why is this project useful?
You can use this project as a pre-coded customizable bot.
Original (and currently working example) bot's Telegram username: @LutzPyBot

### How to deploy it?
 1. Clone repository on your linux server into `Stan` user's home directory.
 2. Create virtual environment, activate virtual environment, install required packages from `requirements.txt`.
 3. Create `.env` file in `Stan` directory with 3 variables: `LUTZPYBOT` (Bot Token), `whitelist` (White usernames, comma separated), `whiteids` (White IDs, comma separated)
 4. Install `gunicorn` and `uvicorn` package with `pip install gunicorn uvicorn`
 5. Set webhook using Python interactive shell with `bot.set_webhook()` or manually according [Telegram Bot API Documentation](https://core.telegram.org/bots/api#setwebhook).
 6. Configure nginx as a reverse proxy. Example of Nginx config:
    ```
    server {
            server_name rykov7.ru;
    
            root /home/inferno/Stan;
            index index.html index.htm index.nginx-debian.html;
    
            location / {
                    # First attempt to serve request as file, then
                    # as directory, then fall back to displaying a 404.
                    try_files $uri $uri/ =404;
            }
    
            # Stan Telegram Bot
            location /[your_bot_token_must_be_here]/ {
                    include proxy_params;
                    proxy_pass http://127.0.0.1:8813;
            }
            }
    ```
Then install certbot SSL certificate for this config.

 7. Configure the bot as a daemon:
 * Create daemon unit file in `/etc/systemd/system/stan.service` with the next content (replace `inferno` with your username):
```
[Unit]
Description=@Stan Telegram Bot
After=network.target

[Service]
User=inferno
Group=inferno
WorkingDirectory=/home/inferno/Stan
Environment="PATH=/home/inferno/Stan/venv/bin"
ExecStart=/home/inferno/Stan/.venv/bin/gunicorn -k uvicorn.workers.UvicornWorker --bind 127.0.0.1:8813 wsgi:app

[Install]
WantedBy=multi-user.target
```
*  Enable and start with `systemctl enable stan.service`, `systemctl start stan.service`.


### Where can I get more help, if I need it?
You can read [PyTelegramBotAPI documentation](url=https://github.com/eternnoir/pyTelegramBotAPI) for more usage examples.


### How do I read logs of running Stan bot?
Continuous log reading on Linux:
```# journalctl --unit=stan.service -f```


### How to interact with Stan?
Bot can receive commands and behave depending on chat situation.

Standard command pack for bot father includes:
* nobot - Telebot shouldn't be your first Python project
* nogui - GUI app shouldn't be your first Python project
* nometa - Don't ask meta questions
* neprivet - Don't hello
* bdmtss - Rim shot
* quote - Random quote
* add - Add quote
* g - Google it [Request text can be any text from replied message or arguments if there's text after `\g example`]
* rules - Chat rules
* faq - FAQ
* books - Pythonista's Library
* lutz - Send Lutz book