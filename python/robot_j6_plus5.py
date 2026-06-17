import json
import time
from datetime import datetime
from pymycobot.mycobot import MyCobot

PORT = "COM3"
BAUD = 115200
ROBOT_ID = "MYCOBOT-01"

JOINT_ID = 6
DELTA = 5
SPEED = 10


def close_robot(mc):
    try:
        if hasattr(mc, "_serial_port") and mc._serial_port:
            mc._serial_port.close()
    except Exception:
        pass


def read_angles_with_retry(mc, retries=5, delay=0.5):
    for _ in range(retries):
        angles = mc.get_angles()

        if isinstance(angles, list) and len(angles) >= 6:
            return angles

        time.sleep(delay)

    raise RuntimeError("Invalid angles value after retries")


mc = None

try:
    mc = MyCobot(PORT, BAUD)
    time.sleep(0.5)

    connected = mc.is_controller_connected()

    if connected != 1:
        raise RuntimeError("myCobot controller is not connected")

    angles = read_angles_with_retry(mc)

    current_j6 = float(angles[5])
    target_j6 = current_j6 + DELTA

    if target_j6 > 180:
        target_j6 = 180

    if target_j6 < -180:
        target_j6 = -180

    mc.send_angle(JOINT_ID, target_j6, SPEED)

    time.sleep(2)

    new_angles = read_angles_with_retry(mc)

    result = {
        "source": "mycobot",
        "robot_id": ROBOT_ID,
        "command": "J6_PLUS_5",
        "connected": True,
        "joint_id": JOINT_ID,
        "old_j6": current_j6,
        "target_j6": target_j6,
        "new_angles": new_angles,
        "status": "MOVED",
        "timestamp": datetime.now().isoformat(timespec="seconds")
    }

    print(json.dumps(result, ensure_ascii=False))

except Exception as e:
    result = {
        "source": "mycobot",
        "robot_id": ROBOT_ID,
        "command": "J6_PLUS_5",
        "connected": False,
        "status": "ERROR",
        "error": str(e),
        "timestamp": datetime.now().isoformat(timespec="seconds")
    }

    print(json.dumps(result, ensure_ascii=False))

finally:
    if mc is not None:
        close_robot(mc)
