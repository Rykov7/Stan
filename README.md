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