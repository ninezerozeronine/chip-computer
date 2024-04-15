from machine import Pin
from gpiodefs import READ_PIN
from outcome_mod import Outcome

class FakePanel():
    def __init__(self):
        self.read_pin = Pin(READ_PIN, Pin.IN, Pin.PULL_DOWN)
        self.led_pin = Pin("LED", Pin.OUT)
        self.user_input_char = ""
        self.allowed_chars = (
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "A",
            "B",
            "C",
            "D",
            "*",
            "#",
        )

    def read_pin_state(self):
        return Outcome(True, data=self.read_pin.value())
        
    def set_led_state(self, state):
        self.led_pin.value(state)
        return Outcome(True)

    def set_user_input_char(self, char):
        if char in self.allowed_chars:
            self.user_input_char = char
            return Outcome(True)
        else:
            return Outcome("False", message=f"{char} is not a valid character")

    def do_a_slow_thing(self):
        pass

    def get_display_state(self):
        return {
            "user_input": self.user_input_char
        }