from termcolor import colored
from console_progressbar import ProgressBar
import sys, os, time
def undetected():
    return colored("Undetected", 'green')

def detected():
    return colored("Detected", 'red')

def seperator(name):
    print(colored('\n ' + name + ' ', 'yellow'))

def menu():
    end = input ("(0)restart : (1) close :")
    if end == '0':
        os.execl(sys.executable, sys.executable, *sys.argv)
def print_banner():
    print("                                                                              ")
    print(colored("         ( )  __    __  ___  ___      ___    __  ___ ( )  ___       __", 'blue'))
    print(colored("||  / / / / //  ) )  / /   //___) ) //   ) )  / /   / / //   ) ) //   ) )", 'blue'))
    print(colored("|| / / / / //       / /   //       //        / /   / / //   / / //   / /", 'blue'))
    print(colored("||/ / / / //       / /   ((____   ((____    / /   / / ((___/ / //   / /", 'blue'))

def loading():
    pb = ProgressBar(total=100,prefix='virtection', suffix='Loading..', decimals=3, length=50, fill='X', zfill='-')
    pb.print_progress_bar(2)
    time.sleep(1)
    pb.print_progress_bar(25)
    time.sleep(1)
    pb.print_progress_bar(50)
    time.sleep(1)
    pb.print_progress_bar(95)
    time.sleep(1)
    pb.print_progress_bar(100)
    if os.name == 'nt':
        os.system("cls")
    else:
        os.system("clear")
