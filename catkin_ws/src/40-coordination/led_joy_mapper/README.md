# Package `led_joy_mapper` {#led_joy_mapper}

<move-here src='#led_joy_mapper-autogenerated'/>

## In depth

To test the LED emitter with your joystick, run the following command:

    $ roslaunch led_joy_mapper led_joy_with_led_emitter_test.launch veh:=![robot name]

This launches the joy controller, the mapper controller, and the led emitter nodes. You should not need to run anything external for this to work. Use the joystick buttons X and Y to turn on and off the LEDs.

Note that the function allows different blinking frequencies. This can be directly changed in the initialization of the class defined in led_emitter_node.py.
