import sys, datetime, os; from colorama import Fore; from rich.traceback import Traceback

class Logger():
    def __init__(self):
        self.red = Fore.RED
        self.green = Fore.GREEN
        self.cyan = Fore.CYAN
        self.blue = Fore.BLUE
        self.purp = Fore.MAGENTA
        self.yellow = Fore.YELLOW
        self.reset = Fore.RESET
    
    def log(self, level, *args, **kwargs):
        time_now = datetime.datetime.now().strftime("%H:%M:%S")
        data = f" {self.purp}[ {self.blue}{time_now}{self.purp} ] {self.yellow}[{level}]{self.purp}"
        for arg in args:
            data += f"| {self.green}{arg} {self.purp}"
        if kwargs:
            data += f"| {self.cyan} {kwargs} {self.reset}"
        data += "\n"
        sys.stdout.write(data)
        sys.stdout.flush()