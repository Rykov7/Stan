from imp import reload

from . import config
from . import me
from . import query_log
from . import reminder
from . import report
from . import bot as bot_mod


def reload_modules():
    reload(reminder)
    reload(report)
    reload(config)
    reload(me)
    reload(query_log)
    reload(bot_mod)


