#from luma.core.interface.serial import i2c
#from luma.core.render import canvas
#from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
#from time import sleep

from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.lcd.device import st7789
from time import sleep

import sys
import subprocess
import json, requests

from PIL import Image,ImageDraw,ImageFont

import re

from gpiozero import Button
#from signal import pause

#KEY1   P24     Button 1/GPIO
#KEY2   P23     Button 2/GPIO

def dark():
  print("Button dark erkannt!")
  status["dark"] = not status["dark"]
  if status["dark"]:
      device.hide()
  else:
      device.show() 

def second():
  print("Button second erkannt!")
  status["second"] = not status["second"]
  status["dark"] = False;
  device.show()
  display_update()

status = {"dark": False,
          "second": False}

btn_second = Button(23, bounce_time=0.05)
btn_second.when_pressed = second
btn_dark = Button(24, bounce_time=0.05)
btn_dark.when_pressed = dark

cmd = "ip -br addr show eth0 | awk '{print $3}' | cut -d/ -f1" # only ETH
IPhole = subprocess.check_output(cmd, shell=True, text=True).strip()
if not IPhole:
    IPhole = "192.168.178.80"

print(f"IP: {IPhole}")

#IPhole = "192.168.178.80"
#IPhole = "localhost"
payload = {"password": "uis1pwsb"}   #### FIXME

pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}" # IPv4 regex

size = 32
yaxis = 0
icon_font= ImageFont.truetype('lineawesome-webfont.ttf', size)
#font18 = ImageFont.truetype("PixelOperator.ttf", size)
#font18 = ImageFont.truetype("EBGaramond-Medium.ttf", size-3)
font18 = ImageFont.truetype("RobotoCondensed-Regular.ttf", size-5)
#serial = i2c(port=1, address=0x3C)
#device = ssd1306(serial, rotate=0)

#serial = spi(port=0, device=0, gpio_DC=25, gpio_RST=27)
#device = st7789(serial, width=240, height=320, rotate=1)
#device = st7789(serial, width=240, height=13, rotate=2)

serial = spi(port=0, device=0, gpio_DC=25, gpio_RST=27)
#device = st7789(serial, width=240, height=320, rotate=1)
device = st7789(serial, width=320, height=240, rotate=0)
#device = st7789(serial, width=240, height=135, rotate=0, offset=(40, 53))

# 135x240 offset
OFFSET_X = 40
OFFSET_Y = 53

DEVICE_WIDTH = 240
DEVICE_HEIGHT = 135


def display_update ():
  if not status["dark"]:
    with canvas(device) as draw:
        print("line")
        width, height = draw.im.size
        
        #draw.rectangle(device.bounding_box, outline="hotpink", fill="hotpink")
        draw.rectangle((OFFSET_X, OFFSET_Y, OFFSET_X + DEVICE_WIDTH - 1, OFFSET_Y + DEVICE_HEIGHT - 1), outline="hotpink", fill="hotpink")
        draw.rectangle((OFFSET_X, OFFSET_Y, OFFSET_X + DEVICE_WIDTH - 1, OFFSET_Y + size), outline="red", fill="red")
        
        if not status["second"]:
          draw.text((OFFSET_X + 1, OFFSET_Y + int(0*size)), chr(61931), font=icon_font, fill="white")  # ip
          draw.text((OFFSET_X + 1, OFFSET_Y + 1*size), chr(62171), font=icon_font, fill="white") # cpu
          draw.text((OFFSET_X + DEVICE_WIDTH - 1 - size, OFFSET_Y + 1*size), chr(62153), font=icon_font, fill="white") # temp
          draw.text((OFFSET_X + 1, OFFSET_Y + 2*size), chr(62776), font=icon_font, fill="white") # memory
          draw.text((OFFSET_X + DEVICE_WIDTH - 1 -size, OFFSET_Y + 2*size), chr(0xF007), font=icon_font, fill="white") # clients
          draw.text((OFFSET_X + 1, OFFSET_Y + 3*size), chr(63426), font=icon_font, fill="white") # disk
          draw.text((OFFSET_X + DEVICE_WIDTH - 1 -size, OFFSET_Y + 3*size), chr(62034), font=icon_font, fill="white") # uptime

          draw.text((OFFSET_X + size+6, OFFSET_Y + 0*size-yaxis), str(IP,'utf-8'), font=font18, fill="white") 
          draw.text((OFFSET_X + size+6, OFFSET_Y + 1*size-yaxis), str(CPU,'utf-8') + "%", font=font18, fill="white")
          draw.text((OFFSET_X + DEVICE_WIDTH - 1 -size-3, OFFSET_Y + 1*size-yaxis), str(temp,'utf-8') + "°C", font=font18, fill="white", anchor="ra")
          draw.text((OFFSET_X + size+6, OFFSET_Y + 2*size-yaxis), str(Memuseper,'utf-8') + "%", font=font18, fill="white")
          draw.text((OFFSET_X + DEVICE_WIDTH - 1 -size-3, OFFSET_Y + 2*size-yaxis), str(active_clients), font=font18, fill="white", anchor="ra")
          draw.text((OFFSET_X + size+6, OFFSET_Y + 3*size-yaxis), str(Disk,'utf-8'), font=font18, fill="white")
          draw.text((OFFSET_X + DEVICE_WIDTH - 1 -size-3, OFFSET_Y + 3*size-yaxis), str(uptime,'utf-8'), font=font18, fill="white", anchor="ra")

        else:  
          draw.text((OFFSET_X + 1, OFFSET_Y + int(0*size)), chr(0xF714), font=icon_font, fill="white") # pihole
          draw.text((OFFSET_X + DEVICE_WIDTH - 1 -size, OFFSET_Y + int(0*size)), chr(0xF2ED), font=icon_font, fill="white") # pihole block
          draw.text((OFFSET_X + 1, OFFSET_Y + 1*size), chr(0xF6E2), font=icon_font, fill="white") # cache
          draw.text((OFFSET_X + 1, OFFSET_Y + 2*size), chr(0xF47D), font=icon_font, fill="white") # blocklist
          draw.text((OFFSET_X + 1, OFFSET_Y + 3*size), chr(0xF2F2), font=icon_font, fill="white") # recent blocked
          draw.text((OFFSET_X + size+6, OFFSET_Y + int(0*size)-yaxis), percent_text, font=font18, fill="white")
          draw.text((OFFSET_X + DEVICE_WIDTH - 1 -size-3, OFFSET_Y + int(0*size)-yaxis), str(blocked), font=font18, fill="white", anchor="ra")
          draw.text((OFFSET_X + size+6, OFFSET_Y + 1*size-yaxis), str(cache) + " Cache", font=font18, fill="white")
          draw.text((OFFSET_X + size+6, OFFSET_Y + 2*size-yaxis), str(gravity_size) + " Domains", font=font18, fill="white")
          draw.text((OFFSET_X + size+6, OFFSET_Y + 3*size-yaxis), str(recent_blocked), font=font18, fill="white")

pihole_menu = Image.open("pihole-menu.png").convert("RGBA").resize((240, 60))
backgroud = Image.new("RGBA", device.size, "white")
backgroud.paste(pihole_menu, (OFFSET_X, OFFSET_Y+48), pihole_menu)
draw = ImageDraw.Draw(backgroud)
draw.rectangle((OFFSET_X, OFFSET_Y, OFFSET_X + DEVICE_WIDTH - 1, OFFSET_Y + size), outline="red", fill="red")
draw.text((OFFSET_X + 1, OFFSET_Y + int(0*size)), chr(61931), font=icon_font, fill="white")  # ip
draw.text((OFFSET_X + size+6, OFFSET_Y + 0*size-yaxis), IPhole, font=font18, fill="white") 
          
device.display(backgroud.convert(device.mode))
#print("Anzeige aktualisiert!")
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
  if not status["dark"]:
      if not status["second"]:
        cmd = "ip -br addr show eth0 | awk '{print $3}' | cut -d/ -f1" # only ETH
        IP = subprocess.check_output(cmd, shell = True ) # Register ouput from cmd in var
        #print("+" + str(IP) + "+")
        if not re.search(pattern, str(IP)):
          cmd = "ip -br addr show wlan0 | awk '{print $3}' | cut -d/ -f1" # only WLAN 
          IP = subprocess.check_output(cmd, shell = True ) 
      
        #cmd = "vmstat 4 2|tail -1|awk '{print 100-$15}' | tr -d '\n'" # Takes a second to fetch for accurate cpu usage in %
        cmd = "top -bn2 -d 0.5 | grep 'Cpu(s)' | tail -1 | awk '{print 100-$8}' | tr -d '\n'"
        CPU = subprocess.check_output(cmd, shell = True )
        cmd = "free -m | awk -v CONVFMT='%.1f' 'NR==2{printf $3*100/$2}'"
        Memuseper = subprocess.check_output(cmd, shell = True )
        cmd = "df -h | awk '$NF==\"/\"{printf \"%s\", $5}'"
        Disk = subprocess.check_output(cmd, shell = True )
        cmd = "uptime | awk '{print $3,$4}' | cut -f1 -d','"
        uptime = subprocess.check_output(cmd, shell = True )
        cmd = "cat /sys/class/thermal/thermal_zone*/temp | awk -v CONVFMT='%.1f' '{printf $1/1000}'"
        temp = subprocess.check_output(cmd, shell = True )
      
      if sid:
          url = f"http://{IPhole}/api/padd?sid=" + sid
          response = requests.get(url)
          #print(response.json())
          if response.status_code == 200:
               data = response.json()
               percent_val = data.get('queries', {}).get('percent_blocked', 0.0)
               percent_text = "{:.1f}%".format(percent_val)
               blocked = data.get('queries', {}).get('blocked', 0)
               total = data.get('queries', {}).get('total', 0)
               recent_blocked = data.get('recent_blocked', 0)
               gravity_size = data.get('gravity_size', 0)
               active_clients = data.get('active_clients', 0)
               cache = data.get('cache', {}).get('inserted', 0)
          else:
               print("failed.")

      #response = requests.get("https://alex.zeitform.de/images/moonii.jpg")
      #img = Image.open(BytesIO(response.content))
      #img.show()
      #sleep(3)
      
      display_update()
           
      i = i + 1
      sleep(3)


