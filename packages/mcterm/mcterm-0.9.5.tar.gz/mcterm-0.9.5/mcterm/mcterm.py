"""
Author: Jess Williams
Email: devel@inuxnet.org
Description: Better Minecraft Remote Console with auto complete.
"""
from mcrcon import MCRconException, MCRcon as mc
import webbrowser
import argparse
from prompt_toolkit import prompt
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, WordCompleter
from prompt_toolkit.history import InMemoryHistory
from getpass import getpass
import sys
import os
import sqlite3
import requests
import sysconfig


# Globals
A_OK = 0
INVALID_CONNECTION = 1
INVALID_DATABASE = 2
CANNOT_WRITE = 3
INVALID_PORT = 4
global db_path, current_dir
current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
package_dir = os.path.join(current_dir,'mcterm')
db_path = os.getenv('MCTERM_DB', os.path.join(package_dir,'commands.db'))


def restore_database(db_path):
    """
    Restores the Database if it is unavailable
    :param db_path: <class 'str'>
    """
    global current_dir
    print(f"Attempting to initialize SQLite database...")
    sql_dump = None
    if os.path.isfile(os.path.join(current_dir,'commands.sql')):
        with open(os.path.join(current_dir,'commands.sql')) as f:
            sql_dump = f.read()
    else:
        request = requests.get("https://newgit.inuxnet.org/devel/bettermcrcon/-/raw/master/mcterm/commands.sql?ref_type=heads")
        if request.status_code == 200:
            sql_dump = request.text
    if sql_dump != None:
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            print(f"Restoring SQLite database to {db_path}...")
            conn = sqlite3.connect(db_path)
            conn.executescript(sql_dump)
            conn.close()
            print("Database restored successfully.")
        except Exception as e:
            print(f"Invalid permissions or read only. Error: {e}", file=sys.stderr)
            sys.exit(CANNOT_WRITE)
    else:
        print("Unable to initialize the database, exiting...", file=sys.stderr)
        sys.exit(INVALID_DATABASE)


def set_environment_variable(var_name, value):
    """
    Sets the environment variable for the database path
    :param var_name: <class 'str'>
    :param value: <class 'str'>
    """
    env_var = os.getenv('MCTERM_DB', 'None')
    if env_var == 'None':
        print(f"Setting persistent environment variable: {var_name}={value}")
        if os.name == "nt":  # Windows
            # Use PowerShell to set a system environment variable
            os.system(f'[Environment]::SetEnvironmentVariable("{var_name}", "{value}", "User")')
        else:  # Unix/Linux/MacOS
            # Update the shell configuration file
            home_dir = os.path.expanduser("~")
            shell_config = os.path.join(home_dir, ".bashrc")  # Use .zshrc or equivalent if needed
            with open(shell_config, "a") as file:
                file.write(f'\nexport {var_name}="{value}"\n')
            print(f"Environment variable added to {shell_config}.")


def get_ids(dbcon, table, column):
    """
    Returns a list of ids for table
    :param dbcon: <class 'sqlite3.Connection'>
    :param table: <class 'str'>
    :param column: <class 'str'>
    :return: <class 'list'>
    """
    cursor = dbcon.cursor()
    cursor.execute(f"SELECT {column} from {table} ORDER BY {column}")
    result = cursor.fetchall()
    elements = [row[0] for row in result]
    return elements


def get_players(mccon):
    """
    Returns a list of players
    :param dbcon: <class 'mcrcon.MCRcon'>
    :return: <class 'list'>
    """
    output = mccon.command('list')
    targets = [ x.strip() for x in output.split(':')[-1].split(',') ]
    return targets


def get_arguments(dbcon, mccon, command, tokens, token_index):
    """
    Returns a list of arguments
    :param dbcon: <class 'sqlite3.Connection'>
    :param mccon: <class 'mcrcon.MCRcon'>
    :param command: <class 'str'>
    :param tokens: <class 'str'>
    :param token_index: <class 'int'>
    :return: <class 'list'>
    """
    cursor = dbcon.cursor()
    query = "SELECT arguments from commands WHERE command = ?"
    cursor.execute(query, (command,))
    result = cursor.fetchall()
    arguments = []
    if len(result) > 0:
        parameter = [ param[0] for param in result ]
        parameters = parameter[0].split('|')
        token_list = tokens.split(' ')
        if token_list[-1] == 'structure':
            return get_ids(dbcon,'structures','id')
        elif token_list[-1] == 'biome':
            return get_ids(dbcon,'biomes','id')
        elif token_list[-1] == 'biome':
            return get_ids(dbcon,'poi','poi')
        if len(parameters) > token_index:
            for argument in parameters[token_index].split(','):
                if argument.find('<target') >= 0 or argument.find('<player') >= 0:
                    arguments += get_players(mccon)
                elif argument.find('<gamemode') >= 0:
                    arguments += get_ids(dbcon,'gamemode','gamemode')
                elif argument.find('<enchantment') >= 0:
                    arguments += get_ids(dbcon,'enchantment','id')
                elif argument.find('<effect') >= 0:
                    arguments += get_ids(dbcon,'effect','name')
                elif argument.find('<block') >= 0 or argument.find('<item') >= 0:
                    arguments += get_ids(dbcon,'items','item_id')
                elif argument.find('<biome') >= 0:
                    arguments += get_ids(dbcon,'biomes','id')
                elif argument.find('<structure') >= 0:
                    arguments += get_ids(dbcon,'structures','id')
                elif argument.find('<poi') >= 0:
                    arguments += get_ids(dbcon,'poi','poi')
                elif argument.find('<entity') >= 0:
                    arguments += get_ids(dbcon,'entities','entity_id')
                elif argument.find('<advancement') >= 0:
                    arguments += get_ids(dbcon,'advancements','id')
                elif argument.find('<attribute') >= 0:
                    arguments += get_ids(dbcon,'attributes','id')
                elif argument.find('<particle') >= 0:
                    arguments += get_ids(dbcon,'particles','particle')
                else:
                    arguments.append(argument)
    return arguments


def get_matches(words, tokens):
    """
    Returns a list of arguments that match
    :param words: <class 'list'>
    :param tokens: <class 'list'>
    :return: <class 'list'>
    """
    output = []
    current_text = tokens[-1]
    for word in words:
        if word.find(current_text) == 0:
            output.append(word)
    return output


class TokenCompleter(Completer):

    def __init__(self, con, dbcon):
        """
        Constructor for TokenCompleter
        :param con: <class 'mcrcon.MCRcon'>
        :param dbcon: <class 'sqlite3.Connection'>
        """
        self.__con = con
        self.__dbcon = dbcon

    def get_completions(self, document, complete_event):
        """
        Word Comlpleter and Yielder for TokenCompleter
        """
        current_text = document.text_before_cursor.lstrip()
        word = document.get_word_before_cursor()
        tokens = current_text.split(' ')
        if len(tokens) == 1 or (len(tokens) == 2 and tokens[0] == '?') or (len(tokens) == 2 and tokens[0] == 'help'):
            words = get_ids(self.__dbcon,'commands','command')
            words = get_matches(words,tokens)
            yield from WordCompleter(words,WORD=True).get_completions(document, complete_event)
        else:
            words = get_arguments(self.__dbcon, self.__con, tokens[0], ' '.join(tokens).strip(), len(tokens) - 2)
            words = get_matches(words,tokens)
            yield from WordCompleter(words,WORD=True).get_completions(document, complete_event)


class BetterMCRConsole:

    def __init__(self, con, prompt):
        """
        Constructor for Better Minecraft Remote Console
        :param con: <class 'mcrcon.MCRcon'>
        :param prompt: <class 'str'>
        """
        global db_path
        if not os.path.exists(db_path):
            install_dir = os.path.join(sysconfig.get_path('purelib'), "mcterm")
            if os.path.exists(os.path.join(install_dir,'commands.db')):
                db_path = os.path.join(install_dir,'commands.db')
            else:
                print(f"Cannot find database in '{db_path}'", file=sys.stderr)
                restore_database(db_path)
        if not isinstance(con, mc):
            print("'con' is not Type <class 'mcrcon.MCRcon'>", file=sys.stderr)
            sys.exit(INVALID_CONNECTION)
        self.__prompt = prompt
        self.__dbcon = sqlite3.connect(db_path)
        self.__validate_db()
        self.__commands = []
        self.__init_commands()
        self.__con = con
        self.__completer = TokenCompleter(self.__con, self.__dbcon)
        self.__history = InMemoryHistory()
        self.__session = PromptSession(history=self.__history)

    def __del__(self):
        """
        Destructor
        """
        if self.__dbcon:
            self.__dbcon.close()
            print("Database connection closed.")

    def __validate_db(self):
        """
        Validate Database
        """
        cursor = self.__dbcon.cursor()

        tables = {'commands':['command','description'],'attributes': ['id'],'effect': ['name'],
                  'gamemode': ['gamemode'],'biomes':['id'],'particles':['particle'],
                  'items':['item_id'],'poi':['poi'],'structures':['id'],'entities':['entity_id'],
                  'enchantment':['id'],'advancements':['id']}
        for command in tables.keys():
            # Validate commands table
            cursor.execute(f"PRAGMA table_info({command})")
            result = cursor.fetchall()

            if not result:
                print(f"Table '{command}' does not exist. The Database is invalid.", file=sys.stderr)
                sys.exit(INVALID_DATABASE)
            else:
                columns = [ col[1] for col in result ]
                for column in tables[command]:
                    if column not in columns:
                        print(f"Required Column '{column}' does not exist in Table '{command}'. The Database is invalid.", file=sys.stderr)
                        sys.exit(INVALID_DATABASE)
        print("Database is valid.")

    def __init_commands(self):
        """
        Initialize Commands List
        """
        self.__commands = get_ids(self.__dbcon,'commands','command')

    def __get_description(self, cmd):
        """
        Returns the description or url of the command
        :param cmd: <class 'str'>
        :return: <class 'str'>
        """
        cursor = self.__dbcon.cursor()
        cursor.execute("SELECT description from commands WHERE command = ?", (cmd,))
        result = cursor.fetchone()
        return str(result[0]).replace('~','\n')

    def run(self):
        """
        Execute
        """
        while True:
            try:
                user_input = prompt(self.__prompt, completer=self.__completer, history=self.__history)
                self.handle_input(user_input)
            except KeyboardInterrupt:
                # Handle Ctrl+C
                continue
            except EOFError:
                # Handle Ctrl+D or Ctrl+Z
                print("\nExiting the console.")
                sys.exit(A_OK)

    def handle_input(self, user_input):
        """
        Event to handle the input
        """
        if not user_input.strip() == "":
            command = user_input.strip().split()[0]
            if command.lower() == 'exit' or user_input.lower() == 'quit':
                print("Exiting the console.")
                self.__con.disconnect()
                sys.exit(A_OK)
            elif command == '?':
                cmd = user_input.split()[1]
                description = self.__get_description(cmd)
                if description.find("https://") >= 0:
                    webbrowser.open_new_tab(description)
                else:
                    print(description)
            elif command in self.__commands:
                output = self.__con.command(user_input)
                print(output)
            else:
                print("Unknown command. Type 'exit' or 'quit' to exit console.")


def main():
    """
    Main Entry Point
    """
    parser = argparse.ArgumentParser(description='Better Minecraft Remote Console')
    parser.add_argument('--host', type=str, help='Remote server host')
    parser.add_argument('--port', type=int, help='Port number of the server')
    parser.add_argument('--password', type=str, help='Password for server')
    parser.add_argument('--prompt', type=str, help='Custom Prompt (Defaults "<host>:<port> >>>")')
    args = parser.parse_args()
    if not args.host:
        args.host = input("Server Hostname or IP: ")
    if not args.port:
        valid = False
        while not valid:
            try:
                args.port = int(input("Server Port: "))
                valid = True
            except Exception as e:
                print("Port must be an integer")
    if args.port < 0 or args.port > 65535:
        print(f"Port '{args.port}' is not in valid range (0-65535)", file=sys.stderr)
        sys.exit(INVALID_PORT)
    if not args.password:
        args.password = getpass("Enter Password: ")
    if not args.prompt:
        args.prompt = f'{args.host}:{args.port} >>> ' 
    con = mc(host=args.host,password=args.password,port=args.port)
    try:
        con.connect()
        console = BetterMCRConsole(con, args.prompt)
        console.run()
    except MCRconException as e:
        print("Invalid server IP, credentials, or port", file=sys.stderr)
        sys.exit(INVALID_CONNECTION)


if __name__ == '__main__':
    main()
