from os import system
from time import sleep


for _ in range(5):
    system('python AppDynamicsJob.py')
    sleep(60)
