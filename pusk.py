from os import system
from time import sleep
from loguru import logger


i = 1
while True:
    system('python AppDynamicsJobV.py')
    logger.success(f'круг № {i}')
    if i % 6 == 0:
        logger.success(f'{i} круг, Спим 10 минут !!!')
        sleep(300)
        logger.success('Осталось 5 минут')
        sleep(300)

    sleep(5)
    i += 1
