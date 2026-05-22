#!/usr/bin/env python3
"""
Sequential GPIO button discovery.

Prompts for each button in turn then waits for a press then records the GPIO.

Usage:
    sudo python btnmap.py --buttons 1 2 3
    sudo python btnmap.py --buttons 1,2,3,4
    sudo python btnmap.py --buttons 1 2 3 --all   # include I2C/SPI/UART pins

Ctrl-C to abort.

Assumes buttons wired to GND, active-low (internal pull-ups enabled).
RPi.GPIO does not work on Pi 5.
"""

import sys
import time
import argparse
import threading
import RPi.GPIO as GPIO

HEADER_GPIOS = [
    2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
    18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
]

RESERVED = {
    2: "I2C SDA", 3: "I2C SCL",
    7: "SPI CE1", 8: "SPI CE0", 9: "SPI MISO",
    10: "SPI MOSI", 11: "SPI SCLK",
    14: "UART TX", 15: "UART RX",
}

DEBOUNCE_MS = 50
SETTLE_S = 0.3   # pause between buttons so release isn't read as next press


def parse_button_list(values):
    """Accept ['1','2','3'] or ['1,2,3'] or mix."""
    raw = " ".join(values).replace(",", " ").split()
    try:
        return [int(x) for x in raw]
    except ValueError as e:
        sys.exit(f"bad --buttons arg: {e}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--buttons", nargs="+", required=True,
                    help="button labels to map, e.g. --buttons 1 2 3")
    ap.add_argument("--all", action="store_true",
                    help="include reserved bus pins (I2C/SPI/UART)")
    args = ap.parse_args()

    labels = parse_button_list(args.buttons)
    pins = [p for p in HEADER_GPIOS if args.all or p not in RESERVED]

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    watched = []
    for p in pins:
        try:
            GPIO.setup(p, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            watched.append(p)
        except (RuntimeError, ValueError):
            pass

    print(f"watching {len(watched)} GPIOs: {watched}\n")

    # Shared state: a press fills these in and sets the event.
    pressed_gpio = [None]
    event = threading.Event()
    already_mapped = set()

    def make_handler():
        def handler(channel):
            # Ignore pins already assigned to a previous button.
            if channel in already_mapped:
                return
            if pressed_gpio[0] is None:
                pressed_gpio[0] = channel
                event.set()
        return handler

    handler = make_handler()
    for p in watched:
        try:
            GPIO.add_event_detect(p, GPIO.FALLING,
                                  callback=handler,
                                  bouncetime=DEBOUNCE_MS)
        except RuntimeError:
            pass

    mapping = {}
    try:
        for label in labels:
            # Reset state for this round.
            pressed_gpio[0] = None
            event.clear()

            print(f"  press Button {label}... ", end="", flush=True)
            event.wait()
            gpio = pressed_gpio[0]
            mapping[label] = gpio
            already_mapped.add(gpio)
            print(f"GPIO {gpio}")

            time.sleep(SETTLE_S)  # let user release before next prompt
    except KeyboardInterrupt:
        print("\naborted.")
    finally:
        GPIO.cleanup()

    if mapping:
        print("\n--- mapping ---")
        for label, gpio in mapping.items():
            print(f"Button {label} -> GPIO {gpio}")

        # Python-dict form for paste-back
        print("\nPIN_MAP = {")
        for label, gpio in mapping.items():
            print(f"    {label}: {gpio},")
        print("}")


if __name__ == "__main__":
    main()
