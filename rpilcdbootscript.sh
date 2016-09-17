sudo rm -rf /home/pi/RPiLCDPhone/
cd /home/pi/
git clone https://github.com/naslundx/RPiLCDPhone

sh /home/pi/RPiLCDPhone/stopserial.sh
sudo sh /home/pi/RPiLCDPhone/stopserial.sh
sudo python /home/pi/RPiLCDPhone/lcd-phone.py

cp /home/pi/RPiLCDPhone/rpilcdbootscript.sh /home/pi/rpilcdbootscript.sh
