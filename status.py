from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
from time import sleep

import sys
import subprocess
import json, requests
from PIL import Image,ImageDraw,ImageFont

import re

IPhole = "192.168.178.80"
#IPhole = "localhost"
payload = {"password": "uis1pwsb"}   #### FIXME

pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}" # IPv4 regex

icon_font= ImageFont.truetype('lineawesome-webfont.ttf', 16)
font18 = ImageFont.truetype("PixelOperator.ttf", 16)

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, width=128, height=32, rotate=2)

img_path = "pihole-menu-oled.png"
logo = Image.open(img_path).convert("1")  # Zu 1-Bit (Monochrom) konvertieren

device.display(logo)
sleep(3)

url = f"http://{IPhole}/api/auth"
response = requests.post(url, json=payload)
#print(response.json())

if response.status_code == 200:
  data = response.json()
  sid = data.get("session", {}).get("sid")
      
  sid and print(f"Erfolgreich angemeldet! Deine SID ist: {sid}") 
else:
  print(f"Fehler beim Login: {response.status_code}")
  print(response.text)

i = 0
while True:
    
  if (not i%2):

      cmd = "ip -br addr show eth0 | awk '{print $3}' | cut -d/ -f1" # only ETH
      IP = subprocess.check_output(cmd, shell = True ) # Register ouput from cmd in var
      #print("+" + str(IP) + "+")
      if not re.search(pattern, str(IP)):
          cmd = "ip -br addr show wlan0 | awk '{print $3}' | cut -d/ -f1" # only WLAN 
          IP = subprocess.check_output(cmd, shell = True ) 
      
      cmd = "cat /sys/class/thermal/thermal_zone*/temp | awk -v CONVFMT='%.1f' '{printf $1/1000}'"
      temp = subprocess.check_output(cmd, shell = True )
      
      if sid:
          #print(f"Erfolgreich angemeldet! Deine SID ist: {sid}")

          url = f"http://{IPhole}/api/stats/summary?sid=" + sid
          response = requests.get(url)
          #print(response.json())
          if response.status_code == 200:
              data = response.json()
              percent_val = data.get('queries', {}).get('percent_blocked', 0.0)
              percent_text = "{:.1f}%".format(percent_val)
              #blocked = data.get('queries', {}).get('blocked', 0)
              #total = data.get('queries', {}).get('total', 0)
          else:
              print("failed.")


  else:
      ##cmd = "free -m | awk 'NR==2{printf $3}'| awk '{printf $1/1000}'"
      #cmd = "free -m | awk 'NR==2{printf $3}'| awk '{printf $1}'"
      #Memuse = subprocess.check_output(cmd, shell = True )
      #cmd = "cat /proc/meminfo | head -n 1 | awk -v CONVFMT='%.0f' '{printf $2/1000000}'"
      #MemTotal = subprocess.check_output(cmd, shell = True )
      cmd = "free -m | awk -v CONVFMT='%.1f' 'NR==2{printf $3*100/$2}'"
      Memuseper = subprocess.check_output(cmd, shell = True )
      cmd = "df -h | awk '$NF==\"/\"{printf \"%s\", $5}'"
      Disk = subprocess.check_output(cmd, shell = True )
      cmd = "uptime | awk '{print $3,$4}' | cut -f1 -d','"
      uptime = subprocess.check_output(cmd, shell = True )
    
      #cmd = "vmstat 4 2|tail -1|awk '{print 100-$15}' | tr -d '\n'" # Takes a second to fetch for accurate cpu usage in %
      cmd = "top -bn2 -d 0.5 | grep 'Cpu(s)' | tail -1 | awk '{print 100-$8}' | tr -d '\n'"
      CPU = subprocess.check_output(cmd, shell = True )
  
  with canvas(device) as draw:
    print("line")
    #draw.rectangle(device.bounding_box, outline="white", fill="black")
    
    #draw.text((10, 40), "Hello World" + str(i), font=font18, fill="white")

    if (not i%2):
        draw.text((1, 0), chr(61931), font=icon_font, fill="white")  # ip
        #draw.text((1, 16), chr(62171), font=icon_font, fill="white") # cpu
        draw.text((1, 16), chr(0xF714), font=icon_font, fill="white") # pihole
        draw.text((111, 16), chr(62153), font=icon_font, fill="white") # temp

        draw.text((22, 0), str(IP,'utf-8'), font=font18, fill="white") 
        #draw.text((22, 16), str(CPU,'utf-8') + "%", font=font18, fill="white")
        draw.text((22, 16), percent_text, font=font18, fill="white")
        draw.text((107, 16), str(temp,'utf-8') + "°C", font=font18, fill="white", anchor="ra")

    else:
        draw.text((1, 0), chr(62776), font=icon_font, fill="white") # memory
        #draw.text((111, 0), chr(0xF714), font=icon_font, fill="white") # pihole
        draw.text((111, 0), chr(62171), font=icon_font, fill="white") # cpu
        draw.text((1, 16), chr(63426), font=icon_font, fill="white") # disk
        draw.text((111, 16), chr(62034), font=icon_font, fill="white") # uptime

        draw.text((22, 0), str(Memuseper,'utf-8') + "%", font=font18, fill="white")
        #draw.text((107, 0), percent_text, font=font18, fill="white", anchor="ra")
        draw.text((107, 0), str(CPU,'utf-8') + "%", font=font18, fill="white", anchor="ra")
        draw.text((22, 16), str(Disk,'utf-8'), font=font18, fill="white")
        draw.text((107, 16), str(uptime,'utf-8'), font=font18, fill="white", anchor="ra")

    
    #draw.text((22, 0), str(IP,'utf-8'), font=font18, fill="white") 
    #draw.text((22, 16), str(CPU,'utf-8') + "%", font=font18, fill="white")
    #draw.text((107, 16), str(temp,'utf-8') + "°C", font=font18, fill="white", anchor="ra")
    #draw.text((22, 32), str(Memuseper,'utf-8') + "%", font=font18, fill="white")
    #draw.text((107, 32), percent_text, font=font18, fill="white", anchor="ra")
    #draw.text((22, 48), str(Disk,'utf-8'), font=font18, fill="white")
    #draw.text((107, 48), str(uptime,'utf-8'), font=font18, fill="white", anchor="ra")

    i = i + 1
  sleep(5)
