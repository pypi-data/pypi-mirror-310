# __init__.py
# Copyleft (c) 2024 daysant - 2024
# This file is licensed under the terms of the daysant license v2.
# daysant@proton.me

import os

class Nisshi:
    def __init__(self):
        self.levels = {
            "trace": True,
            "debug": True,
            "info": True,
            "warn": True,
            "error": True
        }
        self.colors = {
            "trace": "\033[90m",
            "debug": "\033[34m",
            "info": "\033[0m",
            "warn": "\033[33m",
            "error": "\033[31m"
        }
        self.log_file_path = None

    def set_levels(self, levels):
        if levels == "all":
            for key in self.levels:
                self.levels[key] = True
        elif levels == "none":
            for key in self.levels:
                self.levels[key] = False
        else:
            self.levels.update(levels)

    def set_colors(self, colors):
        self.colors.update(colors)

    def set_log_file_path(self, file_path):
        self.log_file_path = file_path
        if self.log_file_path is False:
            return
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write('')

    def log_to_file(self, message):
        if self.log_file_path:
            with open(self.log_file_path, 'a') as f:
                f.write(message + '\n')

    def trace(self, message):
        level = "trace"
        if self.levels[level]:
            lines = message.split('\n')
            for index, line in enumerate(lines):
                if index == 0:
                    print(f"{self.colors[level]}\033[1m{level.upper()}\033[0m{self.colors[level]} │ {line}\033[0m")
                else:
                    print(f"{self.colors[level]}      │ {line}\033[0m")
            self.log_to_file(f"{level.upper()} │ {message}")

    def debug(self, message):
        level = "debug"
        if self.levels[level]:
            lines = message.split('\n')
            for index, line in enumerate(lines):
                if index == 0:
                    print(f"{self.colors[level]}\033[1m{level.upper()}\033[0m{self.colors[level]} │ {line}\033[0m")
                else:
                    print(f"{self.colors[level]}      │ {line}\033[0m")
            self.log_to_file(f"{level.upper()} │ {message}")

    def info(self, message):
        level = "info"
        if self.levels[level]:
            lines = message.split('\n')
            for index, line in enumerate(lines):
                if index == 0:
                    print(f"{self.colors[level]}\033[1m{level.upper()}\033[0m{self.colors[level]}  │ {line}\033[0m")
                else:
                    print(f"{self.colors[level]}      │ {line}\033[0m")
            self.log_to_file(f"{level.upper()} │ {message}")

    def warn(self, message):
        level = "warn"
        if self.levels[level]:
            lines = message.split('\n')
            for index, line in enumerate(lines):
                if index == 0:
                    print(f"{self.colors[level]}\033[1m{level.upper()}\033[0m{self.colors[level]}  │ {line}\033[0m")
                    self.log_to_file(f"{level.upper()} │ {line}")
                else:
                    print(f"{self.colors[level]}      │ {line}\033[0m")
                    self.log_to_file(f"      │ {line}")

    def error(self, message):
        level = "error"
        if self.levels[level]:
            lines = message.split('\n')
            for index, line in enumerate(lines):
                if index == 0:
                    print(f"{self.colors[level]}\033[1m{level.upper()}\033[0m{self.colors[level]} │ {line}\033[0m")
                else:
                    print(f"{self.colors[level]}      │ {line}\033[0m")
            self.log_to_file(f"{level.upper()} │ {message}")

    def newline(self):
        print('      │')
