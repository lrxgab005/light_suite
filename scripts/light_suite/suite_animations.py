# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various colors and animations
import time

from neopixel import *

import numpy as np


# LED strip configuration:
LED_PER_METER  = 30		 # Number of LEDs per meter
LED_COUNT      = 120      # Number of LED pixels.
LED_PIN        = 12      # GPIO pin connected to the pixels (12 & 18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequenpcy in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 50     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_BGR   # Strip type and colour ordering
TIME_START	   = time.time() 


def hexToRGB(h):
	h = h.lstrip('#')
	h = tuple(int(h[i:i+2], 16) for i in (0, 2 ,4))
	return h[0], h[1], h[2]

# Define functions which animate LEDs in various ways. 
def setColor(strip, color):
	"""Wipe color across display a pixel at a time."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
	strip.show()
	time.sleep(wait_ms/1000.0)


# p(t) = color * ((sin([rad/s] * [s] * [pixNr] * [m / pix] + 1) / 2)
def sinWave(strip, px_range, colorList, freq=10, period_meters=1, offset=0):  # f defines the rate at which the wave moves. period_meters the period of sine wave in meter
	t = time.time() - TIME_START  # Time in secs since epoch
	d = float(1.0 / LED_PER_METER)	# m per pixel
	reds = []
	print("#######################################")
	for i in px_range:
		func = ((np.sin( (2 * np.pi) * freq * t * (i * d * period_meters) + offset ) + 1) / 2)
		print(int(colorList[2] * func))
		r, g, b = int(colorList[0]), int(colorList[1]), int(colorList[2] * func)
		reds.append(r)
		color = Color(r, g, b)
		strip.setPixelColor(i, color)
	print("#######################################")
	
	strip.show()
	# print(reds)

def theaterChase(strip, color, wait_ms=50, iterations=10):
	"""Movie theater light style chaser animation."""
	for j in range(iterations):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, color)
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)

def centreRun(strip, color1, color2, wait_ms=50, iterations=10, dir=1):
	"""Movie theater light style chaser animation."""
	for j in range(iterations):
		for q in range(3):
			if dir>0:
				q=3-q
			for i in range(0, strip.numPixels()/2, 3):
				strip.setPixelColor(i+q, color1)
				strip.setPixelColor(strip.numPixels() - i - q, color1)


			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels()/2, 3):
				strip.setPixelColor(i+q, color2)
				strip.setPixelColor(strip.numPixels() - i - q, color2)

def setSymetricPixels(strip, px_range, incr, limits, color1, color2):
	for idx, i in enumerate(px_range[0]):
		ledNr = i + incr
		if i + incr < limits[0]:
			strip.setPixelColor(ledNr, color1)

		ledNr = i + incr + 1
		if ledNr < limits[0]:
			strip.setPixelColor(ledNr, color1)

		ledNr = i + incr + 2
		if ledNr < limits[0]:
			strip.setPixelColor(ledNr, color2)

		ledNr = px_range[1][idx] - incr
		if ledNr >= limits[1]:
			strip.setPixelColor(ledNr, color1)

		ledNr = px_range[1][idx] - incr + 1
		if ledNr >= limits[1]:
			strip.setPixelColor(ledNr, color1)

		ledNr = px_range[1][idx] - incr + 2
		if ledNr >= limits[1]:
			strip.setPixelColor(ledNr, color2)

def centreRunLS(strip, color1, color2, wait_ms=50, iterations=10, dir=1):

	under_arms = [list(range(6, 40, 3)), [x+2 for x in reversed(range(81, 115, 3))]]
	top_arms = [list(range(60, 81, 3)), [x+1 for x in reversed(range(40, 59, 3))]]
	waist = [list(range(114, 120, 3)), [x+2 for x in reversed(range(0, 6, 3))]]

	for j in range(iterations):
		for q in range(3):
			if dir>0:
				q=3-q

			# sinWave(strip, under_arms[0], [100, 0, 100])
			# sinWave(strip, top_arms[0], [100, 0, 100])
			# sinWave(strip, waist[0], [100, 0, 100])

			# sinWave(strip, under_arms[1], [100, 0, 100])
			# sinWave(strip, top_arms[1], [100, 0, 100])
			# sinWave(strip, waist[1], [100, 0, 100])


			setSymetricPixels(strip, under_arms, q, [40, 81], color1, color2)
			setSymetricPixels(strip, top_arms, q, [81, 40], color1, color2)
			setSymetricPixels(strip, waist, q, [120, 0], color1, color2)

			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i + q, 0)

# Main program logic follows:
if __name__ == '__main__':
	# Load config
	with open('config.txt', 'r') as file:
		config = file.readlines()
	# Create NeoPixel object with appropriate configuration.
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
	# Intialize the library (must be called once before other functions).
	strip.begin()

	if config[0][0] == '#':
		r, g, b = hexToRGB(config[0])
	else:
		r, g, b = list(map(int, config[0].split(",")))

	if config[1][0] == '#':
		r2, g2, b2 = hexToRGB(config[1])
	else:
		r2, g2, b2 = list(map(int, config[1].split(",")))

	print("Color 1 RGB: ", r, g, b)
	print("Color 2 RGB: ", r2, g2, b2)
	delay=int(config[2])
	dir=int(config[3])
	
	print('Press Ctrl-C to quit.')
	while True:
		centreRunLS(strip, Color(r, g, b), Color(r2, g2, b2), delay, 1000, dir)  # Red wipe
		# sinWave(strip, [r, g, b])
