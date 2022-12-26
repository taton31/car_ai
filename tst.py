from multiprocessing import Pool
import time
from threading import Thread


def f(x):
    for i in x:
        i=i*i

if __name__ == '__main__':
    
    tst = [x for x in range(100000000)]
    start_time = time.time()
    # p.map(f, tst)
    # import threading

    # threads = []

    # # Create threads and pass the parameters to each thread
    # t1 = threading.Thread(target=f, args=[tst[0::3]])
    # t2 = threading.Thread(target=f, args=[tst[1::3]])
    # t3 = threading.Thread(target=f, args=[tst[2::3]])

    # # Start the threads
    # threads.append(t1)
    # threads.append(t2)
    # threads.append(t3)
    # t1.start()
    # t2.start()
    # t3.start()
    f(tst)
    # for i in tst:
    #     f(i)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Function execution time: {round(elapsed_time,2)} seconds')
    