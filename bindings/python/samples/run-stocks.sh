#!/bin/bash
sudo python3 /home/dietpi/ledmatrix/bindings/python/samples/stocks.py --led-gpio-mapping adafruit-hat --led-slowdown-gpio 1 -r 32 --led-cols 64 -c 2 --led-pixel-mapper "U-mapper;Rotate:270" --led-brightness 50 
