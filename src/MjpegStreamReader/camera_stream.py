import requests
from threading import Thread, Event

class CameraStream():

    def __init__(self, frame_receiver):
        self.frame_receiver = frame_receiver
        

    def start_stream(self, camera_url, stream_id = 0):
        self.stream_id = stream_id
        self._kill_stream = Event()
        self.stream_daemon = Thread(target=self._open_stream, args=(camera_url, ))
        self.stream_daemon.start()

    def close_stream(self):
        if(self.stream_daemon is None):
            return
        
        self._kill_stream.set()
        self.stream_daemon.join()
        self.stream_daemon = None

        

    #region Camera Stream
    def _open_stream(self, camera_url):
        print("Starting camera stream at: " + camera_url)
        with requests.get(camera_url, stream=True, timeout=20) as r:
            print("Stream opened")
            bytes = b''
            for chunk in r.iter_content(chunk_size=2048):
                bytes += chunk
                bytes = self._push_frame_if_exists(bytes)
                if self._kill_stream.is_set():
                    break
            r.close()

    def _push_frame_if_exists(self, bytes):
        start, end = self._find_frame_start_end(bytes)
        if self._is_frame_found(start, end):
            jpg_bytes, bytes = self._cut_jpg_from_bytes(bytes, start, end)
            self._get_frame_from_bytes(jpg_bytes)
        return bytes

    def _is_frame_found(self, start, end):
        return start != -1 and end != -1


    def _cut_jpg_from_bytes(self, bytes, start, end):
        return bytes[start:end], bytes[end:]

    def _find_frame_start_end(self, bytes):
        start = bytes.find(b'\xff\xd8') #frame starting 
        end = bytes.find(b'\xff\xd9') #frame ending
        if end != -1:
            end = end + 2
            
        return start, end


    def _get_frame_from_bytes(self, jpg_bytes):
        if len(jpg_bytes) < 1:
            return

        self.frame_receiver.on_frame_bytes_received(jpg_bytes, self.stream_id)
    #endregion
