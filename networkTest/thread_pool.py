import Queue, threading, sys
from threading import Thread
import time

# working thread
class Worker(Thread):
    #worker_count = 0
    timeout = 1
    def __init__( self, workQueue, resultQueue,timeout=2,**kwds):
        Thread.__init__( self, **kwds)
        #self.id = Worker.worker_count
        #Worker.worker_count += 1
        self.setDaemon( True )
        self.workQueue = workQueue
        self.resultQueue = resultQueue
        self.start()
        self.timeout = timeout

    def run( self ):
        while True:
            try:
                callable, args, kwds = self.workQueue.get(timeout=self.timeout)
                res = callable(*args, **kwds)
                #print "worker[%2d]: %s" % (self.id, str(res))
                self.resultQueue.put([res,args,kwds])
                #time.sleep(Worker.sleep)
            except Queue.Empty:
                break
            except :
                print sys.exc_info()
                raise

class WorkerManager(object):
    def __init__(self, num_of_workers=10):
        self.workQueue = Queue.Queue()
        self.resultQueue = Queue.Queue()
        self.workers = []
        #self.timeout = timeout
        self._recruitThreads(num_of_workers)

    def _recruitThreads(self, num_of_workers):
        for i in range( num_of_workers):
            worker = Worker( self.workQueue, self.resultQueue)
            self.workers.append(worker)

    def wait_for_complete(self):
    # ...then, wait for each of them to terminate:
        while len(self.workers):
            worker = self.workers.pop()
            #worker.join()
            if worker.isAlive():
                worker.join()
            #if worker.isAlive() and not self.workQueue.empty():
            #    self.workers.append( worker)
        print "All jobs are completed."

    def add_job(self, callable, *args, **kwds):
        self.workQueue.put((callable, args, kwds))

    def get_result( self, *args, **kwds):
        return self.resultQueue.get( *args, **kwds)

