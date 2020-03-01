from consolemenu import *
from consolemenu.format import *
from consolemenu.items import *
from database.model import SyncPlayers
import os

def add_player(db):

    player = input("Player IGN: ")
    shard = input("Shard: ")

    confirmation = input("\nYou entered {0} ({1}), is that correct? [Y/N]: ".format(player, shard))

    if confirmation == 'Y':
        sess = db.Session()
        p = SyncPlayers(player_ign=player, shard=shard)
        sess.add(p)
        sess.commit()
        sess.close()
    elif input("Would you like to try again? [Y/N]: ") == "Y":
        add_player(db)

    input("Press Enter to return to the menu")

    return

def list_players(db):
    sess = db.Session()

    for p in sess.query(SyncPlayers).all():
        print(p.player_ign, p.shard)

    input("\nPress Enter to return to the menu")

    return

def cli(db):

    # Menu formatting
    menu_format = MenuFormatBuilder().set_border_style_type(MenuBorderStyleType.HEAVY_BORDER) \
        .set_prompt("SELECT>") \
        .set_title_align('center') \
        .set_subtitle_align('center') \
        .set_left_margin(4) \
        .set_right_margin(4) \
        .show_header_bottom_border(True)

    # Main Menu
    main_menu = ConsoleMenu(
        "PUBG API Sync - Configuration Menu",
        prologue_text="Use this tool to perform basic administrative tasks for the database, including player management.",
        formatter=menu_format
    )

    # Player Management Menu
    pm_menu = ConsoleMenu(
        'Player Management Tools',
        prologue_text="Use these options to view, enter or delete the players that the API is syncing, along with their shards.",
        formatter=menu_format
    )

    add_player_itm  = FunctionItem("Add new player", add_player, [db])
    pm_menu.append_item(add_player_itm)

    list_players_itm = FunctionItem("List existing players", list_players, [db])
    pm_menu.append_item(list_players_itm)

    pm_menu_item = SubmenuItem("Player Management", submenu=pm_menu)

    pm_menu_item.set_menu(main_menu)

    # Configure everything
    main_menu.append_item(pm_menu_item)

    main_menu.start()
    main_menu.join()