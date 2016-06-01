import multiprocessing
import time
import random

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
    nmspinning = None
    gfpqueue = None
    gmlist = None
    """
        :type nmspinning: multiprocessing.Value
    """
    g = None
    
    def __init__(self, nmspinning, gfpqueue, gmlist):
        print 'New M'
        self.nmspinning = nmspinning
        self.gfpqueue = gfpqueue
        self.gmlist = gmlist
    
    def spin(self):
        #with self.nmspinning.get_lock():
        self.nmspinning.value = self.nmspinning.value + 1
        race = 0
        while race < 10000:
            race = race + 1 
        while self.nmspinning.value == 1:
            1 == 1
        #with self.nmspinning.get_lock():
        self.nmspinning.value = self.nmspinning.value - 1
        if self.gfpqueue.qsize() != 0:
            p = self.gfpqueue.get()
            self.p = p
            while 1 == 1:
                if p.rgqueue.empty():
                    i = random.randint(0, len(self.gmlist) - 1)
                    if p.stealq(self.gmlist[i].p):
                        g = p.rgqueue.get()
                        g['func'](g['args'])
                        continue
                    else:
                        return
                else:
                    g = p.rgqueue.get()
                    g['func'](g['args'])
                    continue
        else:
            print 'No free P'
            
        

def gocommit(gplist, nmspinning, gmlist, gfpqueue, func, args):
    """
        :type nmspinning: multiprocessing.Value
        :type gplist: multiprocessing.List(P)
    """
    i = random.randint(0, multiprocessing.cpu_count() - 1)
    while gplist[i].m == None:
        i = (i + 1) % multiprocessing.cpu_count()
        #TODO: All P are block
    gplist[i].rgqueue.put({'func': func, 'args': args})
    if nmspinning.value > 0 and len(gmlist) < multiprocessing.cpu_count():
        m = M(nmspinning, gfpqueue, gmlist)
        gmlist.append(m)
        p = multiprocessing.Process(target=m.spin)
        p.start()

def test(msg):
    print msg
    time.sleep(10)

if __name__ == '__main__':
    MAX_PROCS = multiprocessing.cpu_count()
    mgr = multiprocessing.Manager();
    gfpqueue = mgr.Queue(0)
    gplist = mgr.list()
    gmlist = mgr.list()
    grgqueue = mgr.Queue(0)
    i = 0
    while i < MAX_PROCS:
        q = mgr.Queue(0)
        p = P(q)
        gplist.append(p)
        gfpqueue.put(p)
        i = i + 1
    
    nmspinning = mgr.Value('i', 0)
    m = M(nmspinning, gfpqueue, gmlist)
    gmlist.append(m)
    p = multiprocessing.Process(target=m.spin)
    p.start()
    
    gocommit(gplist, nmspinning, gmlist, test, 1)
    gocommit(gplist, nmspinning, gmlist, test, 2)
    gocommit(gplist, nmspinning, gmlist, test, 3)
    gocommit(gplist, nmspinning, gmlist, test, 4)
    gocommit(gplist, nmspinning, gmlist, test, 5)
    gocommit(gplist, nmspinning, gmlist, test, 6)
    