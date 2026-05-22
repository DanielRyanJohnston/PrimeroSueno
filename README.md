# PrimeroSueno

Wearable Project for Primero Sueño opera premiered at The Met Cloisters Jan 2025
Developed by Daniel Ryan Johnston and by Kari Love as part of a Vision Into Art Fellowship

This project combines a Pico Projector with Raspberry Pi Zero W 2 and a first surface mirror

Tutorial: https://docs.google.com/document/d/1ZOuhU8HzmDZxRYDuTPh4y_7ntX1cBFEdLn2npm-S11U/edit?usp=sharing 

Utilizes: https://github.com/alubbock/rpi-vidlooper 
Raspberry Pi GPIO-controlled video looper
Copyright (c) 2019 Alex Lubbock
License MIT

Assuming POWER OFF START:

POWER ON : Push and HOLD 1..2..3..4 (on SUGAR)
BLUE LIGHT ON (SUGAR).

WAIT UNTIL startup sequence complete (green terminal prompt will appear).
LET SIT IN THIS STATE FOR 20-30s. OR PRESS ENTER A COUPLE OF TIMES.

`cd PrimeroSueno`

`ls` <- check files are there.

`./run.sh` <-- remember the period and slash! Just this and enter.

NO AUTOSTART - PRESS A BUTTON TO QUEUE START.

If Button Testing Required:

`python3 button_tester.py --buttons 1 2 3 4` 

AT ANY POINT USE CTRL-C to quit out of a running process (like Button Tester) if you're done.
