import machine, neopixel, time, urandom
from uWeb import uWeb, loadJSON

class uPixels:
    def __init__(self, pin, num_leds, address="0.0.0.0", port=8000):
        self.pin = pin
        self.num_leds = num_leds
        self.address = address
        self.port = port
        self.server = uWeb(address, port)
        server.routes({
            (uWeb.GET, "/"): self.app
        })

    # web server methods
    def startServer(self):
        self.server.start()

    def app(self):
        server.render('uPixels.html')

    # animation methods

    # helper methods
