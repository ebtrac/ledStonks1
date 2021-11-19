#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
import time
#import yfinance as yf

#stocks = 'MSFT'
#data = yf.download(tickers = stocks, period='1d',interval='1m')

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
        
    def graph(self, xvalues, yvalues):
        #graphics.DrawLine(self.offscreen_canvas, xvalues[i], yvalues[i], xvalues[i+6], yvalues[i+1]
        pass

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

        self.ledprintln("stonks :)")
        colorstr = "red"
        _r = self.hue[colorstr][0]
        _g = self.hue[colorstr][1]
        _b = self.hue[colorstr][2]
        color = graphics.Color(_r, _g, _b)
        graphics.DrawLine(self.offscreen_canvas,0,0, 20, 30, color) 
        graphics.DrawLine(self.offscreen_canvas,20,30, 40, 10, color) 
        graphics.DrawLine(self.offscreen_canvas,40,10, 63, 63, color) 

        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
        while True:
            pass
        self.clear_screen()

# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()
