import cv2, queue, time
from threading import Thread, Event, Semaphore
import numpy as np

# Queues
extractionQ= queue.Queue(10)
grayQ= queue.Queue(10)



class extractor(Thread):
    def __init__(self, filename):
        Thread.__init__(self, name = 'extractor')
        self.filename = filename
        
    def run(self):
        '''Take a file and extract the frames and put them on a buffer'''
        global extractionQ
        count = 0
        vidcap = cv2.VideoCapture(self.filename)
        success,image = vidcap.read()
        while success:
            success,image = vidcap.read()
            extractionQ.put(image)
            count += 1
            print('Reading frame {} {}'.format(count, success))
            

class grayscaler(Thread):
    def __init__(self):
        Thread.__init__(self, name = 'grayscaler')
        
    def run(self):
        '''Take a buffer and convert to grayscale and put on the next  buffer.'''
        global extractionQ
        global grayQ
        count = 0
        while True:
            print("Converting frame {} ".format(count))
            frame = extractionQ.get() 
            extractionQ.task_done()
            grayQ.put(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
            count += 1
            
class displayer(Thread):
    def __init__(self):
        Thread.__init__(self, name='displayer')

    def run(self):
        '''Take  the frames and display them all'''
        global grayQ
        count = 0
        while True:
            frame = grayQ.get()
            print('displaying frame {}'.format(count))
            cv2.imshow("Video", frame)
            grayQ.task_done()
            count += 1
            if cv2.waitKey(42) and 0xFF == ord("q"):
                break
        print("Finished displaying all frames")
        cv2.destroyAllWindows()
        
def main():
    video =  'clip.mp4'
    global extractionQ
    global grayQ

    #threads
    extractionT = extractor(video)
    grayT = grayscaler()
    displayT =  displayer()

    extractionT.start()
    grayT.start()
    displayT.start()
    
    extractionT.join()
    grayT.join()
    displayT.join()

main()
