import machine, uos, network, neopixel, time, urandom
from uWeb import uWeb, loadJSON

class uPixels:
    VERSION = '1.0'
    def __init__(self, pin, num_leds, address="0.0.0.0", port=8000):
        self.device_name = uos.uname()[0]
        self.pin = machine.Pin(pin, machine.Pin.OUT)  # configure pin for leds
        self.np = neopixel.NeoPixel(self.pin, num_leds)  # configure neopixel library
        self.address = address
        self.port = port
        self.animation_map = {
            'rainbow': self.rainbow,
            'bounce': self.bounce,
            'chase': self.chase,
            'rgbFade': self.rgbFade,
            'altColors': self.altColors,
            'randomFill': self.randomFill,
            'fillFromMiddle': self.fillFromMiddle,
            'fillFromSides': self.fillFromSides,
            'fillStrip': self.fillStrip,
            'setSegment': self.setSegment,
            'clear': self.clear
        }
        self.statusLED = 5
        self.startupAnimation()
        self.toggleServerStatusLED()

    def setDeviceName(self, name):
        self.device_name = name

    # web server methods
    def startServer(self):
        self.server = uWeb(self.address, self.port)
        self.server.routes({
            (uWeb.GET, "/"): self.app,
            (uWeb.POST, '/execute'): self.execute
        })
        self.server.start()

    def app(self):
        vars = {
            'name' : self.device_name,
            'upixels_ver': self.VERSION,
            'mp_ver': uos.uname()[3],
            'ip': network.WLAN(network.STA_IF).ifconfig()[0],
            'host': network.WLAN(network.STA_IF).ifconfig()[0]+":"+str(self.server.port),
            'num': self.np.n
        }
        self.server.render('uPixels.html', variables=vars)

    def execute(self):
        query = loadJSON(self.server.request_body)
        action = query["action"]
        params = query["params"]
        if 'color' in params.keys():
            if params['color'] != None:
                params['color'] = (params['color']['r'], params['color']['g'], params['color']['b'])
        if 'firstColor' in params.keys():
            if params['firstColor'] != None:
                params['firstColor'] = (params['firstColor']['r'], params['firstColor']['g'], params['firstColor']['b'])
        if 'secondColor' in params.keys():
            if params['secondColor'] != None:
                params['secondColor'] = (params['secondColor']['r'], params['secondColor']['g'], params['secondColor']['b'])
        print("passing ", params)
        self.animation_map[action](**params) # call the animcation method

    def setStatusLED(self, pin):
        self.statusLED = pin

    def toggleServerStatusLED(self, status=1):
        if self.statusLED:
            status_led = machine.Pin(self.statusLED, machine.Pin.OUT)
            status_led.value(status)

    # animation methods
    def startupAnimation(self):
        self.chase(color=(0, 255, 155), direction='right')
        self.chase(color=(0, 255, 155), direction='left')
        self.clear()

    def chase(self, ms=20, color=None, direction='right'):
        if color == None:
            color = self.randColor()
        if direction == 'right':
            led_iter = range(self.np.n)
        else:
            led_iter = range(self.np.n - 1, -1, -1)
        for i in led_iter:
            self.np[i] = color
            self.np.write()
            time.sleep_ms(ms)
            self.np[i] = (0,0,0)

    def fillStrip(self, ms=25, color=None):
        if color == None:
            color = self.randColor()
        count = self.np.n
        while count > 0:
            for i in range(count):
                self.np[i] = color
                self.np.write()
                time.sleep_ms(ms)
                if i != count-1:
                    self.np[i] = (0,0,0)
            count -= 1

    def fillFromMiddle(self, ms=40, color=None):
        if color == None:
            color = self.randColor()
        midpoint = int(self.np.n / 2)
        counter = 0
        while counter != midpoint:
            self.np[midpoint + counter] = color
            if self.np.n % 2 == 0:
                self.np[midpoint - 1 - counter] = color
            else:
                self.np[midpoint - counter] = color
            self.np.write()
            time.sleep_ms(ms)
            counter += 1

    def fillFromSides(self, ms=40, color=None):
        if color == None:
            color = self.randColor()
        midpoint = int(self.np.n / 2)
        counter = 0
        while counter != midpoint:
            self.np[0 + counter] = color
            self.np[self.np.n - 1 - counter] = color
            self.np.write()
            time.sleep_ms(ms)
            counter += 1

    def randomFill(self, ms=150, color=None):
        random_positions = []
        while len(random_positions) < self.np.n:
            random_pos = self.randInt(0, self.np.n)
            if random_pos not in random_positions:
                random_positions.append(random_pos)
        for position in random_positions:
            if color == None:
                self.np[position] = self.randColor()
            else:
                self.np[position] = color
            self.np.write()
            time.sleep_ms(ms)

    def altColors(self, ms=125, firstColor=None, secondColor=None):
        if firstColor == None:
            color = self.randColor()
        if secondColor == None:
            color = self.randColor()
        while True:
            for i in range(self.np.n):
                if i % 2 == 0:
                    self.np[i] = firstColor
                else:
                    self.np[i] = secondColor
            self.np.write()
            time.sleep_ms(ms)
            for i in range(self.np.n):
                if i % 2 == 0:
                    self.np[i] = secondColor
                else:
                    self.np[i] = firstColor
            self.np.write()
            time.sleep_ms(ms)

    def bounce(self, ms=20, color=False):
        while True:
            if color == False:
                self.chase(ms, self.randColor(), 'right')
                self.chase(ms, self.randColor(), 'left')
            else:
                self.chase(ms, color, 'right')
                self.chase(ms, color, 'left')

    def rgbFade(self, ms=20):
        for channel in range(3):
            for v in range(256):
                if channel == 0:
                    self.setSegment(list(range(self.np.n)), (v,0,0))
                if channel == 1:
                    self.setSegment(list(range(self.np.n)), (0,v,0))
                if channel == 2:
                    self.setSegment(list(range(self.np.n)), (0,0,v))
                time.sleep_ms(ms)
            for v in range(255,-1,-1):
                if channel == 0:
                    self.setSegment(list(range(self.np.n)), (v,0,0))
                if channel == 1:
                    self.setSegment(list(range(self.np.n)), (0,v,0))
                if channel == 2:
                    self.setSegment(list(range(self.np.n)), (0,0,v))
                time.sleep_ms(ms)

    def rainbow(self, ms=20, iterations = 2):
        for j in range(256*iterations):
            for i in range(self.np.n):
                self.np[i] = self.wheel(((i * 256 // self.np.n) + j) & 255)
            self.np.write()
            time.sleep_ms(ms)

    def rainbowChase(self, ms=50):
        for j in range(256):
            for q in range(3):
                for i in range(0, self.np.n, 3):
                    self.np[i+q] = self.wheel((i+j) % 255)
                self.np.write()
                time.sleep_ms(ms)
                for i in range(0, self.np.n, 3):
                    self.np[i+q] = (0, 0, 0)

    def clear(self):
        self.setSegment(list(range(self.np.n)), (0,0,0))

    # helper methods
    def setSegment(self, segment_of_leds, color):
        for led in segment_of_leds:
            self.np[led] = color
        self.np.write()

    def randInt(self, lower, upper):
        randomNum = urandom.getrandbits(len(bin(upper)[2:])) + lower
        if randomNum < upper:
            return randomNum
        else:
            return upper - 1

    def randColor(self):
        return (self.randInt(0,256),self.randInt(0,256),self.randInt(0,256))

    def wheel(self, pos):
        if pos < 85:
            return (pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return (255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return (0, pos * 3, 255 - pos * 3)
