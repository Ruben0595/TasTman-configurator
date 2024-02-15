import tkinter as tk
from mp import mpfshell

# Create an instance of the MPFShell
shell = mpfshell.MpFileShell()

# Connect to the device
shell.do_open('ws:192.168.4.1, 123456')

# You can add more commands to execute here if needed
if shell.do_check_connection():
    #shell.do_cd('database')
    shell.do_ls('<dir> database')
    shell.do_cd('..')
    print('went back')
    shell.do_ls('')
    #shell.do_put('config.txt config.py')
    shell.do_close('')
