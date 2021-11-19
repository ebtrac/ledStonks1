//Ethan Tracy, 2021-07-11 Sunday 1:40PM
// mostly copied from input-example.cc
#include "led-matrix.h"
#include "graphics.h"

#include <unistd.h>
#include <math.h>
#include <stdio.h>
#include <signal.h>

using rgb_matrix::RGBMatrix;
using rgb_matrix::Canvas;

volatile bool interrupt_received = false;
static void InterruptHandler(int sigo) {
  interrupt_received = true;
}

int main (int argc, char * argv[]) {
  RGBMatrix::Options defaults; //options
  defaults.hardware_mapping = "adafruit-hat";
  defaults.rows = 32;
  defaults.cols = 64;
  defaults.chain_length = 2;
  defaults.pixel_mapper_config = "U-mapper;Rotate:270";
  defaults.limit_refresh_rate_hz = 122; //fps cap
  defaults.show_refresh_rate = true; //for debugging and tweaking

  rgb_matrix::RuntimeOptions rt_opts; //other options
  rt_opts.gpio_slowdown = 2;

  //Pass all options to the matrix object constructor
  Canvas *canvas = RGBMatrix::CreateFromOptions(defaults, rt_opts);

  if(canvas == NULL)
    return 1;

  //Set up CTRL+C exit handler
  signal(SIGTERM, InterruptHandler);
  signal(SIGINT, InterruptHandler); 
  
  fprintf(stderr, "display WxH: %dx%d\n\n", canvas->width(), canvas->height());

  while(!interrupt_received) {
    for (int y = 0; y < 64; y++) {
      for (int x = 0; x < 64; x++) {
	canvas->SetPixel(x, y, x, y, x+y);
      }
    }
  }

  //exit
  fprintf(stderr, "Exiting.\n");
  canvas->Clear();
  delete canvas;

  return 0;
}
