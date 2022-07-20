
import cv2
import kafka
import numpy as np


class PanoramaStream:
    """
    Custom Streaming using OpenCV
    """

    def __init__(self):
        kafka_server = '0.0.0.0:9092'
        self.consumer = kafka.KafkaConsumer('jpg_stream',group_id='panoramastream', bootstrap_servers=[kafka_server])
        self.running = True

    def read(self):
        # check if we're still running
        if self.running:
            # read frame from provided source
            bytes = next(self.consumer).value
            frame = cv2.imdecode(np.frombuffer(bytes, dtype=np.uint8), cv2.IMREAD_COLOR)
            # check if frame is available
            if frame is not None:
                return frame
            else:
                # signal we're not running now
                self.running = False
        # return None-type
        return None

    def stop(self):
        self.consumer.close()
        self.running = False