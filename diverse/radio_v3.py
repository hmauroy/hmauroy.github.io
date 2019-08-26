#!/usr/bin/python
#
# Script for Raspberry Pi Internet Radio
# 
# Author: Henrik Mauroy 2019
# 
#
# Original Author: Kyle Prier
# Site: http://wwww.youtube.com/meistervision
# 
# LCD author : Matt Hawkins
# Site   : http://www.raspberrypi-spy.co.uk/
# 
# Date   : 10/01/2012
#

# The wiring for the LCD is as follows:
# 1 : GND
# 2 : 5V
# 3 : Contrast (0-5V)*
# 4 : RS (Register Select)
# 5 : R/W (Read Write)       - GROUND THIS PIN
# 6 : Enable or Strobe
# 7 : Data Bit 0             - NOT USED
# 8 : Data Bit 1             - NOT USED
# 9 : Data Bit 2             - NOT USED
# 10: Data Bit 3             - NOT USED
# 11: Data Bit 4
# 12: Data Bit 5
# 13: Data Bit 6
# 14: Data Bit 7
# 15: LCD Backlight +5V**
# 16: LCD Backlight GND

#import
import RPi.GPIO as GPIO
import time
import os
import re


# Define GPIO to LCD mapping
LCD_RS = 26
LCD_E  = 19
LCD_D4 = 13 
LCD_D5 = 6
LCD_D6 = 21
LCD_D7 = 20

# Default GPIO for Radio Controls
NEXT = 18	# Next radio station
PREV = 17	# Previous radio station
OnOff = 3	# Turn on/off RPi
RadioOnOff = 22 # Start/stop the internet radio
RestartSpotify = 23 # Restart the spotify service
RebootMe = 24	# Reboot the RPi

# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
#LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line    #No 3rd line
#LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line    #No 4th line

# Timing constants
E_PULSE = 0.00005
E_DELAY = 0.00005

def main():
  # Main program block
  GPIO.cleanup()               # Clean up GPIO if any pins are still in use
  GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
  GPIO.setup(LCD_E, GPIO.OUT)  # E
  GPIO.setup(LCD_RS, GPIO.OUT) # RS
  GPIO.setup(LCD_D4, GPIO.OUT) # DB4
  GPIO.setup(LCD_D5, GPIO.OUT) # DB5
  GPIO.setup(LCD_D6, GPIO.OUT) # DB6
  GPIO.setup(LCD_D7, GPIO.OUT) # DB7
  
  GPIO.setup(NEXT, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Next Channel button, PUD_UP = Pull-up resistor so the GPIO stays at 3.3V
  GPIO.setup(PREV, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Buttons are connected to GPIO and other side is GND
  GPIO.setup(OnOff, GPIO.IN)	# External pul-up is fitted to this pin, no need to enable pul-up from software
  GPIO.setup(RadioOnOff, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(RestartSpotify, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(RebootMe, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  
  # Initialise display
  lcd_init()
  # Send some test
  lcd_byte(LCD_LINE_1, LCD_CMD)
  lcd_string("ANINE",2)
  lcd_byte(LCD_LINE_2, LCD_CMD)
  lcd_string("Internet Radio",2)
  #lcd_byte(LCD_LINE_3, LCD_CMD)	# No line 3 with 16x2 LCD
  #lcd_string("by",2)
  #lcd_byte(LCD_LINE_4, LCD_CMD)
  #lcd_string("Meister Vision", 2)	 
  time.sleep(1) 
  os.system("mpc play")
  mpc_plays = 1    # Sets a variable so the program knows that it's playing from mpc
  
  # If we use volume controls (without amplifier) this should be shown in the display
  # str1 = os.popen("amixer cget numid=6 | grep -i ': values='").read()   # .read() reads the output from terminal
  # m = re.search('values=(.+?),', str1)
  # tall = m.group(1) + '\n'
  # vol = int(tall)
  # vol=100*vol/151
  # if vol == 100:
      # print "  Volume=MAX"
  # elif vol == 0:
      # print "  Volume=MIN"
  # else:
      # print "  Volume=" + str(vol) + "%"
          
  while 1:
      if ( GPIO.input(NEXT) == False):
          os.system("mpc next")
          time.sleep(0.2)
          os.system("mpc play")

      if ( GPIO.input(PREV) == False):
          os.system("mpc prev")
          time.sleep(0.2)
          os.system("mpc play")

      if ( GPIO.input(OnOff) == False):
          mpc_plays = 0
          os.system("mpc stop")
          for i in range(1,6):
              print("Shutting down in " + str(6-i) + " sec")
              lcd_byte(LCD_LINE_1, LCD_CMD)
              lcd_string("Shutdown in " + str(6-i) + " sec",1)
              lcd_byte(LCD_LINE_2, LCD_CMD)
              lcd_string("",1)
              time.sleep(1)
          os.system("sudo shutdown -h now")

      if ( GPIO.input(RadioOnOff) == False):
          mpc_plays = 0
          os.system("mpc stop")
          os.system("sudo systemctl restart raspotify")	# restarts the spotify service
          lcd_byte(LCD_LINE_1, LCD_CMD)
          lcd_string("Volumio running",2)
          lcd_byte(LCD_LINE_2, LCD_CMD)
          lcd_string("Radio OFF",2)

      if ( GPIO.input(RestartSpotify) == False):
          os.system("sudo systemctl restart raspotify")	# restarts the spotify service
          for i in range(1,6):
              print("Restarts spotify in" + str(6-i) + " sec")
              lcd_byte(LCD_LINE_1, LCD_CMD)
              lcd_string("Restarts spotify",1)
              lcd_byte(LCD_LINE_2, LCD_CMD)
              lcd_string(str(6-i,2))
              time.sleep(1)
          lcd_byte(LCD_LINE_1, LCD_CMD)
          lcd_string("Volumio running",2)
          lcd_byte(LCD_LINE_2, LCD_CMD)
          lcd_string("Radio OFF",2)

      if ( GPIO.input(RebootMe) == False):
          print("Rebooting")
          lcd_byte(LCD_LINE_1, LCD_CMD)
          lcd_string("Rebooting...",1)
          lcd_byte(LCD_LINE_2, LCD_CMD)
          lcd_string(str("",2))
          os.system("sudo shutdown -r now")

      if mpc_plays == 1:
          f=os.popen("mpc current")
          station = ""
          for i in f.readlines():
              station += i
              # Send some text
              lcd_byte(LCD_LINE_1, LCD_CMD)
              lcd_string(station,1)
              lcd_byte(LCD_LINE_2, LCD_CMD)
              lcd_string("",1)

  time.sleep(10)    # Updates the display for internetradio

def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD)
  lcd_byte(0x32,LCD_CMD)
  lcd_byte(0x28,LCD_CMD)
  lcd_byte(0x0C,LCD_CMD)  
  lcd_byte(0x06,LCD_CMD)
  lcd_byte(0x01,LCD_CMD)  

def lcd_string(message,style):
  # Send string to display
  # style=1 Left justified
  # style=2 Centred
  # style=3 Right justified

  if style==1:
    message = message.ljust(LCD_WIDTH," ")  
  elif style==2:
    message = message.center(LCD_WIDTH," ")
  elif style==3:
    message = message.rjust(LCD_WIDTH," ")

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command

  GPIO.output(LCD_RS, mode) # RS

  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  time.sleep(E_DELAY)    
  GPIO.output(LCD_E, True)  
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)  
  time.sleep(E_DELAY)      

  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  time.sleep(E_DELAY)    
  GPIO.output(LCD_E, True)  
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)  
  time.sleep(E_DELAY)   

if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    time.sleep(0.1)
    os.system("mpc stop")
    time.sleep(0.1)
    lcd_init()
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string("Anine  &",1)
    lcd_byte(LCD_LINE_2, LCD_CMD)
    lcd_string("Henrik!",3)
    GPIO.cleanup()
