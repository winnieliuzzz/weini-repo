import database
from menu import Menu


database.Database.initialize()
menu = Menu()
menu.run_menu()