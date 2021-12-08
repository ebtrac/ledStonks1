#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
import time
import yfinance as yf

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
        
    def graph(self, dat, graph_height, graph_width, xoff, yoff):
        opens = dat['Open']
        # scale between 0 and graph_height
        scl_opens = opens - min(opens)
        scl_opens = round(scl_opens * graph_height/ max(scl_opens))
        # draw axes
        colorstr = 'blue'
        _r = self.hue[colorstr][0]
        _g = self.hue[colorstr][1]
        _b = self.hue[colorstr][2]
        color = graphics.Color(_r, _g, _b)
        self.line(xoff, yoff+graph_height, graph_width, yoff+graph_height, color)
        self.line(xoff, yoff+graph_height, xoff, yoff, color)

        for x in range(len(scl_opens)):
            y1 = graph_height - scl_opens[x]
            xstep = round(graph_width / len(scl_opens))
            xscl = x * xstep
            try:
                y2 = graph_height - scl_opens[x+1]
            except:
                return

            if y2 < y1:
                colorstr = 'green'
            if y2 > y1:
                colorstr = 'red'
            if y2 == y1:
                colorstr = 'white'
            _r = self.hue[colorstr][0]
            _g = self.hue[colorstr][1]
            _b = self.hue[colorstr][2]
            color = graphics.Color(_r, _g, _b)
            self.line(xscl+xoff, y1+yoff, xscl+xstep+xoff, y2+yoff, color)

    def line(self, x1,y1,x2,y2, color):
        graphics.DrawLine(self.offscreen_canvas,x1,y1,x2,y2, color) 
        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)

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
        stockname = "BFS"
        per = "1h"
        inter = "1m"
        data = yf.download(tickers=stockname,period=per, interval=inter)
        self.graph(data, 32, 64, 0, 31)
        self.ledprintln("Open:"+str(round(data.get("Open")[0], 2)), spacing=1)
        self.ledprintln("Current:"+str(round(data.get("Open")[-1], 2)), spacing=1)
        self.ledprintln("Max:"+str(round(max(data.get("Open")), 2)), spacing=1)
        self.ledprintln("Min:"+str(round(min(data.get("Open")), 2)), spacing=1)
        self.ledprintln(stockname + ' ' + per, spacing=1)
        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
        time.sleep(60)
        self.clear_screen()
        return

# Main function
if __name__ == "__main__":
    while True:
        run_text = RunText()
        if (not run_text.process()):
            run_text.print_help()
