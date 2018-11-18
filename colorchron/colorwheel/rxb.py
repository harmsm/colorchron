import math

"""
Generic functions for converting between a collection of random channel colors
and RGB.  

Ported from javascript code by Dave Eddy.  This code works by defining
a coordinate transformation between the two maps. See:

https://www.daveeddy.com/2014/07/01/red-yellow-and-blue/
https://github.com/bahamas10/ryb

To use, define a "magic", which is an 8 x 3 list of lists describing the
cube mapping between the rxb colorspace and the rgb colorspace. 
"""
 
def _cubic_interpolate(t, A, B):

    weight = t * t * (3 - 2 * t)
    return A + weight * (B - A)

def _get_red(iR, iY, iB, magic):

    x0 = _cubic_interpolate(iB, magic[0][0], magic[4][0])
    x1 = _cubic_interpolate(iB, magic[1][0], magic[5][0])
    x2 = _cubic_interpolate(iB, magic[2][0], magic[6][0])
    x3 = _cubic_interpolate(iB, magic[3][0], magic[7][0])
    y0 = _cubic_interpolate(iY, x0, x1)
    y1 = _cubic_interpolate(iY, x2, x3)

    return _cubic_interpolate(iR, y0, y1)

def _get_green(iR, iY, iB, magic):

    x0 = _cubic_interpolate(iB, magic[0][1], magic[4][1])
    x1 = _cubic_interpolate(iB, magic[1][1], magic[5][1])
    x2 = _cubic_interpolate(iB, magic[2][1], magic[6][1])
    x3 = _cubic_interpolate(iB, magic[3][1], magic[7][1])
    y0 = _cubic_interpolate(iY, x0, x1)
    y1 = _cubic_interpolate(iY, x2, x3)
  
    return _cubic_interpolate(iR, y0, y1)

def _get_blue(iR, iY, iB, magic):

    x0 = _cubic_interpolate(iB, magic[0][2], magic[4][2])
    x1 = _cubic_interpolate(iB, magic[1][2], magic[5][2])
    x2 = _cubic_interpolate(iB, magic[2][2], magic[6][2])
    x3 = _cubic_interpolate(iB, magic[3][2], magic[7][2])
    y0 = _cubic_interpolate(iY, x0, x1)
    y1 = _cubic_interpolate(iY, x2, x3)

    return _cubic_interpolate(iR, y0, y1)

def rxb_to_rgb(values, magic):
    """
    Take values on some (arbitrarily-defined) color wheel and spit them out as
    RGB values.  The input values are assumed to be between 0 and 1. The final
    RGB values are between 0 and 255. 

    Magic defines the coordinate transformation.  It should be an 8x3 matrix 
    (see description).
    """

    # Make sure that magic is defined properly.  
    tests_failed = False
          
    if len(magic) != 8:
        tests_failed = True

    if sum([len(m) == 3 for m in magic]) != 8:
        tests_failed = True

    if tests_failed:
        err = "magic must be a list of length 8.  Each element must\n"
        err += "be a list of the floats.\n"  
    
        raise ValueError(err)

    R1 = _get_red(*values, magic)
    G1 = _get_green(*values, magic)
    B1 = _get_blue(*values, magic)

    rgb = [math.ceil(R1 * 255),
           math.ceil(G1 * 255),
           math.ceil(B1 * 255)]
   
    return rgb 

