import threading


def ITNewsSc():
    import ITNewsMedia_Sc

def NikkeiSc():
    import NikkeiXTech_Sc


def main():
    thread1 = threading.Thread(target=ITNewsSc)
    thread2 = threading.Thread(target=NikkeiSc)
    
    print('Thread Start')
    
    thread1.start()
    thread2.start()
    
    thread1.join()
    thread2.join()
    
    print('Thread End')

if __name__=='__main__':
    main()