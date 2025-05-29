# 🏠 Smart Home IoT Dashboard

This is a Django-based IoT dashboard that connects with an ESP32 microcontroller to monitor sensors (Photoresistor and PIR) and control home appliances via a relay using MQTT protocol. It enables remote monitoring and control of a smart home environment in real-time.
- This is Final Project work in Turin Polytechnic University in Tashkent by Yuldashev Khabibulloh, Rahimjonov Muhammadjon, Sunnatov Izzatulloh. 
- **This project is open-source and available under the MIT License**

## 📌 Features

- 📡 MQTT-based communication between ESP32 and Django
- 🧠 Sensor data logging (Photoresistor for light levels, PIR for motion detection)
- 🔌 Remote control of home appliances (e.g., light, fan) via relay
- 🖥️ Dashboard view to monitor sensor values
- 👤 User authentication and profile management
- ⚙️ Broker settings configuration from the UI



## 📷 System Architecture

ESP32 Sensors ↔ MQTT Broker (Mosquitto) ↔ Django Backend ↔ sqlite3 ↔ Web UI


## 🚀 Tech Stack

- **Microcontroller**: ESP32 (PlatformIO)
- **Protocols**: MQTT (Mosquitto)
- **Backend**: Django 5.2
- **Database**: sqlite3
- **Frontend**: HTML + CSS (Django templates)
- **MQTT Python Client**: `paho-mqtt`


## ⚙️ Setup Instructions

###  Clone the Repository and do other steps

- git clone https://github.com/rahimjonovali/Smart-Home.git
- cd smart-home-dashboard

- python -m venv venv
- On linux: source venv/bin/activate
- On Windows: venv\Scripts\activate  

- pip install -r requirements.txt

- python manage.py makemigrations
- python manage.py migrate

- python manage.py runserver


