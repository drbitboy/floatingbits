Summary
=======

  Rockwell Automation PLC-5 utility

  Emulate conversion from a one-element, IEEE-754 32-floating point file
  and a two-element, 16-bit integer file, and vice versa.  By emulate is
  meant to show what integer values result from a floating point value, and
  vice versa.


Usage
=====

  Open floatingbits.html in a Web Browser; file 

    ./scripts/jquery-1.9.0.min.js

  needs to be accessible and in the directory scripts/ which is a sibling
  of floatingbits.html.


Details
=======


Here's the full conversion from 28876 and 16709 to floating-point (FP) value
12.34.


Let's say LSW and MSW are in Binary file 4 with 2 elements  (like your B3
example)


LSW is B4:0 = 16709

MSW is B4:1 = 28836


The bits, from MSBit to LSB, LSW then MSW, are

1. B4:0/15 => 1 bit for sign (set=1 if FP is negative, unset=0 if FP is
positive)
 - for 16709, B4:0/15 is unset, so the number is positive (so far, so good)
 - negative numbers will either have B4:0 greater than 32767 (interpreting
16-bits as an UN-signed Int); or have B4:0 as a negative
number (interpreting 16-bits as a signed Int).
2. B4:0/14 to B4:0/7 => 8 bits evaluated as an 8-bit integer (1-255;
exponent value of zero has a special meaning), minus 127 to give base-two
exponent
 - Int(16709 / 128) - 127 = 130 - 127 = 3
 - 2 to the 3rd power = 8, so the number is between 8 and 16 (8*2) (still so
far so good).
3. B4:0/6 to B4:0/0 and B4:1/15 to B4:1/0 => (7 + 16 =) 23 bits to
represent mantissa-equivalent = bits after binamal (analogous to decimal)
point with an implied leading 1 bit set before the binamal point
 - 16 LSBits (B4:1) are 28836
 - 1+7 most significant bits:
     - 7 bits from LSW = 16709 % 128 = 16709 - (130 * 128) = 69
     - Implicit leading 1 bit:  add 128
     - 69 + 128 = 197  ((197 / 128) * 8 = 12.3125, close to 12.34, still so
far so good)
 - To combine them, left-shift the MSBits by 16-bits and add to the LSBits:
     - (197 * 65536) + 28836 = 12939428
 - and divide that by 2^23 (= 8388608) to shift the binamal point 23 places
to the left;
     - 12939428 / 8388608 = 1.5425

Finally, combining everything: + 1.5425 * (2^3) = 1.5425 * 8 = 12.34


QED?


So, for the general case using *Integer* files, assuming LSW and MSW = N4:0
and N4:1, UN-signed 16-bit integers

SIGN:  +1 if N4:0/1 is unset; -1 if set

EXPONENT:  int( (N4:0 - (int(N4:0/32768) * 32768) / 128) - 127

MANTISSA:  65536.0 * (int( (N4:0 - (int(N4:0/32768) * 32768) - (128 *
(EXPONENT+126))) + N4:1

FP = [SIGN]  MANTISSA * 2^EXPONENT


- N.B. implicit leading 1-bit in MANTISSA is provided by adding +126
instead of +127 in MANTISSA formula above
