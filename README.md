# Cloud Based Underwater Acoustic Recorder
## Introduction
  Underwater noise pollution due to human activities has greatly increased in recent years. There are several studies on high-intensity impulsive noises such as pile driving and seismic exploration. However, less is known about the effects of long-term exposure to low-intensity noises such as those due to bridge traffic. Started as a mechanical engineering capstone project at the University of Washington, Bothell, in 2018, the Cloud Based Underwater Acoustic Recorder (CUAR) was developed to help researchers remotely monitor and collect noise eminnating from Lake Washington's floating bridges. The CUAR is a three-fold project comprised of a budget buoy developed to carry a custom solar panel, a water-tight capsule containing an assortment of electronics fastened to previously the mentioned buoy, and custom software developed by a team of senior computer science majors at UWB.

### Dependencies
## Python Modules
* schedule
* azure
* rpi-gpio
## System (apt)
* ppp
* sox
* arecord
* gpsd
* python-gps
## System (special)
* Hologram SDK

### GPIO Pin Documentation
* GPIO Pin 27: Power (Green)
* GPIO Pin 17: Recording (White)
* GPIO Pin 16: Uploading (Blue)
* GPIO Pin 22: GPS Fix (Red)
* GPIO Pin 20: Internet (Yellow)
* GPIO Pin 24: Amp Enable Line
