__author__ = "sunny mishra"

from database import Database
from Menu import Menu

Database.initialize()

menu = Menu()
menu.run_menu()

