lickport_array_interface_python
===============================

This Python package creates a class named LickportArrayInterface.

Authors::

    Peter Polidoro <peter@polidoro.io>

License::

    BSD

Example Usage::

    from lickport_array_interface import LickportArrayInterface
    dev = LickportArrayInterface() # Try to automatically detect port
    dev = LickportArrayInterface(port='/dev/ttyACM0') # Linux specific port
    dev = LickportArrayInterface(port='/dev/tty.usbmodem262471') # Mac OS X specific port
    dev = LickportArrayInterface(port='COM3') # Windows specific port
    dev.start_acquiring_data()
    dev.start_saving_data()
    dev.stop_saving_data()
    dev.stop_acquiring_data()

    dev.controller.dispense_lickport_for_duration(0,200)
    dev.controller.dispense_lickports_for_duration([0,1],200)
    dev.controller.dispense_all_lickports_for_duration(200)
    dev.controller.get_activated_lickports()
    dev.controller.activate_only_lickport(0)
    dev.controller.activate_only_lickports([0,1])
    dev.controller.activate_lickport(0)
    dev.controller.activate_lickports([0,1])
    dev.controller.deactivate_lickport(0)
    dev.controller.deactivate_lickports([0,1])
    dev.controller.activate_all_lickports()
    dev.controller.deactivate_all_lickports()

