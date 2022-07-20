import uvicorn
from starlette.routing import Route
from vidgear.gears.asyncio import WebGear_RTC
from health_check_route import health_check
from panorama_stream import PanoramaStream

def setup_server():
    options = {"custom_stream": PanoramaStream(), "enable_infinite_frames": True}
    web = WebGear_RTC(logging=True, **options)
    web.routes.append(Route("/health", endpoint=health_check))
    return web

def start_server():
    web = setup_server()
    uvicorn.run(web(), host="0.0.0.0", port=8000)


if __name__ == '__main__':
    start_server()