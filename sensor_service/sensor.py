import Adafruit_DHT

SENSOR = Adafruit_DHT.DHT22
PIN = 4

def read_sensor():
    humidity, temperature = Adafruit_DHT.read_retry(SENSOR, PIN)
    if humidity is not None and temperature is not None:
        return {
            "temperature": round(temperature, 2),
            "humidity": round(humidity, 2),
            "error": False
        }
    else:
        return {
            "temperature": None,
            "humidity": None,
            "error": True
        }