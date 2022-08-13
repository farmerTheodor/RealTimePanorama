
from asyncio import Queue

import cv2
import numpy as np
from asyncio import Queue


class BasicReceiver():

    def __init__(self):
        self._frame_queue = Queue()
        self._latest_frame = None

    def get_latest_frame(self):
        frame = self.get_frame()
        while(frame is not None):
            self._latest_frame = frame
            frame = self.get_frame()
        
        return self._latest_frame
    
    def on_frame_bytes_received(self, jpg_bytes, stream_id):
        frame = cv2.imdecode(np.frombuffer(jpg_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)
        self._frame_queue.put_nowait(frame)

    def get_frame(self):
        if(self._frame_queue.empty()):
            return None
        
        return self._frame_queue.get_nowait()
