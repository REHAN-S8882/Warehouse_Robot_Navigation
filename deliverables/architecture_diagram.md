# 🧭 Warehouse Robot Navigation – System Architecture

## High-Level Overview
+-------------------+            +----------------------+            +-------------------------+
|  Sensors on Robot |            |      IoT Gateway     |            |         Cloud           |
|  - LIDAR          | --MQTT-->  | (Edge device: Jetson | --MQTT-->  | - AWS IoT / Azure IoT  |
|  - Camera (RGB)   |            |  Nano/Raspberry Pi)  |            | - Storage (S3/Blob/GCS)|
+-------------------+            +----------------------+            +-------------------------+
