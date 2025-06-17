# MMM-RoomSensors

MMM-RoomSensors is a MagicMirror² module to display temperature and humidity readings from multiple Raspberry Pi sensors located in different rooms. It combines local sensor data and remote sensor data via a simple HTTP API.


 🌡️ Températures       

 🏠 Salon                     
   🌡️ Température : 22.3 °C   
   💧 Humidité   : 48.7 %     

 🛏️ Chambre                   
   🌡️ Température : 20.1 °C   
   💧 Humidité   : 51.2 %     



---

## Features

- Supports multiple sensors on different Raspberry Pis
- Fetches remote sensor data via HTTP
- Displays temperature and humidity with icons
- Easy to configure and extend

---

## Requirements

- MagicMirror² installed on a Raspberry Pi (or compatible system)
- Node.js installed (comes with MagicMirror²)
- Python 3 installed on the Raspberry Pis with sensors
- Network connectivity between the MagicMirror Pi and remote Pi sensors

---

## Installation

### Step 1: Setup the Remote Sensor (Raspberry Pi Zero)

1. Install Raspberry Pi OS and connect your sensor (e.g. DHT22).  
2. Update and install Python dependencies:
3. Set up Python environment and dependencies:
   
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
```

4. Create a folder and copy the sensor service files (app.py, sensor.py, __init__.py, requirements.txt) there:

```bash
mkdir ~/sensor_service
cd ~/sensor_service
```

5. Copy the Python files (app.py, sensor.py, __init__.py) into this folder.
(These files run a small Python web server that reads sensor data and serves it over the network.)

6. Create a Python virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 2 – Create and enable the systemd service on Pi Zero

1. Create a systemd service file to run the sensor server automatically:

```bash
sudo nano /etc/systemd/system/sensor_service.service
```

2. Paste this content:

```ini
[Unit]
Description=Room Sensor Service
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/sensor_service
ExecStart=/home/pi/sensor_service/venv/bin/python /home/pi/sensor_service/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

3. Save and exit (Ctrl+O, Enter, Ctrl+X).

4. Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable sensor_service.service
sudo systemctl start sensor_service.service
```

5. Verify the service is running:

```bash
sudo systemctl status sensor_service.service
```
Your Pi Zero is now running a server that provides sensor data at http://<pi-zero-ip>:5000/data.

---

### Step 3 – Install the MMM-RoomSensors module on your MagicMirror (Pi 4)

1. SSH into your Pi 4 (MagicMirror):

```bash
cd ~/MagicMirror/modules
git clone https://github.com/cobaye49/MMM-RoomSensors.git
```

2. Navigate into the module folder and install npm dependencies:

```bash
cd MMM-RoomSensors
npm install
```

### Step 4 – Configure MagicMirror to use the module

1. Open your MagicMirror config file:

```bash
nano ~/MagicMirror/config/config.js
```

2. Add this module config
Remplace pi-zero-ip with the actual IP address of your PI Zero

```js
{
  module: "MMM-RoomSensors",
  position: "top_right",
  config: {
    refreshInterval: 30000, // refresh every 30 seconds
    sensors: [
      {
        name: "Living Room",
        type: "local",
        sensorType: "dht22",
        gpioPin: 4
      },
      {
        name: "Remote Room",
        type: "remote",
        url: "http://<pi-zero-ip>:5000/data"
      }
    ]
  }
},
```

3. Save and exit (Ctrl+O, Enter, Ctrl+X).

### Step 5 – Restart MagicMirror

Restart your MagicMirror app to load the new module:

```bash
pm2 restart mm
```

Or

```bash
cd ~/MagicMirror
npm start
```

---

### What you should see

- Temperature and humidity readings from both your Pi 4 (local sensor) and Pi Zero (remote sensor)
  
- Nicely formatted with icons (thermometer, droplet) and labels showing each room’s name
  
- Values updated every 30 seconds
  
---

### Troubleshooting tips

- Make sure your Pi Zero’s sensor server is running and reachable (try visiting http://<pi-zero-ip>:5000/data in a browser).

- Ensure your Pi 4 and Pi Zero are on the same local network.

- Check MagicMirror logs (~/.pm2/logs/mm-out.log) for any errors related to MMM-RoomSensors.

- Confirm npm dependencies installed correctly inside the module folder.
