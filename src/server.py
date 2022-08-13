import uvicorn
from starlette.routing import Route
from vidgear.gears.asyncio import WebGear
from health_check_route import health_check
from panorama_stream import kafka_stream
from config_route import set_camera_settings
from camera_manager import CameraManager


def setup_server():
    web = WebGear(logging=True)
    web.config["generator"] = kafka_stream
    web.routes.append(Route("/health", endpoint=health_check))
    web.routes.append(Route("/config", endpoint=set_camera_settings, methods=["POST"]) )
    return web
def tear_down_server():
    CameraManager().disconnect_all_cameras()
    
def start_server():
    web = setup_server()
    uvicorn.run(web(), host="0.0.0.0", port=8080)
    tear_down_server()

if __name__ == '__main__':
    start_server()