import multiprocessing
import time

class P:
    rgqueue = None
    m = None
    gfpqueue = None
    """
        :type rgqueue: multiprocessing.Queue
        :type m: M
        :type gfpqueue: multiprocessing.Queue
    """
    
    def __init__(self, rgqueue):
        self.rgqueue =  rgqueue
        
    def stealq(self, p2):
        """
            :type p2: P
        """
        size = p2.rgqueue.qsize()
        if size < 1:
            self.m.p = None
            self.gfpqueue.put(self)
            return False
        i = 0
        while i < size / 2:
            g = p2.qgqueue.get()
            self.rgqueue.put(g)
            i = i + 1
        return True

class M:
    p = None
    spinning = False
    
    def spin(self):
        

if __name__ == '__main__':
    MAX_PROCS = multiprocessing.cpu_count()
    
    i = 0
    rgqueues = []
    while i < MAX_PROCS:
        q = multiprocessing.Queue(0)
        rgqueues.append(q)
        i = i + 1
    
    grgqueue = multiprocessing.Queue(0)
    gfpqueue = multiprocessing.Queue(0)
    gfmqueue = multiprocessing.Queue(0)
    gplist = multiprocessing.List()
    nmspinning = multiprocessing.Value('d', 0)
    