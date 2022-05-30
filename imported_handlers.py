from tgbot.handlers.admin import register_admin
from tgbot.handlers.echo import register_echo
from tgbot.handlers.start import register_start
from tgbot.handlers.user import register_user
from tgbot.handlers.flat_selection import register_selection_flat


def register_all_handlers(dp):

    register_start(dp)
    register_selection_flat(dp)
    register_admin(dp)
    register_user(dp)
    register_echo(dp)
