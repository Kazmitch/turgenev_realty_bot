from tgbot.handlers.about_project import register_about_project
from tgbot.handlers.admin import register_admin
from tgbot.handlers.documentation import register_documentation
from tgbot.handlers.echo import register_echo
from tgbot.handlers.menu import register_menu
# from tgbot.handlers.photo_id import register_photo_id
from tgbot.handlers.purchase_terms import register_purchase_terms
from tgbot.handlers.send_contact import register_send_contact
from tgbot.handlers.show_flats import register_show_flats
from tgbot.handlers.show_photo_gallery import register_show_gallery
from tgbot.handlers.special_offers import register_show_special_offers
from tgbot.handlers.start import register_start
from tgbot.handlers.user import register_user
from tgbot.handlers.flat_selection import register_selection_flat


def register_all_handlers(dp):

    register_start(dp)
    register_menu(dp)
    register_send_contact(dp)
    register_about_project(dp)
    register_show_gallery(dp)
    register_selection_flat(dp)
    register_show_flats(dp)
    register_show_special_offers(dp)
    register_documentation(dp)
    register_purchase_terms(dp)
    # register_photo_id(dp)
    register_admin(dp)
    register_user(dp)
    # register_echo(dp)
