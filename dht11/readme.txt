------------------------------------------
Introduction - DHT11
------------------------------------------
The DHT11 is a basic, low-cost digital temperature
and humidity sensor. It uses a capacitive humidity
sensor and a thermistor to measure the
surrounding air, and spits out a digital signal on the
data pin (no analog input pins needed). 

------------------------------------------
Where to find datasheet
------------------------------------------
http://robocraft.ru/files/datasheet/DHT11.pdf

------------------------------------------
How to check if it is connected correctly
------------------------------------------
> sudo su
> I2Cdetect -y 1
its address is 77

------------------------------------------
How to run it
------------------------------------------
./dhttest.py
OR
python3 dhttest.py
