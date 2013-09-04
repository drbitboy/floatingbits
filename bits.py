
import math
import numpy

def fpfromints(ints):
  lsw,msw = tuple(ints)
  SIGN = -1 if (lsw&32768) else +1
  if SIGN < 0: lsw -= 32768
  EXPONENT = (lsw / 128) - 127
  MANTISSA = 65536.0 * (lsw - (128.0 * (EXPONENT+126.0))) + msw

  return SIGN, EXPONENT, MANTISSA, SIGN * MANTISSA * math.pow(2.0,EXPONENT) / 8388608

for inp1 in '12.34 24.68 6.17 3.085 1.5425 0.77125 30 15 7.5 3.75 1.875 0.9375 2 1 .5'.split():
  for inp in [inp1,'-'+inp1]:
    na = numpy.array(inp,dtype=numpy.float32)
    nastring = na.tostring()
    ints = list(numpy.fromstring( nastring,dtype=numpy.uint16))
    byts = list(numpy.fromstring(nastring,dtype=numpy.uint8))
    ints.reverse()
    byts.reverse()
    print( ( '%12f' % na, '%3x'*4 % tuple(byts), '%5x'*2 % tuple(ints), byts, ints, fpfromints(ints), ) )
