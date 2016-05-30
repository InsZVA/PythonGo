import multiprocessing
import time
import Queue
import random

class P:
    m = 0   #M associated with P
    rgqueue = multiprocessing.Queue(0)    #runnable goroutine queue
    stealfaild = 0
    gfpqueue = 0
    
    def __init__(self, gfpqueue):
        self.gfpqueue = gfpqueue
        
    def steal(self, qpqueue):
        #print 'steal'
        if (len(qpqueue) == 1):
            print 'steal faild&go free because of only 1'
            self.stealfaild = 0
            self.m.p = 0
            self.m = 0
            self.gfpqueue.put(self)
            return
        i = random.randint(0, len(qpqueue) - 1)
        print i
        if (qpqueue[i].rgqueue.empty()):
            self.stealfaild = self.stealfaild + 1
        else:
            j = 0
            self.stealfaild = 0
            while (j <= qpqueue[i].rgqueue.qsize() / 2):
                self.rgqueue.put(qpqueue[i].rgqueue.get())
        if (self.stealfaild >= 8):
            print 'steal faild&go free'
            self.stealfaild = 0
            self.m.p = 0
            self.m = 0
            self.gfpqueue.put(self)

class M:
    p = 0   #P associated with M
    block = 0
    g = 0   #G which is running on M now
    grqueue = 0
    nmspinning = 0
    gfpqueue = 0
    spinning = 0
    gplist = 0
    
    def __init__(self, grgqueue, nmspinning, gfpqueue, gplist):
        self.grgqueue = grgqueue
        self.nmspinning = nmspinning
        self.gfpqueue = gfpqueue
        self.gplist = gplist
        
    def spin(self):
        while (1 == 1):
            if (self.g == 0):
                if (self.p != 0):    #P is associated
                    if (self.p.rgqueue.empty()):    #P has no G to run
                        if (self.grgqueue.empty()):    #Global has no G to run
                            #TODO: Steal 
                            #self.p.steal(self.gplist)
                            1 == 1
                        else:
                            print 'Peek global queue'
                            while (self.grgqueue.empty() != True):
                                g = self.grgqueue.get()
                                self.p.rgqueue.put(g)
                    else:
                        g = self.p.rgqueue.get()
                        self.g = g
                        if (self.spinning == 1):
                            self.spinning = 0
                            self.nmspinning = self.nmspinning - 1
                        g['func'](g['args'])
                        self.g = 0
                else:
                    if (self.gfpqueue.empty() and self.grgqueue.empty() != True): #Global has no free P
                        print 'Create new P'
                        p = P(self.gfpqueue)
                        self.gplist.append(p)
                        self.p = p
                        self.p.m = self
                        continue
                    else:
                        if (self.grgqueue.empty()):
                            if (self.nmspinning >= 1):
                                print 'Go die'
                                break           
                            else:
                                self.spinning = 1
                                self.nmspinning = self.nmspinning + 1
                        else:                
                            print 'Get a free P'
                            p = self.gfpqueue.get()
                            self.p = p
                            p.m = self
            else:
                if (self.spinning == 1):
                    self.spinning = 0
                    self.nmspinning = self.nmspinning - 1
                g['func'](g['args'])
                self.g = 0
                continue

def go(grgqueue, nmspinning, gfpqueue, gplist, func, args):
    if (len(gplist) < 8):
        print 'new M'
        m = M(grgqueue, nmspinning, gfpqueue, gplist)
        m.spin()
    grgqueue.put({'func': func, 'args': args})
    
def func(msg):
    1 == 1
    
if __name__ == "__main__":
    mgr = multiprocessing.Manager()
    grgqueue = mgr.Queue(0)
    gfpqueue = mgr.Queue(0)
    gplist = mgr.list()
    nmspinning = mgr.Value('d', 0)
    i = 0
    while (i < 200):
        go(grgqueue, nmspinning, gfpqueue, gplist, func, (1,))
        i = i + 1
    
