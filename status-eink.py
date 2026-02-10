import os
import time
import sys
import subprocess
import json, requests
from waveshare_epd import epd2in13_V4
from PIL import Image, ImageDraw, ImageFont
import re

cmd = "ip -br addr show eth0 | awk '{print $3}' | cut -d/ -f1" # only ETH
IPhole = subprocess.check_output(cmd, shell=True, text=True).strip()
if not IPhole:
    IPhole = "192.168.178.80"
print(f"IP: {IPhole}")

payload = {"password": "uis1pwsb"}   #### FIXME
pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}" # IPv4 regex

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

try:
    epd = epd2in13_V4.EPD()
    epd.init()
    epd.Clear(0xFF)    
    
    canvas = Image.new('1', (epd.height, epd.width), 255).rotate(90, expand=True)
    draw = ImageDraw.Draw(canvas)
    
    logo = Image.open('pihole-menu-122x38.png').convert('1').resize((122, 38))
    
    canvas.paste(logo, (0, 2))

    size = 22
    yaxis = 2
    icon_font= ImageFont.truetype('lineawesome-webfont.ttf', size)
    
    try:
        font18 = ImageFont.truetype('RobotoCondensed-Regular.ttf', 18)
        #font18 = ImageFont.truetype('EBGaramond-Regular.ttf', 19)
    except:
        font18 = ImageFont.load_default()

    #font2 = ImageFont.truetype('PixelOperator.ttf', 20)
    #font3 = ImageFont.truetype('RobotoCondensed-Regular.ttf', 18)

    draw.line((0, 1, epd.width, 1), fill=0, width=1)
    draw.line((0, 41, epd.width, 41), fill=0, width=1)
    
    draw.text((0, 67), chr(62171), font=icon_font, fill=0) # cpu
    draw.text((0, 87), chr(62776), font=icon_font, fill=0) # memory
    draw.text((0, 107), chr(63426), font=icon_font, fill=0) # disk
    draw.text((0, 127), chr(62153), font=icon_font, fill=0) # temp
    draw.text((0, 147), chr(0xF007), font=icon_font, fill=0) # clients
    draw.text((0, 167), chr(62034), font=icon_font, fill=0) # uptime 
    draw.text((0, 187), chr(0xF714), font=icon_font, fill=0) # pihole
    draw.text((0, 207), chr(0xF47D), font=icon_font, fill=0) # blocklist
    draw.text((0, 227), chr(0xF2F2), font=icon_font, fill=0)
  
    epd.displayPartBaseImage(epd.getbuffer(canvas))

    i = 0
    while True:
      cmd = "ip -br addr show eth0 | awk '{print $3}' | cut -d/ -f1" # only ETH
      IP = subprocess.check_output(cmd, shell = True ) # Register ouput from cmd in val
      if not re.search(pattern, str(IP)):
          cmd = "ip -br addr show wlan0 | awk '{print $3}' | cut -d/ -f1" # only WLAN 
          IP = subprocess.check_output(cmd, shell = True ) 
     
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
               #blocked = data.get('queries', {}).get('blocked', 0)
               #total = data.get('queries', {}).get('total', 0)
               recent_blocked = data.get('recent_blocked', 0)
               gravity_size = data.get('gravity_size', 0)
               active_clients = data.get('active_clients', 0)
               #cache = data.get('cache', {}).get('inserted', 0)
          else:
               print("failed.")

      draw.rectangle((size+2, 48, 122, 250), fill=255)
      
      draw.text((0, 40+yaxis), IP, font=font18, fill=0)
      draw.text((size+3, 67+yaxis), str(CPU, 'utf-8') + "%", font=font18, fill=0)
      draw.text((size+3, 87+yaxis), str(Memuseper, 'utf-8') + "%", font=font18, fill=0)
      draw.text((size+3, 107+yaxis), str(Disk, 'utf-8'), font=font18, fill=0)
      draw.text((size+3, 127+yaxis), str(temp, 'utf-8') + "°C", font=font18, fill=0)
      draw.text((size+3, 147+yaxis), str(active_clients), font=font18, fill=0)
      draw.text((size+3, 167+yaxis), str(uptime, 'utf-8'), font=font18, fill=0)
      draw.text((size+3, 187+yaxis), percent_text, font=font18, fill=0)
      draw.text((size+3, 207+yaxis), str(gravity_size), font=font18, fill=0)
      draw.text((size+3, 227+yaxis), str(recent_blocked), font=font18, fill=0)

      epd.displayPartial(epd.getbuffer(canvas))
      #epd.display_fast(epd.getbuffer(canvas))
      if i % 100 == 0 and i > 0:
        epd.displayPartBaseImage(epd.getbuffer(canvas))
      
      time.sleep(5)
      i = i+ 1

except KeyboardInterrupt:
    print("Programm beendet durch Nutzer")
    epd.sleep()
    # Wichtig: GPIOs freigeben
    from waveshare_epd import epdconfig
    epdconfig.module_exit()


