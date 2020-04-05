import time
from src.amazon import AmazonManger


def run_main():
    manager = AmazonManger(is_whole_foods=True)
    manager.sign_in()
    while True:
        manager.start()


while True:
    try:
        run_main()
    except:
        pass
    time.sleep(10)
