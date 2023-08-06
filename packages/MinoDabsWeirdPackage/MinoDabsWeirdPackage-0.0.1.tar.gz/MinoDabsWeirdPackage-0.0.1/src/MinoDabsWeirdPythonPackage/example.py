from time import sleep
from datetime import datetime
def slowprint(txt):
    for x in txt:
        print(x, end='', flush=True)
        sleep(0.1)
    print()  # go to new line