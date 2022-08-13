import threading
import time

import cv2
import numpy as np

from MjpegStreamReader.basic_camera_receiver import BasicReceiver
from MjpegStreamReader.camera_stream import CameraStream



class CameraManager():
    
    #region Singleton Constructor
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
         
        if not cls._instance:
            with cls._lock:
                # another thread could have created the instance
                # before we acquired the lock. So check that the
                # instance is still nonexistent.
                if not cls._instance:
                    cls._instance = super(CameraManager, cls).__new__(cls)
                    cls._instance.init()
                    
        return cls._instance
    #endregion
    
    def init(self) -> None:
        self.list_of_cameras= []
        self.list_of_recievers = []
    
    def connect_camera(self, camera_ip: str) -> None:        
        reciever = BasicReceiver()
        cam = CameraStream(reciever)
        cam.start_stream(camera_ip) 
        
        self.list_of_recievers.append(reciever)
        self.list_of_cameras.append(cam)
    
    def disconnect_all_cameras(self):
        for cam in self.list_of_cameras:
            cam.close_stream()
    
    def delete_all_cameras(self):
        self.list_of_cameras = []
        self.list_of_recievers = []
    
    def grab_frames_from_all_cameras(self):
        list_of_frames = [None]*len(self.list_of_cameras)
        for i in range(len(self.list_of_cameras)):
            receiver = self.list_of_recievers[i]
            frame = receiver.get_latest_frame()
            list_of_frames[i] = frame
            
            
        return list_of_frames
    

