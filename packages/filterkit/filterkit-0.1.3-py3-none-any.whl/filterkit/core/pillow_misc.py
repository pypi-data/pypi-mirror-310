from PIL import Image, ImageOps
from typing import Tuple, List

from filterkit.tools.common import preserve_transparency

@preserve_transparency
def make_duotone_or_tritone(image: Image.Image, black: Tuple[int, int, int], white: Tuple[int, int, int], midtone: Tuple[int, int, int] = None,
                     black_point: int = 20, white_point: int = 230, mid_point: int = 128) -> Image.Image:
    """
    Makes an image consist of only gradients between two or three colors.\n
    The algorithm essentially entails converting the image to grayscale (if not already) and then linearly interpolating
    between the specified colors for every pixel intensity/gray value, depending on the intensity interval the
    pixel lies in; pixels with intensities less than ``black_point`` are assigned to ``black``, pixels with intensities
    greater than ``white_point`` are assigned ``white`` (similarly for ``midpoint``), and pixels between these two colors
    (or between ``black`` and `` mid``, and between ``mid and ``white``) are interpolated.
    
    :param image: PIL Image
    :param black: Color chosen to represent the darker colors
    :param white: Color chosen to represent the lighter colors
    :param midtone: Color chosen to represent mid-tones (between ``black`` and ``white``) of image
    :param black_point: Pixels with intensities smaller than this are assigned ``black`` [0-255]
    :param white_point: Pixels with intensities greater than this are assigned ``white`` [0-255]
    :param mid_point: Pixels with intensities closer to midpoint are assigned ``mid`` [0-255]
    :return:
    """
    black_point = max(0, min(255, black_point)) if black_point is not None else 20
    white_point = max(0, min(255, white_point)) if white_point is not None else 230
    mid_point = max(0, min(255, mid_point)) if mid_point is not None else 128
    if image.mode != 'L':
        image = image.convert('L')
    if black_point > white_point:
        temp = black_point
        black_point = white_point
        white_point = temp
    if black_point > mid_point:
        temp = black_point
        black_point = mid_point
        mid_point = temp
    if not midtone:
        return ImageOps.colorize(image, black, white, blackpoint=black_point, whitepoint=white_point)
    else:
        return ImageOps.colorize(image, black, white, midtone, black_point, white_point, mid_point)

@preserve_transparency
def apply_autocontrast(image: Image.Image, threshold: float | List[float] | Tuple[float, float]):
    if isinstance(threshold, float):
        threshold = max(0.0, min(1.0, threshold)) if threshold is not None else 0.2
    else:
        lower = max(0.0, min(1.0, threshold[0])) if threshold[0] is not None else 0.2
        upper = max(0.0, min(1.0, threshold[1])) if threshold[1] is not None else 0.2
        threshold = (lower, upper)
    return ImageOps.autocontrast(image, threshold)

@preserve_transparency
def fast_bit_quantization(image: Image.Image, strength: int | float = 4):
    """
    Image quantization by reducing the number of bits to represent colors in each channel.
    
    :param image: PIL Image
    :param strength: The strength of quantization [0.1-1.0] or [1-100]
    :return: Quantized image
    """
    
    if isinstance(strength, int):
        strength = max(1, min(100, strength))
        if 0 < strength <= 100:
            strength = int(1 + ((strength - 1) * 7) / 99)
    elif isinstance(strength, float):
        strength = max(0.1, min(1.0, strength))
        if 0.0 < strength <= 1.0:
            strength = int(1 + ((strength - 0.1) * 7) / 0.9)
    else:
        strength = 4
    mask = ~(2 ** (8 - strength) - 1)
    lut = [i & mask for i in range(256)]
    if image.mode == 'RGB':
        lut = lut * 3
    image = image.point(lut)
    return image

@preserve_transparency
def equalise_histogram(image: Image.Image, mask: Image.Image = None):
    """
    Evenly spreads out the intensity levels among each channel in the area specified by the white pixels in ``mask`` or
    the whole image if ``mask`` is not specified.
    
    :param image: PIL Image
    :param mask: PIL Image (binary)
    :return: Equalised image
    """
    if mask:
        if mask.mode == '1':
            return ImageOps.equalize(image, mask)
    else:
        return ImageOps.equalize(image)

