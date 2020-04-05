import time
from src.amazon import AmazonManger

manager = AmazonManger(is_whole_foods=True)
manager.sign_in()
while True:
    time.sleep(3)
    try:
        manager.start()
    except:
        pass
