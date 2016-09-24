sudo rm -rf /home/pi/RPiLCDPhone/
cd /home/pi/
git clone https://github.com/naslundx/RPiLCDPhone

sh /home/pi/RPiLCDPhone/stopserial.sh
sudo sh /home/pi/RPiLCDPhone/stopserial.sh
cp /home/pi/RPiLCDPhone/rpilcdbootscript.sh /home/pi/rpilcdbootscript.sh

# sudo update-rc.d lightdm disable  # Make sure X server is off

sudo python /home/pi/RPiLCDPhone/lcd-phone.py

# sudo reboot  # Reboot on failure