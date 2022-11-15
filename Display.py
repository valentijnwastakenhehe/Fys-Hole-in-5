#+-----+-----+---------+------+---+--- N2 ---+---+------+---------+-----+-----+
# | I/O | wPi |   Name  | Mode | V | Physical | V | Mode |  Name   | wPi | I/O |
# +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
# |     |     |    3.3V |      |   |  1 || 2  |   |      | 5V      |     |     |
# | 493 |   8 |   SDA.2 | ALT1 | 1 |  3 || 4  |   |      | 5V      |     |     |
# | 494 |   9 |   SCL.2 | ALT1 | 1 |  5 || 6  |   |      | 0V      |     |     |
# | 473 |   7 |  IO.473 |   IN | 0 |  7 || 8  | 1 | ALT1 | TxD1    | 15  | 488 |
# |     |     |      0V |      |   |  9 || 10 | 1 | ALT1 | RxD1    | 16  | 489 |
# | 479 |   0 |  IO.479 |   IN | 1 | 11 || 12 | 1 | IN   | IO.492  | 1   | 492 |
# | 483 |   3 |  IO.483 |   IN | 1 | 15 || 16 | 1 | IN   | IO.476  | 4   | 476 |
# |     |     |    3.3V |      |   | 17 || 18 | 1 | IN   | IO.477  | 5   | 477 |
# | 484 |  12 |    MOSI | ALT4 | 1 | 19 || 20 |   |      | 0V      |     |     |
# | 485 |  13 |    MISO | ALT4 | 1 | 21 || 22 | 1 | IN   | IO.478  | 6   | 478 |
# | 487 |  14 |    SCLK | ALT4 | 1 | 23 || 24 | 1 | OUT  | CE0     | 10  | 486 |
# |     |     |      0V |      |   | 25 || 26 | 0 | IN   | IO.464  | 11  | 464 |
# | 474 |  30 |   SDA.3 | ALT2 | 1 | 27 || 28 | 1 | ALT2 | SCL.3   | 31  | 475 |
# | 490 |  21 |  IO.490 | ALT1 | 0 | 29 || 30 |   |      | 0V      |     |     |
# | 491 |  22 |  IO.491 |   IN | 1 | 31 || 32 | 0 | IN   | IO.472  | 26  | 472 |
# | 481 |  23 |  IO.481 |   IN | 1 | 33 || 34 |   |      | 0V      |     |     |
# | 482 |  24 |  IO.482 |   IN | 0 | 35 || 36 | 1 | OUT  | IO.495  | 27  | 495 |
# |     |  25 |   AIN.3 |      |   | 37 || 38 |   |      | 1V8     | 28  |     |
# |     |     |      0V |      |   | 39 || 40 |   |      | AIN.2   | 29  |     |
# +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
# | I/O | wPi |   Name  | Mode | V | Physical | V | Mode |  Name   | wPi | I/O |
# +-----+-----+---------+------+---+--- N2 ---+---+------+---------+-----+-----+










#lcd pin 1 = ground : odroid pin 6
#lcd pin 2 = power : odroid pin 2 (5v)
#lcd pin 3 = power : odroid pin 1 (3.3)
#lcd pin 4 = rs : odroid pin 3
#lcd pin 5 = rw : odroid pin 5
#lcd pin 6 = enable signal : odroid pin 8
#lcd pin 11 = data 4 : odroid pin 16
#lcd pin 12 = data 5 : odroid pin 18
#lcd pin 13 = data 6 : odroid pin 22
#lcd pin 14 = data 7 : odroid pin 26

import odroid_wiringpi as wpi
import RPi.GPIO hs GPIO
import time 

#GPIO WPI MAPPING 
LCD_RS = 
