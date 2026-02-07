![Screenshot](./screenshot.png)

# PI-HOLE PORN

## Raspberry Pi Imager

* Device: Raspberry Pi Zero 2 W
* OS: Raspberry Pi OS (other) -> Raspberry Pi OS Lite (64-bit)
* Storage: >32gb SD-Card
* Hostname: pi2hole
* User: alex
* Remote access: Enable SSH - Use public key authentication

Write

## Installation

router -> pi2hole (ETH) -> 192.168.178.86

* `ssh 192.168.178.86`

* `sudo apt update`
* `sudo apt upgrade -y`
* `sudo reboot`

* `ssh 192.168.178.86`

### Pi-Hole

* `curl -sSL https://install.pi-hole.net | bash`

* `sudo pihole setpassword`

### SSH Banner
* `mkdir git`
* `cd git`
* `git clone https://github.com/projekt21/pi-hole-porn.git`

* `sudo mv pi-hole-porn/10-uname /etc/update-motd.d/`
* `sudo chmod +x /etc/update-motd.d/10-uname`
* `sudo rm /etc/motd`
* `sudo sed -i 's/\#PrintLastLog yes/PrintLastLog no/g' /etc/ssh/sshd_config`
* `sudo systemctl restart sshd`
* `cd ..`

### raspi-config
* `sudo raspi-config`
  
`Interface Options -> SPI -> yes`\
`Interface Options -> I2C -> yes`

### luma-Status
* `python3 -m venv ~/luma-env`

* `~/luma-env/bin/python -m pip install --upgrade luma.oled`
* `~/luma-env/bin/python -m pip install --upgrade requests`

* `sudo apt-get install python3 python3-pip python3-pil libjpeg-dev zlib1g-dev libfreetype-dev liblcms2-dev libopenjp2-7 libtiff-dev -y`

* `sudo usermod -a -G spi,gpio,i2c alex`

### luma Service
* `sudo cp ~/git/pi-hole-porn/luma.service /etc/systemd/system/luma.service`
* `sudo systemctl enable luma.service`
* `sudo systemctl start luma.service`

### http://192.168.178.86/admin/
`Settings -> Teleporter -> Import previously exported configuration`

`[ ] Configuration`\
`[ ] DHCP leases`\
`[X] Groups`\
`[X] Lists`\
`[X] Domains/Regexes`\
`[ ] Clients`

Import

## List Block

### Tracking/Ads
*   https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts
* 	https://v.firebog.net/hosts/Easyprivacy.txt
* 	https://v.firebog.net/hosts/Easylist.txt
* 	https://adaway.org/hosts.txt
* 	https://gitlab.com/hagezi/mirror/-/raw/main/dns-blocklists/adblock/pro.txt
* 	https://raw.githubusercontent.com/StevenBlack/hosts/master/extensions/fakenews/hosts
* 	https://adguardteam.github.io/HostlistsRegistry/assets/filter_9.txt
* 	https://v.firebog.net/hosts/static/w3kbl.txt
* 	https://raw.githubusercontent.com/FadeMind/hosts.extras/master/add.Spam/hosts
* 	https://raw.githubusercontent.com/PolishFiltersTeam/KADhosts/master/KADhosts.txt
* 	https://v.firebog.net/hosts/AdguardDNS.txt
* 	https://raw.githubusercontent.com/PolishFiltersTeam/KADhosts/master/KADhosts.txt
* 	https://v.firebog.net/hosts/AdguardDNS.txt
* 	https://v.firebog.net/hosts/Admiral.txt
* 	https://raw.githubusercontent.com/anudeepND/blacklist/master/adservers.txt
* 	https://raw.githubusercontent.com/DandelionSprout/adfilt/master/Alternate%20versions%20Anti-Malware%20List/AntiMalwareHosts.txt
* 	https://phishing.army/download/phishing_army_blocklist_extended.txt

### Porn
*  https://raw.githubusercontent.com/chadmayfield/pihole-blocklists/master/lists/pi_blocklist_porn_all.list
* https://raw.githubusercontent.com/columndeeply/hosts/main/hosts00
* https://raw.githubusercontent.com/columndeeply/hosts/main/hosts01
* https://raw.githubusercontent.com/columndeeply/hosts/main/hosts02
* https://raw.githubusercontent.com/columndeeply/hosts/main/hosts03
* https://raw.githubusercontent.com/columndeeply/hosts/main/hosts04
* https://raw.githubusercontent.com/columndeeply/hosts/main/hosts05
* 	https://alex.zeitform.de/pihole/pihole-porno.txt

### Social (optional)
* https://raw.githubusercontent.com/StevenBlack/hosts/refs/heads/master/extensions/social/sinfonietta/hosts
