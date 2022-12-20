from importlib import reload

from . import bot as bot_mod
from . import check
from . import config
from . import me
from . import report
from . import stan


def reload_modules():
    reload(bot_mod)
    reload(check)
    reload(config)
    reload(me)
    reload(report)
    reload(stan)
