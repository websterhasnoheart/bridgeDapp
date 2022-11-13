import os
import sys

from dotenv import find_dotenv, load_dotenv, set_key
from pyfiglet import Figlet
from web3 import Web3

myDir = os.getcwd()
sys.path.append(myDir)
from pathlib import Path

path = Path(myDir)
a=str(path.parent.absolute())
sys.path.append(a)
from contract_action.compile_deploy import compile, deploy
from contract_action.contract_interact import get_balance


def main_menu():
    f = Figlet(font='slant')
    os.system("cls")
    print (f.renderText('Bridge'))
    print("Welcome to Bridge.dapp\n\n")
    print("choose a option")
    print("""
[1] Compile and deploy smart contract
[2] Interact with deployed smart contract
        """)
    option = input("\nYour choice: ")
    if option == '1':
        compile_deploy_menu()
    elif option == '2':
        interact_menu()
    else:
        print("Invalid input!")
        main_menu()


def compile_deploy_menu():
    dotenv_file = find_dotenv()
    load_dotenv(dotenv_file)
    f = Figlet(font='slant')
    os.system("cls")
    print (f.renderText('Bridge'))
    
    print("\n\nYou need to set up your roles and wallets first")
    print("""
[1] Input owner wallet and private key
[2] Input contractor wallet and private key
[3] Set project name and symbol
[4] Set project budget, payment frequency and times
[5] Compile and deploy the smart contract
[6] Return to the main menu
        """)
    
    option = input("\nYour choice:")
    if option == '6':
        os.system("cls")
        main_menu()
    elif option == '1':
        owner_wallet = input("Input owner wallet address: ")
        owner_wallet_private_key = input("Input wallet private key: ")

        os.environ["OWNER_WALLET"] = owner_wallet
        os.environ["OWNER_PRIVATE_KEY"] = owner_wallet_private_key

        set_key(dotenv_file, "OWNER_WALLET",  os.environ["OWNER_WALLET"])
        set_key(dotenv_file, "OWNER_PRIVATE_KEY",  os.environ["OWNER_PRIVATE_KEY"])
        
        print("Owner wallet and private key was successfully set")
        compile_deploy_menu()
    elif option == '2':
        owner_wallet = input("Input contractor wallet address: ")
        owner_wallet_private_key = input("Input wallet private key: ")

        os.environ["CONTRACTOR_WALLET"] = owner_wallet
        os.environ["CONTRACTOR_PRIVATE_KEY"] = owner_wallet_private_key

        set_key(dotenv_file, "CONTRACTOR_WALLET",  os.environ["CONTRACTOR_WALLET"])
        set_key(dotenv_file, "CONTRACTOR_PRIVATE_KEY",  os.environ["CONTRACTOR_PRIVATE_KEY"])
        
        print("Contractor wallet and private key was successfully set")
        compile_deploy_menu()
    elif option == '3':
        project_name = input("Input project name: ")
        project_symbol = input("Input project symbol: ")
        
        os.environ["PROJECT_NAME"] = project_name
        os.environ["PROJECT_SYMBOL"] = project_symbol
        
        set_key(dotenv_file, "PROJECT_NAME",  os.environ["PROJECT_NAME"])
        set_key(dotenv_file, "PROJECT_SYMBOL",  os.environ["PROJECT_SYMBOL"])
        
        print("Project Name and symbol was successfully set!")
        compile_deploy_menu()
    elif option == '4':
        project_budget = input("Input project budget: ")
        payment_frequency = input("Input payment frequency: ")
        payment_number = input("Input payment times: ")
        
        os.environ["PROJECT_BUDGET"] = project_budget
        os.environ["PAYMENT_FREQUENCY"] = payment_frequency
        os.environ["PAYMENT_NUMBER"] = payment_number
        
        set_key(dotenv_file, "PROJECT_BUDGET",  os.environ["PROJECT_BUDGET"])
        set_key(dotenv_file, "PAYMENT_FREQUENCY",  os.environ["PAYMENT_FREQUENCY"])
        set_key(dotenv_file, "PAYMENT_NUMBER",  os.environ["PAYMENT_NUMBER"])

        print("Project budget, payment frequency and times are all successfully set")
        compile_deploy_menu()
    elif option == '5':
        compile()
        deploy()
        return_to_main = input("Press ENTER to return to main menu")
        if return_to_main == '':
            main_menu()
        
def interact_menu():
    dotenv_file = find_dotenv()
    load_dotenv(dotenv_file)
    contract_address = os.getenv("CONTRACT_ADDRESS")
    f = Figlet(font='slant')
    os.system("cls")
    print (f.renderText('Bridge'))
    
    print(f"\n\nThe contract you are trying to interact is {contract_address}")
    print("Choose a command to execute with smart contract:")
    print("""
[1] Deposit funds
[2] Display balance
[3] Transfer
[4] Withdrawl
[5] Terminate the project
[6] Release progress payment (contractor only)
[7] Return to the main menu
        """)
    option = input("\nYour choice: ")
    if option == '7':
        main_menu()
    elif option == '2':
        get_balance()