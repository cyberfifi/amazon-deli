from multiprocessing import Process
from src.amazon import AmazonManger

manager = AmazonManger(is_whole_foods=True)
try:
    manager.start()
except:
    manager.driver.close()
