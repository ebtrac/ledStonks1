#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
import time
from weatherapi.weatherapi_client import WeatherapiClient
import textwrap
from justifytext import justify

key = "c4088e6598464c8bad3162356211207"
client = WeatherapiClient(key)
weather = client.ap_is
forecast = weather.get_forecast_weather("Louisville", 3)

class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.line_number = 0
        self.col_number = 0
    
    def ledprint(self, s, color="white", spacing=3):
        def refresh_xoffset():
            return self.col_number * self.font.CharacterWidth(ord('X'))
        xoffset = refresh_xoffset()
        # process the color because the python binding won't accept lists or tuples... smh
        _r = self.hue[color][0]
        _g = self.hue[color][1]
        _b = self.hue[color][2]
        color = graphics.Color(_r, _g, _b)
        
        if type(s) is str:
            for c in s:
                if c == '\n':
                    self.line_number += 1
                    self.col_number = 0
                else:
                    yoffset = (1+self.line_number) * self.font.height + spacing * self.line_number
                    graphics.DrawText(self.offscreen_canvas, self.font, xoffset, yoffset, color, str(c))
                    self.col_number += 1
                xoffset = refresh_xoffset()
        else:
            return
        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)

    def ledprintln(self, s, color="white", spacing=3):
        xoffset = self.col_number * self.font.CharacterWidth(ord('X'))
        # process the color because the python binding won't accept lists or tuples... smh
        _r = self.hue[color][0]
        _g = self.hue[color][1]
        _b = self.hue[color][2]
        color = graphics.Color(_r, _g, _b)

        if type(s) is str:
            lines = s.split("\n")
            for line in lines:
                yoffset = (1+self.line_number) * self.font.height + spacing * self.line_number
                graphics.DrawText(self.offscreen_canvas, self.font, xoffset, yoffset, color, line)
                self.line_number += 1
        elif type(s) is list:
            for line in s:
                yoffset = (1+self.line_number) * self.font.height + spacing * self.line_number
                graphics.DrawText(self.offscreen_canvas, self.font, xoffset, yoffset, color, line)
                self.line_number += 1
        else:
            return
                
        self.col_number = 0
        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)

    def clear_screen(self):
        self.line_number = 0
        self.col_number = 0
        self.offscreen_canvas.Clear()
        self.matrix.SwapOnVSync(self.offscreen_canvas)

    def run(self):
        #Init canvas
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()
        self.matrix.SwapOnVSync(self.offscreen_canvas)
        #Init variables
        self.font = graphics.Font()
        self.font.LoadFont("/home/dietpi/ledmatrix/fonts/4x6.bdf")
        self.textColor = graphics.Color(255, 255, 0)
        self.hue = {
                "white" : [255, 255, 255],
                "red" : [255, 0, 0],
                "orange" : [255, 127, 0],
                "yellow" : [255, 255, 0],
                "lightgreen" : [127, 255, 0],
                "green" : [0, 255, 0],
                "cyan" : [0, 255, 255],
                "lightblue" : [0, 127, 255],
                "blue" : [0, 0, 255],
                "magenta" : [255, 0, 255],
                "violet" : [127, 0, 255],
                "gray" : [127, 127, 127],
                "grey" : [127, 127, 127],
                "black" : [0, 0, 0]
        }

        while True:
            """
            #color test with ledprint
            for x in self.hue:
                self.ledprint("X", color=x)
            self.ledprintln("")
            self.ledprint("hey there\nwhats up")
            self.ledprintln(" line")
            self.ledprint("newline here?")
            time.sleep(1)
            self.clear_screen()
            #color test
            for x in self.hue:
                self.ledprintln(x, color=x, spacing=0)
            time.sleep(7)
            self.clear_screen()
            x="magenta"
            self.ledprintln(x, color=x, spacing=0)
            x="violet"
            self.ledprintln(x, color=x, spacing=0)
            x="grey"
            self.ledprintln(x, color=x, spacing=0)
            x="black"
            self.ledprintln(x, color=x, spacing=0)
            time.sleep(7)
            self.clear_screen()
            
            #test character alignment
            self.ledprint("HELLO - print\n")
            self.ledprintln("HELLO - println")
            time.sleep(7)
            self.clear_screen()
            """

            #Units
            degreesymbol = chr(176)
            tempunit = ' ' + "F"
            humidityunit = "%"
            speedunit = " MPH"
            rainunit = "MM"

            #Weather Right Now
            cast = forecast.forecast.forecastday[0]
            temp = str(round(forecast.current.temp_f)) 
            condition = forecast.current.condition.text.upper()
            feel = str(round(forecast.current.feelslike_f)) 
            humidity = str(round(forecast.current.humidity)) 
            windspeed = str(round(forecast.current.wind_mph)) 
            windheading = str(forecast.current.wind_dir) 

            #self.ledprintln(justify(text, 16, justify_last_line=True))
            self.ledprintln("NOW   " + cast.date)
            self.ledprintln(condition, color="lightblue")
            self.ledprint("TEMP:", color="grey")
            self.ledprintln(temp + tempunit, color="lightgreen")
            self.ledprint("FEEL:", color="grey")
            self.ledprintln(feel + tempunit, color="lightgreen")
            self.ledprint("HMDTY:", color="grey")
            self.ledprintln(humidity + humidityunit, color="lightgreen")
            self.ledprint("WIND:", color="grey")
            self.ledprintln(windspeed + speedunit + " " + windheading, color="lightgreen")
            time.sleep(7)
            self.clear_screen()
            
            #Today's Forecast
            cast = forecast.forecast.forecastday[0]
            condition = cast.day.condition.text.upper() 
            tempmin = str(round(cast.day.mintemp_f)) 
            tempmax = str(round(cast.day.maxtemp_f)) 
            avgtemp = str(round(cast.day.avgtemp_f)) 
            humidity = str(round(cast.day.avghumidity))
            windspeedmax = str(round(cast.day.maxwind_mph)) 
            uv =  str(round(cast.day.uv))
            rain_raw = cast.day.totalprecip_mm
            rain = str(round(cast.day.totalprecip_mm)) 
            will_it_rain = cast.day.totalprecip_mm > 0
             
            self.ledprintln("TODAY " + cast.date)
            self.ledprintln(condition, color="lightblue")
            self.ledprint("TEMP:", color="grey")
            #self.ledprintln(tempmin + "/" + tempmax + tempunit, color="lightgreen")
            self.ledprint(tempmin, color="blue")
            self.ledprint(" / ", color="grey")
            self.ledprintln(tempmax + tempunit, color="orange")
            self.ledprint("AVG:", color="grey")
            self.ledprintln(avgtemp + tempunit, color="lightgreen")
            self.ledprint("HMDTY:", color="grey")
            self.ledprintln(humidity + humidityunit, color="lightgreen")
            self.ledprint("WIND:", color="grey")
            self.ledprintln(windspeedmax + speedunit + " MAX", color="lightgreen")
            self.ledprint("UV:", color="grey")
            self.ledprint(uv, color="lightgreen")
            if will_it_rain:
                self.ledprint(" RAIN:", color="grey")
                if rain_raw < 1:
                    self.ledprint("<1" + rainunit, color="lightgreen")
                else:
                    self.ledprint(rain + rainunit, color="lightgreen")
            time.sleep(7)
            self.clear_screen()
            
            #Tomorrow's Forecast
            cast = forecast.forecast.forecastday[1]
            condition = cast.day.condition.text.upper() 
            tempmin = str(round(cast.day.mintemp_f)) 
            tempmax = str(round(cast.day.maxtemp_f)) 
            avgtemp = str(round(cast.day.avgtemp_f)) 
            humidity = str(round(cast.day.avghumidity))
            windspeedmax = str(round(cast.day.maxwind_mph)) 
            uv =  str(round(cast.day.uv))
            rain_raw = cast.day.totalprecip_mm
            rain = str(round(cast.day.totalprecip_mm)) 
            will_it_rain = cast.day.totalprecip_mm > 0
             
            self.ledprintln("TOMRO " + cast.date)
            self.ledprintln(condition, color="lightblue")
            self.ledprint("TEMP:", color="grey")
            #self.ledprintln(tempmin + "/" + tempmax + tempunit, color="lightgreen")
            self.ledprint(tempmin, color="blue")
            self.ledprint(" / ", color="grey")
            self.ledprintln(tempmax + tempunit, color="orange")
            self.ledprint("AVG:", color="grey")
            self.ledprintln(avgtemp + tempunit, color="lightgreen")
            self.ledprint("HMDTY:", color="grey")
            self.ledprintln(humidity + humidityunit, color="lightgreen")
            self.ledprint("WIND:", color="grey")
            self.ledprintln(windspeedmax + speedunit + " MAX", color="lightgreen")
            self.ledprint("UV:", color="grey")
            self.ledprint(uv, color="lightgreen")
            if will_it_rain:
                self.ledprint(" RAIN:", color="grey")
                if rain_raw < 1:
                    self.ledprint("<1" + rainunit, color="lightgreen")
                else:
                    self.ledprint(rain + rainunit, color="lightgreen")
            time.sleep(7)
            self.clear_screen()

            #Threemorrow's Forecast
            cast = forecast.forecast.forecastday[2]
            condition = cast.day.condition.text.upper() 
            tempmin = str(round(cast.day.mintemp_f)) 
            tempmax = str(round(cast.day.maxtemp_f)) 
            avgtemp = str(round(cast.day.avgtemp_f)) 
            humidity = str(round(cast.day.avghumidity))
            windspeedmax = str(round(cast.day.maxwind_mph)) 
            uv =  str(round(cast.day.uv))
            rain_raw = cast.day.totalprecip_mm
            rain = str(round(cast.day.totalprecip_mm)) 
            will_it_rain = cast.day.totalprecip_mm > 0
             
            self.ledprintln("3-MRO " + cast.date)
            self.ledprintln(condition, color="lightblue")
            self.ledprint("TEMP:", color="grey")
            #self.ledprintln(tempmin + "/" + tempmax + tempunit, color="lightgreen")
            self.ledprint(tempmin, color="blue")
            self.ledprint(" / ", color="grey")
            self.ledprintln(tempmax + tempunit, color="orange")
            self.ledprint("AVG:", color="grey")
            self.ledprintln(avgtemp + tempunit, color="lightgreen")
            self.ledprint("HMDTY:", color="grey")
            self.ledprintln(humidity + humidityunit, color="lightgreen")
            self.ledprint("WIND:", color="grey")
            self.ledprintln(windspeedmax + speedunit + " MAX", color="lightgreen")
            self.ledprint("UV:", color="grey")
            self.ledprint(uv, color="lightgreen")
            if will_it_rain:
                self.ledprint(" RAIN:", color="grey")
                if rain_raw < 1:
                    self.ledprint("<1" + rainunit, color="lightgreen")
                else:
                    self.ledprint(rain + rainunit, color="lightgreen")
            time.sleep(7)
            self.clear_screen()

# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()
