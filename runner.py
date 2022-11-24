from interface.menu import main_menu, login_menu
from dotenv import find_dotenv, load_dotenv
import os

if __name__ == '__main__':
    dotenv_file = find_dotenv()
    load_dotenv(dotenv_file)
    logined = os.getenv("LOGINED")
    if logined == "true":
        login_menu()
    else:
        main_menu()