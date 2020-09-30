import time
import random


# На вход интервал времени для ожидания
def sleep_time(minwait, maxwait):
    # Wait for random seconds
    number = random.randint(minwait, maxwait)
    source = "Ждем... {:d} секунд"
    target = source.format(number)
    print(target)
    time.sleep(number)
