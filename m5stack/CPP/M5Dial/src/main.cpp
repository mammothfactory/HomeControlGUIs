/*
__authors__    = ["Blaze Sanders"]
__contact__    = "blazes@mfc.us"
__copyright__  = "Copyright 2023"
__license__    = "TBD"
__status__     = "Development
__deprecated__ = False
__version__    = "0.1.0"
__doc__        = "Code entry point for M5 Stack Dial"
*/

#include <iostream>
#include "/Users/venus/GitRepos/HomeControlGUIs/m5stack/CPP/M5Dial/src/M5Dial.h"
// Update includePath following https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwiXwPqMlNuDAxV-lGoFHYtICGkQFnoECBMQAw&url=https%3A%2F%2Flabs.dese.iisc.ac.in%2Fembeddedlab%2Fvscode-include-paths%2F%23%3A~%3Atext%3DIf%2520the%2520cursor%2520is%2520on%2Copen%2520a%2520file%2520called%2520%25E2%2580%259Cc_cpp_properties.&usg=AOvVaw231xslPsZTSDkx-RQilbB3&opi=89978449
// Mising path to "M5Unified.h"

using namespace m5;
using namespace std;


// Include this to enable the M5 global instance.
#include <M5Unified.h>

#include "iot_knob.h"
#include "iot_button.h"

#include "esp_lvgl_port.h"
#include "lvgl.h"
#include "lv_example_pub.h"

static const char *TAG = "main";

static const uint16_t screenWidth  = 240;
static const uint16_t screenHeight = 240;


int main() {
  cout << "Booting Moe Build LLC M5 Stack Dial software.";
  
  M5_DIAL M5Dial;
  m5::M5Unified::config_t cfg

  M5Dial.begin(cfg, True, False)
  M5Dial.update()

  M5DIAL_ENCODER_H M5DialEncoder
  M5DialEncoder.resolution()
  M5DialEncoder.active_level()
  M5DialEncoder.begin()

  
  return 0;
}