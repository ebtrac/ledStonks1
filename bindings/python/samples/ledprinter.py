#!/usr/bin/env python3
# Just print shit to the led matrix
from samplebase import SampleBase
from rgbmatrix import graphics
import time
import textwrap 
from justifytext import justify

class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.line_number = 0
        
    def ledprintln(self, s):
        spacing = 1
        xoffset = 0
        if type(s) is str:
            lines = s.split("\n")
            for line in lines:
                yoffset = (1+self.line_number) * self.font.height + spacing
                graphics.DrawText(self.offscreen_canvas, self.font, xoffset, yoffset, self.textColor, line)
                self.line_number += 1
        elif type(s) is list:
            for line in s:
                yoffset = (1+self.line_number) * self.font.height + spacing
                graphics.DrawText(self.offscreen_canvas, self.font, xoffset, yoffset, self.textColor, line)
                self.line_number += 1
        else:
            return
                
        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)

    def clear_screen(self):
        self.line_number = 0
        self.offscreen_canvas.Clear()
        self.matrix.SwapOnVSync(self.offscreen_canvas)

    def run(self):
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()
        self.font = graphics.Font()
        self.font.LoadFont("../../../fonts/4x6.bdf")
        self.textColor = graphics.Color(255, 255, 0)
        
        text = "NOW 2021-07-16\n"
        text += "PARTLY CLOUDY" + "\n"
        text += "TEMP:" + str("82") + "F\n"
        text += "FEEL:" + str("59") + "F\n"
        text += "HMDTY:" + str(60) + "%\n"
        text += "WIND:" + str(10.2) + "MPH " + str("NW") + "\n"

        self.ledprintln(justify(text, 16, justify_last_line=True))
        time.sleep(5)
        self.clear_screen()

        time.sleep(2)

        self.ledprintln(textwrap.wrap("hello there friend, I'm ethan and I am your creator. soon you will tell me the weather every day.", width=16))
        time.sleep(5)
        self.clear_screen()

        self.ledprintln("haha nice")
        time.sleep(1)
        self.clear_screen()
        
# Main function
if __name__ == "__main__":
    run_text = RunText()
    run_text.process()

