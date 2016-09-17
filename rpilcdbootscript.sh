cd ~
sudo rm -rf RPiLCDPhone/
git clone https://github.com/naslundx/RPiLCDPhone

sh ~/stopserial.sh
sudo sh ~/stopserial.sh
sudo python lcd-phone.py &

cp ~/RPiLCDPhone/rpilcdbootscript.sh ~/rpilcdbootscript.sh
