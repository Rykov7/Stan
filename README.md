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

### How do I get started?
Clone repository, edit code if needed and deploy on your sever.

### Where can I get more help, if I need it?
Bot is easily understandable reading in-code comments of the handler functions, also read [PyTelegramBotAPI documentation](url=https://github.com/eternnoir/pyTelegramBotAPI) for library help.


### How do I read logs of running Lutz bot daemon?
Continuous log reading on Linux:

```# journalctl --unit=lutz.service -f --no-pager```


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