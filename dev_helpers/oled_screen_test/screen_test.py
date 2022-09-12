# https://docs.micropython.org/en/latest/esp8266/tutorial/ssd1306.html

from machine import Pin, I2C
import ssd1306


# using default address 0x3C
i2c = I2C(sda=Pin(4), scl=Pin(5))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

# Print Hello World on the first line:
display.text('Hello, World!', 0, 0, 1)
display.show()

# def display_test():
#     i2c = SoftI2C(scl=Pin(17), sda=Pin(16))

#     print(i2c.scan())

#     display_width = 128
#     display_height = 32
#     display = ssd1306.SSD1306_I2C(display_width, display_height, i2c)

#     display.text('0000111100001111', 0, 0, 1)
#     display.text('Hello World', 0, 8, 1)
#     display.text('Hello World', 0, 16, 1)
#     display.text('Hello World', 0, 24, 1)
#     display.line(0,7,128,7,1)
#     display.show()