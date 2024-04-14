from machine import Pin
from gpiodefs import READ_PIN
from outcome_mod import Outcome

class FakePanel():
    def __init__(self):
        self.read_pin = Pin(READ_PIN, Pin.In, Pin.PULL_DOWN)
        self.led_pin = Pin("LED", Pin.OUT)

    def read_pin_state(self):
        return Outcome(True, data=self.read_pin.value())
        
    def set_led_state(self, state):
        self.led_pin.value(state)
        return Outcome(True)

    def do_a_slow_thing(self, progress_callback=None):
        pass

    def get_display_state(self):
        pass
        # return {
        #     ""
        # }