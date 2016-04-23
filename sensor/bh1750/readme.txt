
------------------------------------------
Introduction - bh1750
------------------------------------------
Light intensity sensor module with built-in a 16 bit AD converter generating digital signal. The data from this module is light
intensity in lx (lux meter). 

------------------------------------------
Where to find datasheet
------------------------------------------
http://rohmfs.rohm.com/en/products/databook/datasheet/ic/sensor/light/bh1750fvi-e.pdf

------------------------------------------
How to check if it is connected correctly
------------------------------------------
> sudo su
> I2Cdetect -y 1
its address is 23

------------------------------------------
How to run it
------------------------------------------
./bh1750.py
OR
python3 bh1750.py
