# Include the ESP8266 port's default manifest.
include("$(PORT_DIR)/boards/manifest.py")
module("uWeb.py", base_path="/Users/pz/code/uWeb/uWeb")
require("neopixel")
require("ntptime")
package("mcron", base_path="/Users/pz/code/micropython-mcron")
