

### Links und Bilder
[Besuche Google](https://www.google.com)
![Bildbeschreibung](https://via.placeholder.com)

### Code
`inline-code` wird so dargestellt.


# PI-HOLE PORN

## Raspberry Pi Imager

* Device: Raspberry Pi Zero 2 W
* OS: Raspberry Pi OS (other) -> Raspberry Pi OS Lite (64-bit)
* Storage: 128gb SD-Card
* Hostname: pi2hole
* Localisation: Capital city: Berlin (Germany)
  Time zone: Europe/Berlin
  Kayboard layout: de
* User: alex
* Remote access: Enable SSH - Use public key authentication

Write

## Installation

* router -> pi3hole (ETH) -> 192.168.178.86
* `ssh 192.168.178.86`

sudo apt update
sudo apt upgrade -y
sudo reboot

ssh 192.168.178.86

curl -sSL https://install.pi-hole.net | bash

sudo pihole setpassword

----------------------------------------------------------

mkdir git
cd git
git clone https://github.com/projekt21/pi-hole-porn.git

# ssh banner
sudo mv pi-hole-porn/10-uname /etc/update-motd.d/
sudo chmod +x /etc/update-motd.d/10-uname
sudo rm /etc/motd
sudo sed -i 's/\#PrintLastLog yes/PrintLastLog no/g' /etc/ssh/sshd_config
sudo systemctl restart sshd

sudo raspi-config
Interface Options -> SPI -> yes
Interface Options -> I2C -> yes

cd ..

# luma-status
python3 -m venv ~/luma-env

~/luma-env/bin/python -m pip install --upgrade luma.oled
~/luma-env/bin/python -m pip install --upgrade requests


sudo apt-get install python3 python3-pip python3-pil libjpeg-dev zlib1g-dev libfreetype-dev liblcms2-dev libopenjp2-7 libtiff-dev -y

sudo usermod -a -G spi,gpio,i2c alex


cd ~/git/pi-hole-porn
#~/luma-env/bin/python status.py

# luma service
#sudo nano /etc/systemd/system/luma.service
sudo cp luma.service /etc/systemd/system/luma.service
sudo systemctl enable luma.service
sudo systemctl start luma.service

http://192.168.178.86/admin/
Settings -> Teleporter -> Import previously exported configuration
[ ] Configuration
[ ] DHCP leases
[X] Groups
[X] Lists
[X] Domains/Regexes
[ ] Clients

Import
-----------------------------------------------------

