from starlette.responses import JSONResponse
from camera_manager import CameraManager

from offset_manager import OffsetManager

async def set_camera_settings(request):
    offset_manager = OffsetManager()
    offset_manager.delete_all_offsets()
    
    camera_manager = CameraManager()
    camera_manager.disconnect_all_cameras()
    camera_manager.delete_all_cameras()
    
    camera_settings = await request.json()
    for camera in camera_settings:
        camera_manager.connect_camera(camera["ip"])
        offset_manager.create_offset(camera["x"], camera["y"], camera["angle"])
        
    return JSONResponse(camera_settings)
