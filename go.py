import multiprocessing
import time
import Queue

class P:
    m = 0   #M associated with P
    rgqueue = Queue.Queue(0)    #runnable goroutine queue
    def steal():
        

class M:
    p = 0   #P associated with M
    block = 0
    g = 0   #G which is running on M now
    grqueue = 0
    nmspinning = 0
    
    def __init__(grgqueue, nmspinning):
        self.grgqueue = grgqueue
        self.nmspinning = nmspinning
        
    def spin():
        while (1 == 1):
            if (g == 0):
                if (p != 0):    #P is associated
                    if (p.rgqueue.empty()):    #P has no G to run
                        if (self.grgqueue.empty()):    #Global has no G to run
                            #TODO: Steal 
                            p.steal()
                        else:
                            while (!self.grgqueue):
                                g = self.grgqueue.get()
                                self.p.rqueue.put(g)
                    else:
                                                        
class G:
    func = 0 #function to do
    
def go(grgqueue, func, args):
    grgqueue.push({'func': func, 'args': args})
    
if __name__ == "__main__":
    mgr = multiprocessing.Manager()
    grgqueue = mgr.Queue(0)
    gfpqueue = mgr.Queue(0)
    nmspinning = mgr.Value('d', 1)
    m0 = M(grqueue, nmspinning)
    m0.spin()
        