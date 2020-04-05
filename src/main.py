import time
from src.amazon import AmazonManger


def run_main():
    manager = AmazonManger()
    manager.sign_in()
    manager.start()


run_main()
