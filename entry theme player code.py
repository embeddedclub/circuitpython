#############################################
#Author : Ashok R (www.ashokr.com)
#Company : Embedded Club (www.embedded.club)
#File : code.py - Entry Theme Player
#############################################
import board
import time
import digitalio
import audiobusio
import audiomp3
import neopixel
import random

from rainbowio import colorwheel

bgm_file_name = [
    "jack_sparrow_bgm_22hz.mp3",
    "kgf_bgm_22hz.mp3",
    "money_heist_bgm_22hz.mp3",
    "dum_dee_dum_bgm_22hz.mp3",
    "gangster_bgm_22hz.mp3",
    "lucky_luke_bgm_22hz.mp3",
    "the_departed_bgm_22hz.mp3",
]

audio = audiobusio.I2SOut(board.GP0, board.GP1, board.GP2)
audio_is_playing = 0
tone_volume = 0.1  # Increase this to increase the volume of the tone.
frequency = 440  # Set this to the Hz of the tone you want to generate.
length = 8000 // frequency

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

neopix_size = 16
neopix = neopixel.NeoPixel(board.GP4, neopix_size, pixel_order=neopixel.RGBW)
neopix.brightness = 0.2
sense = digitalio.DigitalInOut(board.GP3)
sense.switch_to_input(pull=digitalio.Pull.UP)

# Function that will block the thread with a while loop
# which will simply display a message every second

def rainbow_move(time_ms):
    for i in range(neopix_size):
        pixel_index = random.randint(0, 15) * 256 // neopix_size
        # random.randint(200, 256) // neopix_size
        neopix[i] = colorwheel((pixel_index) & 255)
        neopix.show()
    time.sleep(time_ms)


def rainbow(speed):
    for j in range(1):
        for i in range(neopix_size):
            pixel_index = (i * 256 // neopix_size) + j
            neopix[i] = colorwheel((pixel_index) & 255)
        neopix.show()


while True:
    if sense.value == 1 and audio.playing == 0:
        ri = random.randint(0, 6)
        mp3 = audiomp3.MP3Decoder(open(bgm_file_name[ri], "rb"))
        led.value = True
        audio.play(mp3)
        while audio.playing:
            if mp3.rms_level > 180:
                rainbow_move(mp3.rms_level / 1500)
            else:
                neopix.fill((0, 0, 0))
            pass
    if audio.playing == 0:
        led.value = False
        neopix.fill((0, 0, 0))
    time.sleep(0.6)
