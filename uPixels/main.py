import machine, neopixel, time, urandom

pin = machine.Pin(4, machine.Pin.OUT)
np = neopixel.NeoPixel(pin, 30)

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

def fill(ms, color):
    count = np.n
    while count > 0:
        for i in range(count):
            np[i] = color
            np.write()
            time.sleep_ms(ms)
            if i != count-1:
                np[i] = (0,0,0)
        count -= 1

def randomFill(ms):
    while True:
        random_position = random.randrange(np.n)

def setSegment(segment_of_leds, color):
    for led in segment_of_leds:
        np[led] = color
    np.write()

# def rainbow(ms):
#     for r in range(256):
#         for g in range(256):
#             for b in range(256):
#                 np[0] = (r,g,b)
#                 np.write()
#                 time.sleep_ms(ms)

def bounce(ms,color,segment_length=1):
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

def randomFill:
    pass
    # len(bin(np.n)[2:])
    # random.getrandbits(len(bin(np.n)[2:]))
    #if less than np.n
