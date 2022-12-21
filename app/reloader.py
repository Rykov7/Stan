from importlib import reload

from . import bot
from . import filters
from . import config
from . import me
from . import report
from . import stan


def reload_modules():
    reload(bot)
    reload(filters)
    reload(config)
    reload(me)
    reload(report)
    reload(stan)
