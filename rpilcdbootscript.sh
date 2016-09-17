cd ~
sudo rm -rf RPiLCDPhone/
git clone https://github.com/naslundx/RPiLCDPhone

cp ~/RPiLCDPhone/rpilcdbootscript.sh ~/rpilcdbootscript.sh
sh ~/stopserial.sh
sudo sh ~/stopserial.sh
sudo python lcd-phone.py &
