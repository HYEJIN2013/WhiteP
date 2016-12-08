from abc import ABCMeta, abstractmethod
import logging
import multiprocessing
import threading
import time
try:
    import queue
except ImportError:
    import Queue as queue

log = logging.getLogger(__name__)


class QueueWorker(threading.Thread):
    """
    Worker thread that processes a work queue.
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        super(QueueWorker, self).__init__()
        self.workQueue = None
        self.workQueueBlock = False
        self.runEvent = None

    def run(self):
        if self.runEvent is None:
            raise ValueError('runEvent must be set before starting thread')
        if self.workQueue is None:
            raise ValueError('workQueue must be set before starting thread')

        while self.runEvent.is_set():
            try:
                queueItem = self.workQueue.get(block=self.workQueueBlock)
                self.processNext(queueItem)
            except queue.Empty:
                break

    @abstractmethod
    def processNext(self, queueItem):
        """
        Process the next work queue item.
        """
        pass

    @classmethod
    def startWorkers(cls, workerFactory, workQueue, numThreads=None, waitForever=False):
        """
        Spawns a QueueWorker pool that consumes a workQueue in parallel.
        This pool should only be I/O bound because it's using Python's green threads.
        Parameters
        ----------
        workerFactory : QueueWorker | callable<QueueWorker>
            Factory function to create new threads.
        workQueue : Queue
            Work queue to process.
        numThreads : int
            Number of threads to allocate.
            Defults to the number of CPUs on the machine.
        waitForever : bool
            Should the thread pool wait for tasks forever?
            If False, it will exit once the workQueue is drained.
        """
        if not callable(workerFactory):
            raise ValueError('workerFactory must be callable')

        if not isinstance(workQueue, Queue):
            raise ValueError('workQueue must be a Queue')
        
        # Early optimization
        if (not waitForever) and queue.empty():
            log.warn('Exiting early since waitForever is True, but the workQueue was empty!')
            return

        if numThreads is None:
            numThreads = multiprocessing.cpu_count()
            log.debug('Worker pool is defaulting to %d threads' % numThreads)
        elif numThreads < 1:
            raise ValueError('numThreads must be >= 1')

        runEvent = threading.Event()
        runEvent.set()

        # Spawn worker threads
        threads = []
        for i in range(numThreads):
            thread = workerFactory()
            if not isinstance(thread, QueueWorker):
                raise ValueError('workerFactory must return an instance of a QueueWorker')

            thread.runEvent = runEvent
            thread.workQueue = workQueue
            thread.workQueueBlock = waitForever
            thread.daemon = True
            thread.start()

            threads.append(thread)

        # Wait for threads to finish processing
        try:
            while runEvent.is_set() and (waitForever or not workQueue.empty()):
                time.sleep(1)

        except KeyboardInterrupt:
            log.warn('^C pressed!')

        # Join all threads    
        runEvent.clear()
        for thread in threads:
            if thread.isAlive():
                thread.join()
                

##### Example #####
import urllib


class Downloader(QueueWorker):
    def __init__(self, outputPath):
        super(Downloader, self).__init__()
        self.outputPath = outputPath
    
    def processNext(self, queueItem):
        downloadUrl, fileName = queueItem
        
        outFile = os.path.join(self.outputPath, fileName)
        if os.path.exists(outFile):
            log.debug('Skipping: %s' % outFile)
            return

        log.info('Downloading "%s" from %s' % (fileName, downloadUrl))
        buff = urllib.urlopen(downloadUrl).read()
        with open(outFile, 'wb') as f:
            f.write(buff)


if __name__ == '__main__':
    outputPath = 'downloads'

    downloadQueue = queue.Queue()
    for queueItem in getFilesToDownload(...):
        downloadQueue.put(queueItem)

    QueueWorker.startWorkers(workerFactory=lambda: Downloader(outputPath),
                             workQueue=downloadQueue,
                             numThreads=32)
