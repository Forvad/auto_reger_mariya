from os import system
from time import sleep

system('cd Desktop')
system('cd skript')

for _ in range(5):
    system('python AppDynamicsJob.py')
    sleep(60)
