import time
import random
import sys
import json
import os

import machine
import network
import neopixel
import ntptime
import mcron
from uWeb import uWeb, loadJSON

class uPixels:
    VERSION = "3.0"
    CONFIG_FILE_PATH = "uPixels.config"
    INITIAL_CONFIG = {"device_name": os.uname()[0], "schedules": []}

    def __init__(self, pin, num_leds, address="0.0.0.0", port=8000):
        self.config = {}
        self.pin = machine.Pin(pin, machine.Pin.OUT)  # configure pin for leds
        self.np = neopixel.NeoPixel(self.pin, num_leds)  # configure neopixel library
        self.address = address
        self.port = port
        self.server = uWeb(address, port)
        self.server.routes(
            {
                (uWeb.GET, "/"): self.app,
                (uWeb.POST, "/execute"): self.execute,
                (uWeb.POST, "/schedules"): self.update_schedules,
            }
        )
        self.animation_map = {
            "rainbow": self.rainbow,
            "rainbowChase": self.rainbow_chase,
            "bounce": self.bounce,
            "chase": self.chase,
            "rgbFade": self.rgb_fade,
            "altColors": self.alternating_colors,
            "randomFill": self.random_fill,
            "fillFromMiddle": self.fill_from_middle,
            "fillFromSides": self.fill_from_sides,
            "fillStrip": self.fill_strip,
            "wipe": self.wipe,
            "sparkle": self.sparkle,
            "setStrip": self.set_strip,
            "setSegment": self.set_segment,
            "clear": self.clear,
        }
        self.status_led_pin = 5
        self.load_config()
        self.init_schedule()
        self.startup_animation()

    # config methods

    def set_device_name(self, name):
        self.config["device_name"] = name
        self.save_config()

    def set_schedules(self, schedules):
        self.config["schedules"] = schedules
        self.save_config()
        self.init_schedule()

    def save_config(self):
        with open(self.CONFIG_FILE_PATH, "w", encoding="utf-8") as f:
            config_string = json.dumps(self.config)
            f.write(config_string)

    def load_config(self):
        try:
            with open(self.CONFIG_FILE_PATH, "r", encoding="utf-8") as f:
                self.config = json.loads(f.read())
        except OSError:
            self.config = self.INITIAL_CONFIG
            self.save_config()

    # schedule methods
    def init_schedule(self):
        mcron.init_timer()
        mcron.remove_all()

        # sync time 4x a day
        mcron.insert(
            mcron.PERIOD_DAY,
            range(0, mcron.PERIOD_DAY, mcron.PERIOD_DAY // 4),
            "sync_time",
            self.sync_time,
        )

        for index, schedule in enumerate(self.config["schedules"]):
            mcron.insert(
                mcron.PERIOD_DAY,
                {schedule["time"]},
                "schedule_" + str(index),
                self.scheduled_action_handler(schedule),
            )

    def scheduled_action_handler(self, schedule):
        return lambda _callback_id, _current_time, _callback_memory: self.do_action(
            schedule["action"], schedule["params"]
        )

    def sync_time(self, _callback_id, _current_time, _callback_memory):
        ntptime.settime()

    # web server methods
    def start_server(self):
        self.toggle_server_status_led()
        self.server.start()

    def app(self):
        variables = {
            "name": self.config["device_name"],
            "schedules": json.dumps(self.config["schedules"]),
            "upixels_ver": self.VERSION,
            "mp_ver": os.uname()[3],
            "ip": network.WLAN(network.STA_IF).ifconfig()[0],
            "host": network.WLAN(network.STA_IF).ifconfig()[0]
            + ":"
            + str(self.server.port),
            "num": self.np.n,
        }
        self.server.render("uPixels.html", layout=False, variables=variables)

    def execute(self):
        try:
            query = loadJSON(self.server.request_body)
            action = query["action"]
            params = query["params"]
            if action not in self.animation_map.keys():
                self.server.sendStatus(self.server.BAD_REQUEST)
                self.server.sendBody(b"%s is not a valid action!" % (action))
                return
            self.server.sendStatus(self.server.OK)
            self.do_action(action, params)
        except Exception as e:
            self.server.sendStatus(self.server.BAD_REQUEST)
            self.server.sendBody(b"An error occurred: %s!" % (str(e)))
            sys.print_exception(e)

    def update_schedules(self):
        schedules = loadJSON(self.server.request_body)
        self.set_schedules(schedules)

    def do_action(self, action, params={}):
        if "color" in params.keys():
            if params["color"] is not None:
                params["color"] = (
                    params["color"]["r"],
                    params["color"]["g"],
                    params["color"]["b"],
                )
        if "firstColor" in params.keys():
            if params["firstColor"] is not None:
                params["firstColor"] = (
                    params["firstColor"]["r"],
                    params["firstColor"]["g"],
                    params["firstColor"]["b"],
                )
        if "secondColor" in params.keys():
            if params["secondColor"] is not None:
                params["secondColor"] = (
                    params["secondColor"]["r"],
                    params["secondColor"]["g"],
                    params["secondColor"]["b"],
                )
        self.animation_map[action](**params)  # call the animation method

    def set_status_led(self, pin):
        self.status_led_pin = pin

    def toggle_server_status_led(self, status=1):
        if self.status_led_pin:
            status_led = machine.Pin(self.status_led_pin, machine.Pin.OUT)
            status_led.value(status)

    # animation methods
    def startup_animation(self):
        self.chase(ms=5, color=(0, 255, 155), direction="right")
        self.chase(ms=5, color=(0, 255, 155), direction="left")
        self.clear()

    def chase(self, ms=20, color=None, segment_length=5, direction="right"):
        if color is None:
            color = self.rand_color()
        if direction == "right":
            led_iter = range(self.np.n - segment_length - 2)
        else:
            led_iter = range(self.np.n - segment_length - 2, -1, -1)
        for i in led_iter:
            for j in range(segment_length):
                self.np[i + j] = color
            self.np.write()
            time.sleep_ms(ms)
            if direction == "right":
                clear_iter = range(i, i + segment_length + 1)
            else:
                clear_iter = range(i + segment_length + 1, i, -1)
            for i in clear_iter:
                self.np[i] = (0, 0, 0)

    def fill_strip(self, ms=25, color=None):
        if color is None:
            color = self.rand_color()
        count = self.np.n
        while count > 0:
            for i in range(count):
                self.np[i] = color
                self.np.write()
                time.sleep_ms(ms)
                if i != count - 1:
                    self.np[i] = (0, 0, 0)
            count -= 1

    def fill_from_middle(self, ms=40, color=None):
        if color is None:
            color = self.rand_color()
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

    def fill_from_sides(self, ms=40, color=None):
        if color is None:
            color = self.rand_color()
        midpoint = int(self.np.n / 2)
        counter = 0
        while counter != midpoint:
            self.np[0 + counter] = color
            self.np[self.np.n - 1 - counter] = color
            self.np.write()
            time.sleep_ms(ms)
            counter += 1

    def random_fill(self, ms=150, color=None):
        random_positions = list(range(self.np.n))
        for position in random_positions:
            rand_i = self.rand_int(0, self.np.n)
            temp = position
            position = random_positions[rand_i]
            random_positions[rand_i] = temp
        for position in random_positions:
            if color is None:
                self.np[position] = self.rand_color()
            else:
                self.np[position] = color
            self.np.write()
            time.sleep_ms(ms)

    def alternating_colors(self, ms=125, first_color=None, second_color=None):
        if first_color is None:
            first_color = self.rand_color()
        if second_color is None:
            second_color = self.rand_color()
        while True:
            if time.localtime()[3] == 6:
                self.clear()
                break
            for i in range(self.np.n):
                if i % 2 == 0:
                    self.np[i] = first_color
                else:
                    self.np[i] = second_color
            self.np.write()
            time.sleep_ms(ms)
            for i in range(self.np.n):
                if i % 2 == 0:
                    self.np[i] = second_color
                else:
                    self.np[i] = first_color
            self.np.write()
            time.sleep_ms(ms)

    def bounce(self, ms=20, color=None):
        while True:
            if color is None:
                self.chase(ms=ms, color=self.rand_color(), direction="right")
                self.chase(ms=ms, color=self.rand_color(), direction="left")
            else:
                self.chase(ms=ms, color=color, direction="right")
                self.chase(ms=ms, color=color, direction="left")

    def rgb_fade(self, ms=20):
        for channel in range(3):
            for v in range(256):
                if channel == 0:
                    self.set_strip((v, 0, 0))
                if channel == 1:
                    self.set_strip((0, v, 0))
                if channel == 2:
                    self.set_strip((0, 0, v))
                time.sleep_ms(ms)
            for v in range(255, -1, -1):
                if channel == 0:
                    self.set_strip((v, 0, 0))
                if channel == 1:
                    self.set_strip((0, v, 0))
                if channel == 2:
                    self.set_strip((0, 0, v))
                time.sleep_ms(ms)

    def rainbow(self, ms=20, iterations=2):
        for j in range(256 * iterations):
            for i in range(self.np.n):
                self.np[i] = self.wheel(((i * 256 // self.np.n) + j) & 255)
            self.np.write()
            time.sleep_ms(ms)

    def rainbow_chase(self, ms=50):
        for i in range(5):
            for j in range(256):
                for q in range(3):
                    for i in range(0, self.np.n, 3):
                        self.np[i + q] = self.wheel((i + j) % 255)
                    self.np.write()
                    time.sleep_ms(ms)
                    for i in range(0, self.np.n, 3):
                        self.np[i + q] = (0, 0, 0)

    def wipe(self, ms=20, color=None):
        if color is None:
            color = self.rand_color()
        while True:
            for i in range(self.np.n):
                self.np[i] = color
                self.np.write()
                time.sleep_ms(ms)
            for i in range(self.np.n):
                self.np[i] = (0, 0, 0)
                self.np.write()
                time.sleep_ms(ms)

    def sparkle(self, ms=10, color=None):
        if color is None:
            color = self.rand_color()
        while True:
            i = self.rand_int(0, self.np.n)
            self.np[i] = color
            self.np.write()
            time.sleep_ms(ms)
            self.np[i] = (0, 0, 0)

    def clear(self):
        self.set_strip((0, 0, 0))

    # helper methods
    def set_strip(self, color):
        self.set_segment(list(range(self.np.n)), color)

    def set_segment(self, segment_of_leds, color):
        for led in segment_of_leds:
            self.np[led] = color
        self.np.write()

    def rand_int(self, lower, upper):
        random_num = random.getrandbits(len(bin(upper)[2:])) + lower
        if random_num < upper:
            return random_num
        else:
            return upper - 1

    def rand_color(self):
        return (self.rand_int(0, 256), self.rand_int(0, 256), self.rand_int(0, 256))

    def wheel(self, pos):
        if pos < 85:
            return (pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return (255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return (0, pos * 3, 255 - pos * 3)
