import threading
import sys

def ITNewsSc():
    import ITNewsMedia_Sc

def NikkeiSc():
    import NikkeiXTech_Sc

def stopdef():
    while True:
        n = input()
        if n == 'e':
            print("Stop")
            sys.exit()



thread1 = threading.Thread(target=ITNewsSc)
thread2 = threading.Thread(target=NikkeiSc)
    
thread1.setDaemon(True)
thread2.setDaemon(True)
    
print('Thread Start')
    
thread1.start()
thread2.start()
stopdef()
thread1.stop()
thread2.stop()
    
print('Thread End')
