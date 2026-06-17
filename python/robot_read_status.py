import json
import time
from datetime import datetime
from pymycobot.mycobot import MyCobot

PORT = "COM3"
BAUD = 115200
ROBOT_ID = "MYCOBOT-01"


def close_robot(mc):
    try:
        if hasattr(mc, "_serial_port") and mc._serial_port:
            mc._serial_port.close()
    except Exception:
        pass


def read_with_retry(func, retries=5, delay=0.5):
    for _ in range(retries):
        value = func()
        if value is not None and value != -1:
            return value
        time.sleep(delay)
    return None


mc = None

try:
    mc = MyCobot(PORT, BAUD)
    time.sleep(0.5)

    connected_raw = mc.is_controller_connected()
    connected = connected_raw == 1

    if not connected:
        raise RuntimeError("myCobot controller is not connected")

    angles = read_with_retry(mc.get_angles)
    coords = read_with_retry(mc.get_coords)

    result = {
        "source": "mycobot",
        "robot_id": ROBOT_ID,
        "connected": True,
        "angles": angles,
        "coords": coords,
        "status": "CONNECTED",
        "timestamp": datetime.now().isoformat(timespec="seconds")
    }

    print(json.dumps(result, ensure_ascii=False))

except Exception as e:
    result = {
        "source": "mycobot",
        "robot_id": ROBOT_ID,
        "connected": False,
        "angles": None,
        "coords": None,
        "status": "ERROR",
        "error": str(e),
        "timestamp": datetime.now().isoformat(timespec="seconds")
    }

    print(json.dumps(result, ensure_ascii=False))

finally:
    if mc is not None:
        close_robot(mc)
