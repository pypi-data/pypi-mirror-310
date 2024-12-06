from PIL import Image
import numpy as np
from numba import njit, float32, void, int64

from filterkit.tools.common import clamp, intensity, preserve_transparency

@njit
def _apply_separate(primary, secondary, x, y, func):
    """
    Applies a blend function to the primary matrix value at (``x, y``) using the secondary matrix's value, by applying to
    each channel separately.
    
    :param primary: Base matrix
    :param secondary: Blend matrix
    :param x: Row coordinate
    :param y: Column coordinate
    :param func: Blend function
    :return:
    """
    if not isinstance(primary[x, y], np.float32):
        for i in range(len(primary[x, y])):
            c1, c2 = primary[x, y][i], secondary[x, y][i]
            primary[x, y][i] = func(c1, c2)
    else:
        primary[x, y] = func(primary[x, y], secondary[x, y])

@njit
def _apply_composite(primary, secondary, x, y, func):
    """
    Applies a blend function to the primary matrix value at (``x, y``) using the secondary matrix's value, by applying to
    the pixel directly.
    
    :param primary: Base matrix
    :param secondary: Blend matrix
    :param x: Row coordinate
    :param y: Column coordinate
    :param func: Blend function
    :return:
    """
    if not isinstance(primary[x, y], np.float32):
        r1, g1, b1 = primary[x, y][0], primary[x, y][1], primary[x, y][2]
        r2, g2, b2 = secondary[x, y][0], secondary[x, y][1], secondary[x, y][2]
        i1, i2 = intensity(r1, g1, b1), intensity(r2, g2, b2)
        primary[x, y][:3] = func(r1, r2, i1, i2), func(g1, g2, i1, i2), func(b1, b2, i1, i2)
        if len(primary[x, y]) == 4:
            primary[x, y][3] = func(primary[x, y][3], secondary[x, y][3], i1, i2)
    else:
        primary[x, y] = func(primary[x, y], secondary[x, y], primary[x, y], secondary[x, y])

@njit
def _darken(a, b):
    return a if a < b else b

@njit
def _lighten(a, b):
    return a if a > b else b

@njit
def _darker_color(a, b, i1, i2):
    return a if i1 < i2 else b

@njit
def _lighter_color(a, b, i1, i2):
    return a if i1 > i2 else b

@njit
def _multiply(a, b):
    return clamp((a / 255.0) * (b / 255.0), 0.0, 1.0) * 255

@njit
def _divide(a, b):
    return clamp((b / 255.0) / ((a / 255.0) + 1e-5), 0.0, 1.0) * 255

@njit
def _color_burn(a, b):
    return clamp(1 - (1 - b / 255.0) / ((a / 255.0) + 1e-5), 0.0, 1.0) * 255

@njit
def _linear_burn(a, b):
    return clamp((a / 255.0) + (b / 255.0) - 1, 0.0, 1.0) * 255

@njit
def _color_dodge(a, b):
    return clamp((b / 255.0) / (1 - (a / 255.0) + 1e-5), 0.0, 1.0) * 255

@njit
def _linear_dodge(a, b):
    return clamp((a / 255.0) + (b / 255.0), 0.0, 1.0) * 255

@njit
def _screen(a, b):
    return clamp(1 - (1 - (a / 255.0)) * (1 - (b / 255.0)), 0.0, 1.0) * 255

@njit
def _soft_light(a, b, i1, i2):
    return _screen(a, b) / 2 if i1 > i2 else _multiply(a, b) / 2

@njit
def _hard_light(a, b, i1, i2):
    return _linear_dodge(a, b) / 2 if i1 > i2 else _linear_burn(a, b) / 2

@njit
def _vivid_light(a, b, i1, i2):
    return _color_dodge(a, b) / 2 if i1 > i2 else _color_burn(a, b) / 2

@njit
def _pin_light(a, b, i1, i2):
    return _lighten(a, b) / 2 if i1 > i2 else _darken(a, b) / 2

@njit
def _hard_mix(a, b):
    return 255 if a + b >= 255 else 0

@njit
def _difference(a, b):
    return a - b if a > b else b - a

@njit
def _subtract(a, b):
    return clamp((a / 255.0) - (b / 255.0), 0.0, 1.0) * 255

@njit
def _exclusion(a, b):
    return _difference(a, b) if a != b else 128

@njit(['void(float32[:,:,:], float32[:,:,:], int64)', 'void(float32[:,:], float32[:,:], int64)'])
def _blend(img1, img2, mode):
    img_h, img_w = img1.shape[:2]
    for h in range(img_h):
        for w in range(img_w):
            if mode == 0:
                _apply_separate(img1, img2, h, w, _lighten)
            elif mode == 1:
                _apply_separate(img1, img2, h, w, _darken)
            elif mode == 2:
                _apply_separate(img1, img2, h, w, _multiply)
            elif mode == 3:
                _apply_separate(img1, img2, h, w, _divide)
            elif mode == 4:
                _apply_separate(img1, img2, h, w, _color_burn)
            elif mode == 5:
                _apply_separate(img1, img2, h, w, _linear_burn)
            elif mode == 6:
                _apply_separate(img1, img2, h, w, _screen)
            elif mode == 7:
                _apply_composite(img1, img2, h, w, _lighter_color)
            elif mode == 8:
                _apply_composite(img1, img2, h, w, _darker_color)
            elif mode == 9:
                _apply_separate(img1, img2, h, w, _color_dodge)
            elif mode == 10:
                _apply_separate(img1, img2, h, w, _linear_dodge)
            elif mode == 11:
                _apply_composite(img1, img2, h, w, _soft_light)
            elif mode == 12:
                _apply_composite(img1, img2, h, w, _hard_light)
            elif mode == 13:
                _apply_composite(img1, img2, h, w, _vivid_light)
            elif mode == 14:
                _apply_composite(img1, img2, h, w, _pin_light)
            elif mode == 15:
                _apply_separate(img1, img2, h, w, _hard_mix)
            elif mode == 16:
                _apply_separate(img1, img2, h, w, _difference)
            elif mode == 17:
                _apply_separate(img1, img2, h, w, _subtract)
            elif mode == 18:
                _apply_separate(img1, img2, h, w, _exclusion)
            else:
                continue

@preserve_transparency      # will be removed when alpha blending is added
def apply_blending(image: Image.Image, layer: Image.Image, style: int = 0):
    """
    Blend an image with another layer inplace using the blend mode specified by ``style``.\n
    If the blend image is not of the same mode as the base image, it is converted to the base image's mode. This
    means a grayscale base image will only be blended with grayscale version of the blend image/layer, unless it
    is already grayscale, and likewise for color images and images with transparency.\n
    * 0 - Lighten
    * 1 - Darken
    * 2 - Multiply
    * 3 - Divide
    * 4 - Color Burn
    * 5 - Linear Burn
    * 6 - Screen
    * 7 - Lighter Color
    * 8 - Darker Color
    * 9 - Color Dodge
    * 10 - Linear Dodge (Add)
    * 11 - Soft Light
    * 12 - Hard Light
    * 13 - Vivid Light
    * 14 - Pin Light
    * 15 - Hard Mix
    * 16 - Difference
    * 17 - Subtract
    * 18 - Exclusion
    
    :param image: Base image to be blended into
    :param layer: Image/layer to be blended in
    :param style: Blend mode [0-18]
    :return: Blended version of base image
    """
    # TODO: Alpha blending/compositing
    if layer.mode != image.mode:
        layer = layer.convert(image.mode)
    if layer.size != image.size:
        layer = layer.resize(image.size)
    image_np1 = np.array(image, dtype=np.float32)
    image_np2 = np.array(layer, dtype=np.float32)
    _blend(image_np1, image_np2, style)
    blended_image = Image.fromarray(image_np1.astype('uint8'))
    return blended_image
