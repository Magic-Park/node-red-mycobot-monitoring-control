# myCobot Robot Monitoring and Safe Manual Control

## Project Overview

This project demonstrates a small robot monitoring and safe manual control system using Node-RED, Python, and a myCobot robot arm.

The system reads robot status data through Python, sends it to Node-RED as JSON, displays the values on a Node-RED Dashboard, and allows safe manual control of Joint 6 using small movement commands.

This is a practical learning project focused on robotics monitoring, industrial automation, dashboard visualization, Python integration, and safe command execution.

## Technologies Used

- Node-RED
- Node-RED Dashboard 2.0
- Python
- pymycobot
- pyserial
- myCobot robot arm
- Windows COM port communication

## Features

- Read myCobot connection status
- Display robot ID
- Display joint angles J1-J6
- Display robot pose values X, Y, Z, RX, RY, RZ
- Safe manual control of Joint 6
- J6 +5° movement command
- J6 -5° movement command
- Command status feedback
- Last command tracking
- Basic rate limiting for safer manual control
- JSON parsing between Python and Node-RED

## System Architecture

```text
myCobot Robot
    ↓
Python script
    ↓
JSON output
    ↓
Node-RED exec node
    ↓
JSON parser
    ↓
Node-RED Dashboard
