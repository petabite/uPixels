# μPixels (microPixels)

![logo](https://raw.githubusercontent.com/petabite/uPixels/master/images/apple-icon-114x114px.png)

### Addressable RGB LED Strip controller for MicroPython enabled micro-controllers

## Contents
- [Features](#features)
- [Changelog](#changelog)
- [Screenshot](#screenshot)
- [Requirements](#requirements)
- [Dependencies](#dependencies)
- [Schematic](#schematic)
- [Setup](#setup)
- [Quick Start](#quick-start)
- [REST API Reference](#rest-api-reference)
- [Documentation](#documentation)
- [Additional Resources](#additional-resources)
- [Tested On](#tested-on)
- [Special Thanks](#special-thanks)


## Features

- Up and running in just three lines of code!
- User-friendly interface hosted from the micro-controller itself!
- Complete control over animations from delay time, color, brightness
- Completely customizable animations and user interface which is written with just Python/HTML/CSS/JS!
- Use with the user interface or programmatically using the Animations API
- Call animations from the network!
- Support for optional separate status indicator LED

    ### Out of the Box Animations:

    - Rainbow
    - Rainbow Chase
    - Bounce
    - Sparkle
    - Wipe
    - Chase
    - RGB Fade
    - Alternating Colors
    - Random Fill
    - Fill from Middle
    - Fill from Sides
    - Fill Strip
    - Christmas

## Changelog
| Release | Changes                                                                     |   Date    |
| :-----: | :-------------------------------------------------------------------------- | :-------: |
|  v2.0   | <ul><li>Offical release of /execute API</li><li>add setStrip method</li><li>New rainbow chase + wipe + sparkle animations</li><li>Segment length on chase animation</li></ul> | 12/31/2020 |
|  v1.2   | <ul><li>New colors section</li><li>New Christmas lights animation</li></ul> | 3/22/2020 |
|  v1.1   | <ul><li>New status LED indicator</li><li>New startup animation</li></ul>    | 9/2/2019  |
|  v1.0   | <ul><li>FIRST RELEASE!!</li></ul>                                           | 8/12/2019 |

## Screenshots

<img src="https://raw.githubusercontent.com/petabite/uPixels/master/images/screenshot.png" width="400">

**Animations screen**

<img src="https://raw.githubusercontent.com/petabite/uPixels/master/images/colors-screen.png" width="400">

**Colors screen**

## Requirements

- Micro-controller that supports MicroPython(like the NodeMCU ESP8266)
- WS2812 Individually Addressable RGB LEDs
- 3V3 to 5V Logic Level Shifter
- A regular LED(optional)
- 270 ohm resistor
- 1000 μF capacitor
- 5V Power Supply(The amperage depends on your project. Each LED draws about 60mA @ full brightness/completely white)
- Wi-Fi network for your micro-controller to connect to(if you want to use the controller interface)
- USB cable to transfer files to your micro-controller(depending on your situation)
- More info on materials: [Adafruit](https://learn.adafruit.com/adafruit-neopixel-uberguide), [Sparkfun](https://learn.sparkfun.com/tutorials/ws2812-breakout-hookup-guide/all)

## Dependencies
- MicroPython v1.24 or later (may work on earlier versions but not tested)
- uWeb (get it from my repo [here](https://github.com/petabite/uWeb))
- MicroCRON (get it from fizista's repo [here](https://github.com/fizista/micropython-mcron))

## Schematic

#### The circuit diagram below is one possible configuration for μPixels.

![schematic](https://raw.githubusercontent.com/petabite/uPixels/master/images/uPixels.png)

##### Some Notes:

- Depending on your board, you may not need the Logic Level Shifter. The NodeMCU ESP8266(which I used for testing) is a 3V3 board while the LED Strip is a 5V device so it is important that the 3V3 signal is converted to 5V so that everything works properly.
- The power supply that you will need for your project will vary depending on the number of LEDS you want to drive(Rule of thumb: Each individual LED draws about 60mA @ full brightness/completely white). Refer to these resources to decide: [Adafruit](https://learn.adafruit.com/adafruit-neopixel-uberguide), [Sparkfun](https://learn.sparkfun.com/tutorials/ws2812-breakout-hookup-guide/all)
- The capacitor between the terminals of the power supply helps to smooth the supply of power as power draw can change drastically.
- It is important that all the grounds are connected together.
- It is recommended to power the LED strip directly from the power source. Don't power the strip from the board. Your board might not be able to supply the necessary current and it will blow up 💥.
- You may power the LEDs directly from the board if you only want to drive a few LEDs.


## Setup
1. Install MicroPython v1.24 or later on your board if you have not already ([ESP8266 installation](http://docs.micropython.org/en/latest/esp8266/tutorial/intro.html#intro))
1. Install μWeb by following the INSTALLATION instructions on my [repo](https://github.com/petabite/uWeb#installation).
2. Install MicroCRON. In a REPL session, run the following:
    ```python
    import mip
    mip.install('github:fizista/micropython-mcron/mcron/__init__.py', target='mcron')
    ```
3. Head over to the releases tab on this repo. Download the source code for the latest version. Copy the μPixels project files to your board using the same method you used to copy the μWeb files. Make sure that you have transferred:
    - uPixels.css
    - uPixels.html
    - uPixels.js
    - uPixels.mpy

    *NOTE:* If you are running a different version of MicroPython, you may need to compile a version of uPixels.mpy that works with your version of MicroPython using [`mpy-cross`](https://github.com/micropython/micropython/tree/master/mpy-cross). See [MicroPython .mpy files docs](https://docs.micropython.org/en/latest/reference/mpyfiles.html).

4. Construct the circuit [above](#schematic) (or a variation of it, depending on your board). You may also follow these hookup guides: [Adafruit](https://learn.adafruit.com/adafruit-neopixel-uberguide), [Sparkfun](https://learn.sparkfun.com/tutorials/ws2812-breakout-hookup-guide/all)
5. Check out the [Quick Start](#quick-start) section for examples.
6. Make sure you also have a boot.py for the initial setup of your board(ie: connecting to wifi) and main.py for the μPixels code.
7. Power up your board.
8. Navigate to your board's IP address on port 8000 using a web browser to access the UI(Ex: 192.168.100.48:8000)
9. Enjoy the light show!

## Quick Start

#### Example application using the μPixels user interface:

``` python
from uPixels import uPixels

pixels = uPixels(4, 30) # init a μPixels object using Pin 4 and controlling a LED strip with 30 LEDS
pixels.start_server() # start the server that hosts the UI on port 8000
```

#### Example application using Animations API:

``` python
from uPixels import uPixels

pixels = uPixels(4, 30) # init a μPixels object on Pin 4 that is controlling a LED strip with 30 LEDS

for i in range(3):
    pixels.chase(ms=40, color=(100, 0, 0), direction='right') # do a chase animation three times with delay of 40ms, red color, going right.

pixels.random_fill(ms=150, color=None) # random fill animation with 150ms delay and random colors
```

#### See the docs below for usage of all the μPixels animations!

-----

## REST API Reference

After running `uPixels.start_server()`, the following routes will be available at the address and port set when uPixels was initialized(Default: 0.0.0.0:8000).

### `GET /`

#### *Response*

- Returns uPixels user interface(works best on a mobile browser)
- Add this page to your phone's homescreen using Chrome(Android) or Safari(iOS) for an app-like experience([tutorial](https://www.howtogeek.com/196087/how-to-add-websites-to-the-home-screen-on-any-smartphone-or-tablet/))!
### `POST /execute`

- Run animations from the Animations API and other methods via a POST request to this route from any device connected on the same network as your microcontroller.
- All animations from the Animations API can be called from here as well as the `set_strip`, `set_segment`, and `clear` methods.
- BEWARE of infinite loop animations. Once you start them, they can't be stopped unless you do a hard reset!
  
#### *Parameters*
- This route takes a JSON body with an `action` and `params` to be passed to the `action`
- *Required:*
  - `action` - (string) name of function/animation to be run (name must be camel-case version of the method name in documentation)
  - `params` - (object) named params to be passed to the function(if no params, pass an empty object)
    - When color is needed, pass a `color` object with `r`, `g`, `b` values, such as
      ```JSON
      {
        ...
        "color" : {
          "r": 100,
          "g": 100,
          "b": 100,
        }
      }
    - NOTE: For the `altColors` animation, pass a `first_color` and `second_color` object

*Ex: To run the `rainbow` animation(w/ params), send a JSON body like this:* 
```JSON
{
	"action": "rainbow",
	"params": {
		"ms": 10,
		"iterations": 1
	}
}
```

*Ex: To run `setStrip`, which takes a color, send a JSON body like this:* 
```JSON
{
	"action": "setStrip",
	"params": {
		"color": {
			"r": 255,
			"g": 50,
			"b": 50
		}
	}
}
```

*Ex: To run `clear`, which takes no params, send a JSON body like this:* 
```JSON
{
	"action": "clear",
	"params": {}
}
```

#### *Response*
- On success, the response will have a `200` status with no body.
- On error, the response will have a `400` status and will return an error message. Check the MicroPython WebREPL for a more detailed error message!

### `POST /schedules`
- Schedule animations to run at a specific time of day
  
#### *Parameters*
- This route takes a JSON body with an array of objects containing `time`, `action`, and `params` representing the time of day to run the animation (in seconds from midnight UTC), the animation to run, and the parameters to pass to the animation.

*Ex: To run `setStrip` at 1:30 AM UTC and `clear` at 7:00 AM UTC, send a JSON body like this:* 

```JSON
[
  {
    "time": 5400,
    "action": "setStrip",
    "params": {
      "color": {
        "r": 255,
        "g": 108,
        "b": 8
      }
    }
  },
  {
    "time": 25200,
    "action": "clear",
    "params": {}
  }
]
```

**NOTE:** 1:30 AM = $` 1 \times (60 \times 60) + 30 \times 60 = 5400 `$ and 7:00 AM = $` 7 \times (60 \times 60) = 25200 `$

#### *Response*
- On success, the response will have a `200` status with no body.

## Documentation

### Objects

### `uPixels.uPixels(pin, num_leds, address="0.0.0.0", port=8000)`

 ###### Description
Initialize a uPixels object to control a LED strip with `num_leds` on `pin`. `Address` and `port` specifies where to host the UI.

  ###### Parameters
  - pin - (int) pin where the LED strip data line is connected
  - num_leds - (int) number of LEDS on strip
  - address - (str) address to listen on. Default: "0.0.0.0"
  - port - (int) port to listen on. Default: 8000

## Attributes

- `uPixels.device_name` - (str) name of device
- `uPixels.pin` - (machine.Pin) pin object of board that LED is connected to
- `uPixels.np` - (neopixel.NeoPixel) Neopixel object
- `uPixels.address` - (str) address UI is hosted on
- `uPixels.port` - (int) port UI is hosted on
- `uPixels.animation_map` - (dict) mapping of animation names to their corresponding functions. Used when calling the animations from the UI.
- `uPixels.status_led_pin` - (int) pin number of status LED indicator. Default: 5

----

## Server Methods


## `uPixels.set_device_name(name)`

  ###### Description
  Sets name of device
  ###### Parameters
  - name - (str) device name

-----

## `uPixels.start_server()`

###### Description
Serves the UI using the uWeb server on specified address and port

-----


## `uPixels.app()`

  ###### Description
  Renders the UI template to client

-----

## `uPixels.execute()`

  ###### Description
  Runs when uPixels receives a POST request from the client and executes the animation from uPixels.animation_map

-----

## `uPixels.set_status_led(pin)`

  ###### Description
  Set the pin number for the optional status LED indicator
  ###### Parameters
  - pin - (int) pin number where your LED is connected. NOTE: set this to False to disable the status LED indicator

-----

## `uPixels.toggle_server_status_led(status=1)`

  ###### Description
  Toggle the status LED indicator
  ###### Parameters
  - status - (int) state of the LED to set; 0 = off, 1 = on. Default: 1.

-----

## Animations API

-----

## `uPixels.startup_animation()`

  ###### Description
  Default startup animation played when uPixels is first initialized. Override this method to set a custom animation.

-----

## `uPixels.chase(ms=20, color=None, segment_length=5, direction='right')`

  ###### Description
  Chase animation going left or right
  ###### Parameters
  - ms - (int) delay time in milliseconds. Default: 20
  - color - (tuple) RGB color for animation in the format (r, g, b). Default: None (random color)
  - segment_length - (int) number of LEDs to be used. Default: 5
  - direction - (str) direction of animation; 'left' or 'right'. Default: 'right'

-----

## `uPixels.fill_strip(ms=25, color=None)`

  ###### Description
  Fill strip animation starting from the first LED
  ###### Parameters
  - ms - (int) delay time in milliseconds. Default: 25
  - color - (tuple) RGB color for animation in the format (r, g, b). Default: None (random color)

-----

## `uPixels.fill_from_middle(ms=40, color=None)`

  ###### Description
  Fill strip animation starting from the middle of the strip
  ###### Parameters
  - ms - (int) delay time in milliseconds. Default: 40
  - color - (tuple) RGB color for animation in the format (r, g, b). Default: None (random color)

-----

## `uPixels.fill_from_sides(ms=40, color=None)`

  ###### Description
  Fill strip animation starting from both ends
  ###### Parameters
  - ms - (int) delay time in milliseconds. Default: 40
  - color - (tuple) RGB color for animation in the format (r, g, b). Default: None (random color)

-----

## `uPixels.random_fill(ms=150, color=None)`

  ###### Description
  Random filling of strip one LED at a time
  ###### Parameters
  - ms - (int) delay time in milliseconds. Default: 150
  - color - (tuple) RGB color for animation in the format (r, g, b). Default: None (random color)

-----

## `uPixels.alternating_colors(ms=125, first_color=None, second_color=None)`

  ###### Description
  Alternating colors every other LED on strip
  ###### Parameters
  - ms - (int) delay time in milliseconds. Default: 125
  - first_color - (tuple) RGB color for first color in the format (r, g, b). Default: None (random color)
  - second_color - (tuple) RGB color for second color in the format (r, g, b). Default: None (random color)

-----

## `uPixels.bounce(ms=20, color=None)`

  ###### Description
  Bouncing animation of one LED from left to right and back
  ###### Parameters
  - ms - (int) delay time in milliseconds. Default: 20
  - color - (tuple) RGB color for animation in the format (r, g, b). Default: None (random color)

-----

## `uPixels.rgb_fade(ms=20)`

  ###### Description
  Fade of RGB values on whole strip
  ###### Parameters
  - ms - (int) delay time in milliseconds. Default: 20

-----

## `uPixels.rainbow(ms=20, iterations=2)`

  ###### Description
  Cycle of colors in rainbow over entire strip
  ###### Parameters
  - ms - (int) delay time in milliseconds. Default: 20
  - iterations - (int) repetitions of animation

-----

## `uPixels.rainbow_chase(ms=50)`

  ###### Description
  Rainbow chase animation
  ###### Parameters
  - ms - (int) delay time in milliseconds. Default: 50

-----

## `uPixels.wipe(ms=20, color=None)`

  ###### Description
  Wipe animation
  ###### Parameters
  - ms - (int) delay time in milliseconds. Default: 20
  - color - (tuple) RGB color for animation in the format (r, g, b). Default: None (random color)

-----

## `uPixels.sparkle(ms=10, color=None)`

  ###### Description
  Sparkle animation
  ###### Parameters
  - ms - (int) delay time in milliseconds. Default: 10
  - color - (tuple) RGB color for animation in the format (r, g, b). Default: None (random color)

-----

## `uPixels.clear()`

  ###### Description
  Clears entire strip

-----

## Helper Methods

## `uPixels.set_strip(color=None)`

  ###### Description
  Set entire strip to a color
  ###### Parameters
  - color - (tuple) RGB color in the format (r, g, b). Default: None (random color)

-----

## `uPixels.set_segment(segment_of_leds, color)`

  ###### Description
  Set specified segments of LEDS to a color
  ###### Parameters
  - segment_of_leds - (list) positions of each individual LED to be set(Ex: `[1, 4, 10]` will set LEDS @ index 1, 4, and 10 to the color).
  - color - (tuple) RGB color in the format (r, g, b).

-----

## `uPixels.rand_int(lower, upper)`

  ###### Description
  Returns a random number between lower and upper(not including upper)
  ###### Parameters
  - lower - (int) lower bound
  - upper - (int) upper bound(this value is not included in the function)
  ###### Returns
  - (int) integer between `lower` and `upper` not including `upper`

-----

## `uPixels.rand_color()`

  ###### Description
  Return a random RGB tuple
  ###### Returns
  - (tuple) RGB tuple in form (r, g, b). Min: 0, Max: 255

-----

## `uPixels.wheel(pos)`

  ###### Description
  Rainbow wheel function used in the rainbow animations
  ###### Parameters
  - pos - (int) position in wheel
  ###### Returns
  - (tuple) RGB tuple representing the position of the wheel

-----

## Additional Resources
- [Adafruit](https://learn.adafruit.com/adafruit-neopixel-uberguide)
- [Sparkfun](https://learn.sparkfun.com/tutorials/ws2812-breakout-hookup-guide/all)
- [NodeMCU v3 Pinout](https://www.theengineeringprojects.com/wp-content/uploads/2018/10/Introduction-to-NodeMCU-V3.png)
- [WS2812B LED Strip Datasheet](https://www.kitronik.co.uk/pdf/WS2812B-LED-datasheet.pdf)

## Tested on
- NodeMCU v3 (ESP8266)
- WS2812b Individually Addressable RGB LEDs

## Special Thanks
- MaterializeCSS
- Google Material Design Icons
- Spectrum.js
- noUiSlider.js
- MicroPython
- jQuery
- jgarff - [rpi_ws281x](https://github.com/jgarff/rpi_ws281x)
- fizista - [MicroCRON](https://github.com/fizista/micropython-mcron)
