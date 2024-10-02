# cli application

import sys
import os
import shutil
import subprocess
from colorama import Fore, Style
import winshell
from win32com.client import Dispatch
from difflib import get_close_matches

class CliDow:
    def __init__(self, args):
        self.args = args
        self.apps_dir = os.path.expanduser("~/cli_apps")
        self.applications = self.get_applications()
        self.cliBuild(self.applications)

    def cliBuild(self, applications):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            terminal_width = shutil.get_terminal_size().columns
            max_columns = max(1, terminal_width // 34)
            total_apps = len(applications)
            max_rows = (total_apps + max_columns - 1) // max_columns
            rows = min(max_rows, (total_apps + max_columns - 1) // max_columns)

            color_map = {chr(i): color for i, color in zip(range(65, 91), [Fore.RED, Fore.GREEN, Fore.WHITE, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE] * 4)}

            for row in range(rows):
                line = ""
                for col in range(max_columns):
                    index = row * max_columns + col
                    if index < total_apps:
                        app = applications[index]
                        if len(app) > 20:
                            name, ext = os.path.splitext(app)
                            app = name[:16] + "... " + ext
                        color = color_map.get(app[0].upper(), Fore.RESET)
                        line += f"{Fore.YELLOW}[{index + 1:2}]: {color}{app:<30}{Style.RESET_ALL}"
                print(line)
                if row < rows - 1:
                    print("-" * (34 * max_columns))

            print(f"\n{Fore.WHITE}usage{Fore.WHITE}: {Fore.GREEN}open {Fore.WHITE}<app_nmbr> | {Fore.GREEN}open {Fore.WHITE}<app_str> | {Fore.YELLOW}find {Fore.WHITE}<term> | {Fore.BLUE}add {Fore.WHITE}url <url> | {Fore.BLUE}add {Fore.WHITE}exe <.exe path> | {Fore.RED}remove {Fore.WHITE}<app_nmbr> | {Fore.YELLOW}path {Fore.WHITE}<app_nmbr> | {Fore.CYAN}rename {Fore.WHITE}<app_nmbr> <new_name> | {Fore.MAGENTA}help {Fore.WHITE}for instructions on all functionality\n")
            command = input(f"{Fore.MAGENTA}CLIdow: {Fore.CYAN}").strip().split(maxsplit=2)

            if not command:
                print(f"{Fore.RED}No command entered. Please try again.{Style.RESET_ALL}")
                input(f"{Fore.MAGENTA}Press Enter to continue...{Style.RESET_ALL}")
                continue

            action = command[0].lower()
            if action == 'open' and len(command) > 1:
                self.open_app(command[1])
            elif action == 'find':
                term = command[1] if len(command) > 1 else ""
                applications = self.find_apps(term)
            elif action == 'add' and len(command) > 2:
                if command[1].lower() == 'exe':
                    self.add_exe(command[2])
                elif command[1].lower() == 'url':
                    self.add_url(command[2])
                applications = self.get_applications()
            elif action == 'remove' and len(command) > 1:
                self.remove_app(command[1])
                applications = self.get_applications()
            elif action == 'path' and len(command) > 1:
                self.show_path(command[1])
            elif action == 'rename' and len(command) > 2:
                self.rename_app(command[1], command[2])
                applications = self.get_applications()
            elif action == 'help':
                self.show_help()
            else:
                print(f"{Fore.RED}Invalid command{Style.RESET_ALL}")
                input(f"{Fore.MAGENTA}Press Enter to continue...{Style.RESET_ALL}")

    def get_applications(self):
        applications = []
        for root, _, files in os.walk(self.apps_dir):
            for file in files:
                if os.access(os.path.join(root, file), os.X_OK) or file.endswith(('.exe', '.lnk', '.url')):
                    applications.append(file)
        return applications

    def open_app(self, app_identifier):
        try:
            app_index = int(app_identifier) - 1
            app_path = os.path.join(self.apps_dir, self.applications[app_index])
        except ValueError:
            matches = get_close_matches(app_identifier, self.applications, n=1, cutoff=0.1)
            if matches:
                app_path = os.path.join(self.apps_dir, matches[0])
            else:
                print(f"{Fore.RED}No application found matching '{app_identifier}'{Style.RESET_ALL}")
                input(f"{Fore.MAGENTA}Press Enter to continue...{Style.RESET_ALL}")
                return
        except IndexError:
            print(f"{Fore.RED}Invalid application number{Style.RESET_ALL}")
            input(f"{Fore.MAGENTA}Press Enter to continue...{Style.RESET_ALL}")
            return

        if app_path.endswith('.url') or app_path.endswith('.lnk'):
            os.startfile(app_path)
        elif app_path.endswith('.exe'):
            subprocess.Popen(app_path)

    def find_apps(self, term):
        if term:
            return [app for app in self.applications if term.lower() in app.lower()]
        return self.get_applications()

    def add_exe(self, exe_path):
        if not os.path.isfile(exe_path) or not exe_path.endswith('.exe'):
            print(f"{Fore.RED}Invalid .exe path{Style.RESET_ALL}")
            input(f"{Fore.MAGENTA}Press Enter to continue...{Style.RESET_ALL}")
            return
        shortcut_path = os.path.join(self.apps_dir, os.path.basename(exe_path) + '.lnk')
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = exe_path
        shortcut.save()

    def add_url(self, url):
        if not url.startswith('http://') and not url.startswith('https://'):
            print(f"{Fore.RED}Invalid URL{Style.RESET_ALL}")
            input(f"{Fore.MAGENTA}Press Enter to continue...{Style.RESET_ALL}")
            return
        url_path = os.path.join(self.apps_dir, url.split('//')[1].replace('/', '_') + '.url')
        with open(url_path, 'w') as url_file:
            url_file.write(f"[InternetShortcut]\nURL={url}\n")

    def remove_app(self, app_number):
        try:
            app_index = int(app_number) - 1
            app_path = os.path.join(self.apps_dir, self.applications[app_index])
            os.remove(app_path)
        except (IndexError, ValueError, OSError):
            print(f"{Fore.RED}Invalid application number or unable to remove{Style.RESET_ALL}")
            input(f"{Fore.MAGENTA}Press Enter to continue...{Style.RESET_ALL}")

    def show_path(self, app_number):
        try:
            app_index = int(app_number) - 1
            app_path = os.path.join(self.apps_dir, self.applications[app_index])
            print(f"{Fore.GREEN}Path: {app_path}{Style.RESET_ALL}")
            input(f"{Fore.MAGENTA}Press Enter to continue...{Style.RESET_ALL}")
        except (IndexError, ValueError):
            print(f"{Fore.RED}Invalid application number{Style.RESET_ALL}")
            input(f"{Fore.MAGENTA}Press Enter to continue...{Style.RESET_ALL}")

    def rename_app(self, app_number, new_name):
        try:
            app_index = int(app_number) - 1
            old_path = os.path.join(self.apps_dir, self.applications[app_index])
            name, ext = os.path.splitext(old_path)
            new_path = os.path.join(self.apps_dir, new_name + ext)
            os.rename(old_path, new_path)
        except (IndexError, ValueError, OSError):
            print(f"{Fore.RED}Invalid application number or unable to rename{Style.RESET_ALL}")
            input(f"{Fore.MAGENTA}Press Enter to continue...{Style.RESET_ALL}")

    def show_help(self):
        help_message = f"""
{Fore.MAGENTA}CLIdow Help{Style.RESET_ALL}
{Fore.GREEN}open <app_nmbr>{Style.RESET_ALL}  - Open the application with the given number.
{Fore.GREEN}open <app_str>{Style.RESET_ALL}  - Open the application with the closest match to the given term.
{Fore.YELLOW}find <term>{Style.RESET_ALL}    - Find applications that match the given term.
{Fore.BLUE}add url <url>{Style.RESET_ALL}   - Add a new application from the given URL.
{Fore.BLUE}add exe <.exe path>{Style.RESET_ALL} - Add a new application from the given .exe path.
{Fore.RED}remove <app_nmbr>{Style.RESET_ALL} - Remove the application with the given number.
{Fore.YELLOW}path <app_nmbr>{Style.RESET_ALL} - Show the full path of the application with the given number.
{Fore.CYAN}rename <app_nmbr> <new_name>{Style.RESET_ALL} - Rename the application with the given number, keeping the file type intact.
{Fore.MAGENTA}help{Style.RESET_ALL}          - Show this help message.
"""
        print(help_message)
        input(f"{Fore.MAGENTA}Press Enter to continue...{Style.RESET_ALL}")

#run Clidow
CliDow(sys.argv)
