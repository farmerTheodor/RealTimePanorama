
import asyncio
import os
import time
import cv2
import kafka
import numpy as np

from camera_manager import CameraManager
from offset_manager import OffsetManager




async def kafka_stream():
    
    camManager = CameraManager()
    offsetManager = OffsetManager()
    await asyncio.sleep(.1)
    # loop over frames
    while True:
        list_of_frames = camManager.grab_frames_from_all_cameras()
        list_of_offsets = offsetManager.get_all_offsets()
        stitched_frame = stitch_overlapping_frames(list_of_frames, list_of_offsets)
        
        encodedImage = cv2.imencode(".jpg", stitched_frame)[1].tobytes()
        # yield frame in byte format
        yield (b"--frame\r\nContent-Type:image/jpeg\r\n\r\n" + encodedImage + b"\r\n")
        await asyncio.sleep(0)
        
    
def rotate_bound(image, angle):
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH))

def stitch_overlapping_frames(list_of_frames, img_offsets):
    if(len(list_of_frames) != len(img_offsets)):
        Exception("Number of frames and offsets must be equal")
    
    i = 0
    stitched_frame = np.zeros((1280, 1280,3), np.uint8)
    for frame in list_of_frames:
        if(frame is not None):
            image_offset_x, image_offset_y, rotation = img_offsets[i]
            frame = rotate_bound(frame, rotation)
            
            to_be_stitched_frame = np.zeros(stitched_frame.shape, np.uint8)
            max_offset_x = image_offset_x + frame.shape[1]
            max_offset_y = image_offset_y + frame.shape[0]
            to_be_stitched_frame[image_offset_y:max_offset_y, image_offset_x:max_offset_x] += frame
            
            np.add(stitched_frame, to_be_stitched_frame, where=stitched_frame==0, out=stitched_frame)
            
        else:
            break
            
        i = i + 1
    stitched_frame = increase_brightness(stitched_frame, 150, 100)
    return stitched_frame  

def increase_brightness(img, brightness=50, contrast=30):
    img = np.int16(img)
    img = img * (contrast/127+1) - contrast + brightness
    img = np.clip(img, 0, 255)
    img = np.uint8(img)
    return img

def create_kafka_consumer():
    kafka_server = os.environ['KAFKA_URL']
    kafka_topic = os.environ['KAFKA_TOPIC']
    consumer = kafka.KafkaConsumer(kafka_topic, group_id="test",bootstrap_servers=[kafka_server],consumer_timeout_ms=100)
    return consumer


def grab_frames_from_kafka(consumer, expected_num_frames):
    print("Grabbing frames from Kafka")
    frames_retrieved = [None]*expected_num_frames
    source_ids_frames_retrieved_from = set()
    for message in consumer:
        if(message.key not in source_ids_frames_retrieved_from):
            break
        source_ids_frames_retrieved_from.add(message.key)
        bytes = next(consumer).value
        frame = cv2.imdecode(np.frombuffer(bytes, dtype=np.uint8), cv2.IMREAD_COLOR)
        frames_retrieved[int(message.key)] = frame

    print("Frames retrieved: ", len(frames_retrieved))
    return frames_retrieved