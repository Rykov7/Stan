from importlib import reload

from . import config
from . import me
from . import reminder
from . import report
from . import bot as bot_mod


def reload_modules():
    reload(report)
    reload(config)
    reload(me)
    reload(bot_mod)
