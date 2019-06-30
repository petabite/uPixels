import machine, neopixel, time, urandom

pin = machine.Pin(4, machine.Pin.OUT)
np = neopixel.NeoPixel(pin, 30)

def randInt(lower, upper):
    randomNum = urandom.getrandbits(len(bin(upper)[2:])) + lower
    if randomNum < upper:
        return randomNum
    else:
        return upper - 1

def clear():
    for i in range(np.n):
        np[i] = (0,0,0)
    np.write()

def chase(ms, color, direction='right'):
    if direction == 'right':
        led_iter = range(np.n)
    else:
        led_iter = range(np.n-1, -1, -1)
    for i in led_iter:
        np[i] = color
        np.write()
        time.sleep_ms(ms)
        np[i] = (0,0,0)

def fillStrip(ms, color):
    count = np.n
    while count > 0:
        for i in range(count):
            np[i] = color
            np.write()
            time.sleep_ms(ms)
            if i != count-1:
                np[i] = (0,0,0)
        count -= 1

def fillFromMiddle(ms, color):
    midpoint = int(np.n / 2)
    counter = 0
    while counter != midpoint:
        np[midpoint + counter] = color
        if np.n % 2 == 0:
            np[midpoint - 1 - counter] = color
        else:
            np[midpoint - counter] = color
        np.write()
        time.sleep_ms(ms)
        counter += 1

def fillFromSides(ms, color):
    midpoint = int(np.n / 2)
    counter = 0
    while counter != midpoint:
        np[0 + counter] = color
        np[np.n - 1 - counter] = color
        np.write()
        time.sleep_ms(ms)
        counter += 1

def randomFill(ms, color=True):
    random_positions = []
    while len(random_positions) < np.n:
        random_pos = randInt(0, np.n)
        if random_pos not in random_positions:
            random_positions.append(random_pos)
    for position in random_positions:
        if color == True:
            np[position] = (randInt(0,256),randInt(0,256),randInt(0,256))
        else:
            np[position] = color
        np.write()
        time.sleep_ms(ms)

def setSegment(segment_of_leds, color):
    for led in segment_of_leds:
        np[led] = color
    np.write()

def altColors(ms, firstColor, secondColor):
    while True:
        for i in range(np.n):
            if i % 2 == 0:
                np[i] = firstColor
            else:
                np[i] = secondColor
        np.write()
        time.sleep_ms(ms)
        for i in range(np.n):
            if i % 2 == 0:
                np[i] = secondColor
            else:
                np[i] = firstColor
        np.write()
        time.sleep_ms(ms)

def bounce(ms, color):
    while True:
        chase(ms, color, 'right')
        chase(ms, color, 'left')

def rgbFade(ms):
    for channel in range(3):
        for v in range(256):
            if channel == 0:
                setSegment(list(range(10)), (v,0,0))
            if channel == 1:
                setSegment(list(range(10)), (0,v,0))
            if channel == 2:
                setSegment(list(range(10)), (0,0,v))
            time.sleep_ms(ms)
        for v in range(255,-1,-1):
            if channel == 0:
                setSegment(list(range(10)), (v,0,0))
            if channel == 1:
                setSegment(list(range(10)), (0,v,0))
            if channel == 2:
                setSegment(list(range(10)), (0,0,v))
            time.sleep_ms(ms)

def wheel(pos):
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)

def rainbow(ms=20, iterations = 2):
    for j in range(256*iterations):
        for i in range(np.n):
            np[i] = wheel(((i * 256 // np.n) + j) & 255)
        np.write()
        time.sleep_ms(ms)

def rainbowChase(ms=50):
    for j in range(256):
        for q in range(3):
            for i in range(0, np.n, 3):
                np[i+q] = wheel((i+j) % 255)
            np.write()
            time.sleep_ms(ms)
            for i in range(0, np.n, 3):
                np[i+q] = (0, 0, 0)
