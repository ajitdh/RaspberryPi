------------------------------------------
Introduction
------------------------------------------
BMP180 
 - It is a barometric pressure temperature and altitude.
 - It is I2C integrated

------------------------------------------
Typical applications
------------------------------------------
- Enhancement of GPS navigation (dead-reckoning, slope detection, etc.)
- In- and out-door navigation
- Leisure and sports
- Weather forecast
- Vertical velocity indication (rise/sink speed)

------------------------------------------
Where to find datasheet
------------------------------------------
http://www.datasheetspdf.com/PDF/BMP180/770150/1

------------------------------------------
It has 4 ports
------------------------------------------
1. VIN - Connect it to 3.3 volt  
2. GND - Connect it to ground
3. SCL - Connect it to clock of I2C
4. SDA - Connect it to data of I2C

------------------------------------------
How to check if it is connected correctly
------------------------------------------
> sudo su
> I2Cdetect -y 1
its address is 77. see image1

------------------------------------------
How to run it
------------------------------------------
> python3 bmp180.py

