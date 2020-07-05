import threading
from loguru import logger


def execute_background(target, args=None):
    logger.info("=============background task {0} ========".format(str(target)))

    if(args != None):
        t1 = threading.Thread(target=target, args=args)
    else:
        t1 = threading.Thread(target=target)

    t1.start()
    t1.join()


"""
How to use it 

def someOtherFunc(data, key):
    print "someOtherFunc was called : data=%s; key=%s" % (str(data), str(key))
 
execute_background(someOtherFunc,args=(data,key))

"""