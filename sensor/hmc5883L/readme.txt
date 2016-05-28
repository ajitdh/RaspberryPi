
------------------------------------------
Introduction
------------------------------------------
hmc58831 
 - low-field magnetic sensing
 - digital interface for applications such as lowcost compassing and magnetometry.
 - It is I2C integrated
 
------------------------------------------
Typical applications
------------------------------------------

------------------------------------------
Where to find datasheet
------------------------------------------
https://cdn-shop.adafruit.com/datasheets/HMC5883L_3-Axis_Digital_Compass_IC.pdf

------------------------------------------
It has 4 ports
------------------------------------------
1. VCC +5 - Connect it to 5 volt  
2. GND - Connect it to ground
3. SCL - Connect it to clock of I2C
4. SDA - Connect it to data of I2C

------------------------------------------
How to check if it is connected correctly
------------------------------------------
> sudo su
> I2Cdetect -y 1
its address is 1e

------------------------------------------
How to run it
------------------------------------------
> python3 hmc58831.py

------------------------------------------
References
------------------------------------------
http://www.recantha.co.uk/blog/?p=2547
