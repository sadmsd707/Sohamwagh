import os, subprocess, glob, sys

# ------------------------------------------------------------
# Comprehensive list of MCU & sensor libraries
# ------------------------------------------------------------
repos = [
    # --- Arduino Cores (fundamentals) ---
    "https://github.com/arduino/ArduinoCore-avr.git",
    "https://github.com/arduino/ArduinoCore-samd.git",
    "https://github.com/arduino/ArduinoCore-megaavr.git",
    "https://github.com/arduino/ArduinoCore-nRF528x-mbedos.git",
    "https://github.com/arduino/ArduinoCore-renesas.git",
    "https://github.com/arduino/ArduinoCore-mbed.git",

    # --- ESP32 / ESP8266 ---
    "https://github.com/espressif/arduino-esp32.git",
    "https://github.com/esp8266/Arduino.git",
    "https://github.com/espressif/esp-idf.git",                 # official SDK (contains examples)
    "https://github.com/espressif/esp32-camera.git",

    # --- STM32 ---
    "https://github.com/stm32duino/Arduino_Core_STM32.git",
    "https://github.com/stm32duino/STM32LowPower.git",
    "https://github.com/stm32duino/STM32RTC.git",

    # --- Raspberry Pi Pico (C/C++ SDK & Arduino core) ---
    "https://github.com/raspberrypi/pico-sdk.git",
    "https://github.com/raspberrypi/pico-examples.git",
    "https://github.com/earlephilhower/arduino-pico.git",

    # --- Adafruit Sensor Libraries (the “gold standard”) ---
    "https://github.com/adafruit/Adafruit_Sensor.git",
    "https://github.com/adafruit/Adafruit_BME280_Library.git",
    "https://github.com/adafruit/Adafruit_BME680.git",
    "https://github.com/adafruit/Adafruit_BMP280_Library.git",
    "https://github.com/adafruit/Adafruit_MPU6050.git",
    "https://github.com/adafruit/Adafruit_LIS3DH.git",
    "https://github.com/adafruit/Adafruit_LSM6DS.git",
    "https://github.com/adafruit/Adafruit_ADXL345.git",
    "https://github.com/adafruit/Adafruit_BNO055.git",
    "https://github.com/adafruit/Adafruit_GPS.git",
    "https://github.com/adafruit/Adafruit_BMP085_Unified.git",
    "https://github.com/adafruit/Adafruit_TSL2561.git",
    "https://github.com/adafruit/Adafruit_TSL2591_Library.git",
    "https://github.com/adafruit/Adafruit_VEML6070.git",
    "https://github.com/adafruit/Adafruit_CCS811.git",
    "https://github.com/adafruit/Adafruit_SGP30.git",
    "https://github.com/adafruit/Adafruit_AM2315.git",
    "https://github.com/adafruit/Adafruit_DHT.git",               # DHT11/22
    "https://github.com/adafruit/DHT-sensor-library.git",
    "https://github.com/adafruit/Adafruit_INA219.git",
    "https://github.com/adafruit/Adafruit_INA260.git",
    "https://github.com/adafruit/Adafruit_PM25AQI.git",
    "https://github.com/adafruit/Adafruit_NeoPixel.git",
    "https://github.com/adafruit/Adafruit_GFX_Library.git",      # displays
    "https://github.com/adafruit/Adafruit_SSD1306.git",
    "https://github.com/adafruit/Adafruit-ST7735-Library.git",
    "https://github.com/adafruit/Adafruit_ILI9341.git",
    "https://github.com/adafruit/Adafruit_EPD.git",
    "https://github.com/adafruit/Adafruit_Keypad.git",
    "https://github.com/adafruit/Adafruit_Motor_Shield_V2_Library.git",
    "https://github.com/adafruit/Adafruit-PWM-Servo-Driver-Library.git",

    # --- SparkFun Sensor Libraries ---
    "https://github.com/sparkfun/SparkFun_MPU-9250-DMP_Arduino_Library.git",
    "https://github.com/sparkfun/SparkFun_MS5803-14BA_Breakout_Arduino_Library.git",
    "https://github.com/sparkfun/SparkFun_LIS331_Arduino_Library.git",
    "https://github.com/sparkfun/SparkFun_CCS811_Arduino_Library.git",
    "https://github.com/sparkfun/SparkFun_BME280_Arduino_Library.git",
    "https://github.com/sparkfun/SparkFun_ADXL345_Arduino_Library.git",
    "https://github.com/sparkfun/SparkFun_AS726X_Arduino_Library.git",
    "https://github.com/sparkfun/SparkFun_u-blox_GNSS_Arduino_Library.git",

    # --- Seeed Studio Sensors ---
    "https://github.com/Seeed-Studio/Seeed_Arduino_UltrasonicRanger.git",
    "https://github.com/Seeed-Studio/Grove_Ultrasonic_Ranger.git",
    "https://github.com/Seeed-Studio/Grove_BME280.git",
    "https://github.com/Seeed-Studio/Grove_Temperature_And_Humidity_Sensor.git",
    "https://github.com/Seeed-Studio/Grove_3Axis_Digital_Accelerometer.git",
    "https://github.com/Seeed-Studio/Seeed_Arduino_LIS3DHTR.git",

    # --- Pololu ---
    "https://github.com/pololu/vl53l1x-arduino.git",
    "https://github.com/pololu/drv8835-motor-shield.git",

    # --- Popular standalone sensor drivers ---
    "https://github.com/RobTillaart/DHTlib.git",
    "https://github.com/markruys/arduino-DHT.git",
    "https://github.com/closedcube/ClosedCube_BMP280_Arduino.git",
    "https://github.com/thomasfredericks/BMP280_DEV.git",
    "https://github.com/jrowberg/i2cdevlib.git",                 # massive collection of I2C sensors (MPU6050, HMC5883, etc.)
    "https://github.com/adafruit/Adafruit_BusIO.git",            # I2C/SPI helper

    # --- MicroPython libraries for microcontrollers ---
    "https://github.com/micropython/micropython-lib.git",
    "https://github.com/micropython/micropython.git",            # the core (contains drivers in ports/)
    "https://github.com/arduino/ArduinoCore-renesas.git",

    # --- MQTT / IoT communication (important for MCUs) ---
    "https://github.com/knolleary/pubsubclient.git",
    "https://github.com/adafruit/Adafruit_MQTT_Library.git",

    # --- Additional embedded protocols (CAN, Modbus, etc.) ---
    "https://github.com/sandeepmistry/arduino-CAN.git",
    "https://github.com/4-20ma/ModbusMaster.git",
    "https://github.com/smarmengol/Modbus-Master-Slave-for-Arduino.git",

    # --- Teensy cores (powerful ARM) ---
    "https://github.com/PaulStoffregen/cores.git",

    # --- LittleFS / File systems (commonly used in data logging) ---
    "https://github.com/littlefs-project/littlefs.git",

    # --- RTC libraries ---
    "https://github.com/adafruit/RTClib.git",

    # --- Motor / Servo control ---
    "https://github.com/adafruit/Adafruit-Motor-Shield-library.git",
    "https://github.com/arduino-libraries/Servo.git",
]

# ------------------------------------------------------------
# Clone only if not already present
# ------------------------------------------------------------
os.makedirs("cloned_repos", exist_ok=True)
total = len(repos)
for i, url in enumerate(repos, 1):
    name = url.rstrip("/").split("/")[-1].replace(".git", "")
    dest = os.path.join("cloned_repos", name)
    if not os.path.exists(dest):
        print(f"[{i}/{total}] Cloning {name} ...")
        ret = subprocess.run(["git", "clone", "--depth", "1", url, dest],
                             capture_output=True, text=True)
        if ret.returncode != 0:
            print(f"  Failed: {ret.stderr.strip()}")
        else:
            print("  Done.")
    else:
        print(f"[{i}/{total}] {name} already exists, skipping.")

# ------------------------------------------------------------
# Extract all source files into one big corpus.txt
# ------------------------------------------------------------
print("\nBuilding corpus.txt ...")
extensions = {".c", ".cpp", ".h", ".ino", ".py", ".txt", ".md"}
total_files = 0
with open("corpus.txt", "w", encoding="utf-8", errors="ignore") as out:
    for fpath in glob.iglob("cloned_repos/**/*", recursive=True):
        _, ext = os.path.splitext(fpath)
        if ext.lower() in extensions:
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    if len(content) > 50:   # skip near‑empty files
                        out.write(content + "\n")
                        total_files += 1
            except:
                pass

print(f"Corpus created: {total_files} files written to corpus.txt")
size_mb = os.path.getsize("corpus.txt") / (1024*1024)
print(f"Total size: {size_mb:.2f} MB")