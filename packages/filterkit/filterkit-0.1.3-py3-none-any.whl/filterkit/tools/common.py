import numpy as np
from PIL import Image
from random import random
from collections import Counter
from threading import Thread
from numba import njit, int8, int16, int64, float32, void
from math import sin, cos, radians, log1p, gcd, pi, sqrt

# TODO: docstrings

@njit
def clamp(value, lower, upper):
    if value < lower:
        return lower
    elif value > upper:
        return upper
    else:
        return value

@njit
def intensity(r, g, b):
    return 0.299 * r + 0.587 * g + 0.114 * b

@njit
def rgb_to_hue_color_model(rgb, model):
    """
    Converts an RGB tuple to its HSV/HSL/HSI version based on the provided model id.\n
    * 0 - Hue Saturation Value color model (HSV)
    * 1 - Hue Saturation Lightness color model (HSL)
    * 2 - Hue Saturation Intensity color model (HSI)
    
    :param rgb: RGB tuple (not normalized/standardized)
    :param model: Hue color model id
    :return: Hue color model version of tuple
    """
    r, g, b = rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0
    cmax, cmin = max(r, g, b), min(r, g, b)
    chroma = cmax - cmin
    if chroma == 0:
        h = 0
    elif cmax == r:
        h = (((g - b) / chroma) % 6) * 60
    elif cmax == g:
        h = (((b - r) / chroma) + 2) * 60
    elif cmax == b:
        h = (((r - g) / chroma) + 4) * 60
    else:
        h = 0
    if model == 0:
        v = cmax
        s = 0 if v == 0 else chroma / v
        return h, s, v
    elif model == 1:
        l = (cmax + cmin) / 2
        s = 0 if l == 0 or l == 1 else chroma / (1 - abs(2 * l - 1))
        return h, s, l
    else:
        i = (r + g + b) / 3
        s = 0 if i == 0 else 1 - cmin / i
        return h, s, i

def get_color_counts(image, chunk_size=1000):
    counter = Counter()
    width, height = image.size
    for y in range(0, height, chunk_size):
        for x in range(0, width, chunk_size):
            box = (x, y, min(x + chunk_size, width), min(y + chunk_size, height))
            region = image.crop(box)
            counter.update(region.getdata())
    color_counts = counter.most_common()
    skip = int((1 / 120) * len(color_counts))   # limit to max of 120 most common colors
    main_colors = [x[0:3] for i, (x, y) in enumerate(color_counts) if i % (skip, 1)[skip == 0] == 0][:120]
    del counter, width, height, color_counts, skip
    return main_colors

def get_masked_image(image, color, alpha, tolerance=15, applied=False):
    """
    Applies a color/transparency mask to image (or removes the color mask if ``applied`` is True), with specified alpha,
    and optional tolerance value.
    
    :param image: PIL Image
    :param color: RGB tuple
    :param alpha: Alpha component [0-255]
    :param tolerance: Similarity of colors to be masked (int)
    :param applied: If this is True, remove mask from image instead
    :return: Masked/unmasked image5
    """
    if image.mode != 'RGBA':
        data = np.array(image.convert('RGBA'))
    else:
        data = np.array(image)
    rgb = data[:, :, :3]
    lower_bound = (np.array(color) - tolerance).clip(0, 255)
    upper_bound = (np.array(color) + tolerance).clip(0, 255)
    mask = np.all((rgb >= lower_bound) & (rgb <= upper_bound), axis=-1)
    data[mask] = [*color, alpha]
    if not applied:
        mask = np.all(rgb == color, axis=-1)
        data[mask] = [*color, 255]
    new_im = Image.fromarray(data)
    del data, rgb, mask
    return new_im

@njit(int16[:, :](int16[:, :], float32[:, :, :]))             # not needed here, maybe can use in quantizer(?)
def palette_lookup(palette, im):
    (rows, cols) = im.shape[:2]
    result = np.zeros((rows, cols), dtype=np.int16)
    for i in range(rows):
        for j in range(cols):
            pr, pg, pb = im[i, j]
            bestindex = 0
            bestdist = 2 ** 20
            for index in range(len(palette)):
                cr, cg, cb = palette[index]
                dist = (pb - cb) ** 2 + (pg - cg) ** 2 + (pr - cr) ** 2
                if dist < bestdist:
                    bestdist = dist
                    bestindex = index
            result[i, j] = bestindex
    return result

@njit(float32[:](float32[:], float32[:, :], int64))
def closest_color(value: np.ndarray, palette: np.ndarray, metric: int):
    """
    Returns a color (RGB) from the palette closest to the given color, using a specified distance metric.\n
    * 0 - Intensity difference
    * 1 - Chebyshev distance
    * 2 - Euclidean distance
    * 3 - Manhattan distance
    * 4 - Cylindrical distance in HSV color space
    * 5 - Conical distance in HSV color space
    * 6 - Cylindrical distance in HSL color space
    * 7 - Conical distance in HSL color space
    * 8 - Cylindrical distance in HSI color space
    * 9 - Conical distance in HSI color space

    :param value: Color
    :param palette: Color palette
    :param metric: Distance metric
    :return: Color from palette
    """
    closest_index = 0
    closest_distance = 2 << 20
    if metric < 4 or metric > 9:
        for i, color in enumerate(palette):
            if metric == 1:         # Chebyshev
                distance = max(abs(value[0] - color[0]), abs(value[1] - color[1]), abs(value[2] - color[2]))
            elif metric == 2:       # Euclidean
                distance = (value[0]-color[0])*(value[0]-color[0]) + (value[1]-color[1])*(value[1]-color[1]) + \
                           (value[2]-color[2])*(value[2]-color[2])
            elif metric == 3:       # Manhattan
                distance = abs(value[0] - color[0]) + abs(value[1] - color[1]) + abs(value[2] - color[2])
            else:                   # Intensity difference
                distance = abs(intensity(value[0], value[1], value[2]) - intensity(color[0], color[1], color[2]))
            if distance < closest_distance:
                closest_index = i
                closest_distance = distance
    else:
        if metric in (4, 5):
            value_ = rgb_to_hue_color_model(value, 0)
        elif metric in (6, 7):
            value_ = rgb_to_hue_color_model(value, 1)
        else:   # the reason why I m doing this is to avoid some branch prediction failure...I dont know why else there is a delay
            value_ = rgb_to_hue_color_model(value, 2)
        for i, color in enumerate(palette):
            if metric in (4, 5):
                color_ = rgb_to_hue_color_model(color, 0)
            elif metric in (6, 7):
                color_ = rgb_to_hue_color_model(color, 1)
            else:
                color_ = rgb_to_hue_color_model(color, 2)
            if metric == 4 or metric == 6 or metric == 8:  # Cylindrical formula
                dh = min(abs(value_[0] - color_[0]), 360 - abs(value_[0] - color_[0]))
                ds = abs(value_[1] - color_[1])
                dv = abs(value_[2] - color_[2])
                distance = sqrt(dh * dh + ds * ds + dv * dv)
            else:                                           # Conic formula
                distance = (sin(value_[0]) * value_[1] * value_[2] - sin(color_[0]) * color_[1] * color_[2]) ** 2 + \
                           (cos(value_[0]) * value_[1] * value_[2] - cos(color_[0]) * color_[1] * color_[2]) ** 2 + \
                           (value_[2] - color_[2]) ** 2
            if distance < closest_distance:
                closest_index = i
                closest_distance = distance
    return palette[closest_index]

@njit(float32(float32, float32[:]))
def closest_level(value: float, palette: np.ndarray):
    """
    Returns an intensity level (0-255) from the grayscale palette closest to the given intensity level.

    :param value: Intensity level
    :param palette: Intensity palette
    :return: Intensity value from palette
    """
    closest_index = 0
    closest_distance = 2 << 20
    for i, color in enumerate(palette):
        distance = abs(value - color)
        if distance < closest_distance:
            closest_index = i
            closest_distance = distance
    return palette[closest_index]

@njit
def access_element_safe(m, i, j):
    rows, cols = m.shape
    clamped_i = clamp(i, 0, rows - 1)
    clamped_j = clamp(j, 0, cols - 1)
    return m[clamped_i, clamped_j]

def check_kernel_oversized(kernel: np.ndarray, image: np.ndarray):
    if any(dim_k > dim_im for dim_k, dim_im in zip(kernel.shape, image.shape)):
        return True
    return False

def ensure_valid_kernel(kernel):
    """
    Ensures a non-ndarray kernel is valid, before it can be converted to a ndarray.\n
    
    :param kernel: Kernel (2d iterable)
    :return: Kernel
    """
    if not isinstance(kernel[0], (list, tuple)) or isinstance(kernel, np.ndarray):
        return kernel
    row_length = max(len(row) for row in kernel)
    valid = [row + [0] * (row_length - len(row)) for row in kernel]
    return valid

def preserve_transparency(func):
    """
    If decorated to a method taking in an image and returning a modified version of the image (same number of channels),
    preserve the transparency/alpha channel and apply the function only to the RGB component if image is in RGBA format.
    
    :param func: Image processing method
    :return: Image
    """
    def wrapper(*args, **kwargs):
        image = args[0]
        if image.mode == 'RGBA':
            r, g, b, a = image.split()
            output = func(Image.merge('RGB', (r, g, b)), *args[1:], **kwargs)
            return Image.merge('RGBA', (*output.split(), a))
        return func(*args, **kwargs)
    return wrapper

def channel_handler(func):
    """
    If decorated to a method taking in an image and returning a modified version of the image (same number of channels),
    apply the function to the channel specified by the method's ``channel`` parameter, if provided.
    
    :param func: Image processing method
    :return: Image
    """
    def wrapper(*args, **kwargs):
        image = args[0]
        mode = image.mode
        if 'channel' in kwargs:
            if image.mode != 'L' and kwargs['channel'] in [0, 1, 2]:
                selected_channel = kwargs.pop('channel')
                channels = list(image.split())
                modified = func(channels[selected_channel], *args[1:], **kwargs)
                channels[selected_channel] = modified
                return Image.merge(mode, channels)
            del kwargs['channel']
        return func(*args, **kwargs)
    return wrapper

def allow_mask(func):
    """
    If decorated to a method taking in a 2D matrix (ndarray) and returning a modified version of the matrix, apply the
    function and then return the masked result of the output using a binary mask (if ``mask`` is specified).
    
    :param func: Matrix processing method
    :return: Matrix
    """
    def wrapper(*args, **kwargs):
        if 'mask' in kwargs:
            original = args[0].copy()
            mask = kwargs.pop('mask')
            output = func(*args, **kwargs)
            if not isinstance(mask, np.ndarray):
                mask = np.array(mask, dtype=int8)
            elif mask.dtype != np.int8:
                mask = mask.astype(np.int8)
            if mask.shape[:2] == args[0].shape[:2]:
                mask_matrix(output, original, mask)
            return output
        return func(*args, **kwargs)
    return wrapper

def mode_exclusive(mode: str = 'gray'):
    """
    If decorated to a method taking in a 2D matrix (ndarray) or an image (PIL) and returning a modified matrix, convert
    matrix/image to given mode, if not already, before applying function and returning. Currently, only supports
    grayscale and RGB modes.\n

    :param mode: Image mode
    :return: Matrix/Image
    """
    if any(sub in str(mode).lower() for sub in ['gray', '0', 'l']) or mode in ['g', 'G']:
        mode = 'L'
    else:
        mode = 'RGB'
        
    def decorator(func):
        def wrapper(*args, **kwargs):
            if isinstance(args[0], Image.Image):
                if args[0].mode != mode:
                    converted = args[0].convert(mode)
                    return func(converted, *args[1:], **kwargs)
            elif isinstance(args[0], np.ndarray):
                if len(args[0].shape) == 3 and mode == 'L':
                    if args[0].shape[2] == 4:
                        rgb = args[0][:, :, :3]
                    else:
                        rgb = args[0]
                    gray = np.mean(rgb, axis=2, dtype=np.float32)
                    return func(gray, *args[1:], **kwargs)
                elif len(args[0].shape) == 2 and mode == 'RGB':
                    rgb = np.stack((args[0], args[0], args[0]))
                    return func(rgb, *args[1:], **kwargs)
            else:
                return func(*args, **kwargs)
            return func(*args, **kwargs)
        return wrapper
    return decorator

def mask_matrix(dst, src, mask):
    """
    Get the masked result of the destination matrix using a binary mask with the reference source matrix.\n
    
    :param dst: Destination/Output matrix
    :param src: Source/Reference matrix
    :param mask: Binary mask/matrix
    :return: Masked matrix
    """
    axes = len(dst.shape)
    if axes == 3:
        _mask_3d(dst, src, mask)
    elif axes == 2:
        _mask_2d(dst, src, mask)

@njit(['void(float32[:, :], float32[:, :], int8[:, :])', 'void(int16[:, :], int16[:, :], int8[:, :])'])
def _mask_2d(dst, src, mask):
    for i in range(dst.shape[0]):
        for j in range(dst.shape[1]):
            if mask[i, j] == 0:
                dst[i, j] = src[i, j]

@njit(['void(float32[:, :, :], float32[:, :, :], int8[:, :])', 'void(int16[:, :, :], int16[:, :, :], int8[:, :])'])
def _mask_3d(dst, src, mask):
    for i in range(dst.shape[0]):
        for j in range(dst.shape[1]):
            if mask[i, j] == 0:
                dst[i, j, 0] = src[i, j, 0]
                dst[i, j, 1] = src[i, j, 1]
                dst[i, j, 2] = src[i, j, 2]

def func_to_channel_parallel(func, matrix, *args, **kwargs):
    if 'output' in kwargs:
        output = kwargs.pop('output')
        thds = []
        for i in range(3):
            thds.append(
                Thread(target=func, args=(matrix[:, :, i], output[:, :, i], *args), kwargs=kwargs, daemon=True))
            thds[-1].start()
        for thd in thds:
            thd.join()

@njit
def circle(radius=3):
    l = np.arange(-radius, radius + 1)
    x, y = np.meshgrid(l, l)
    radius += 0.5
    return np.array((x**2 + y**2) <= radius**2, dtype=int)

@njit
def numba_pad_matrix(matrix, mode, top, bottom, left, right):
    """
    Pad a 2D matrix by making the padded rows/columns have the closest value from matrix.\n
    Equivalent to np.pad(matrix, (top, bottom, left, right)) with mode='constant' when ``mode`` = 0 and mode='edge' when
    ``mode`` = 1.
    
    :param matrix: 2d matrix
    :param top: Top padding
    :param bottom: Bottom padding
    :param left: Left padding
    :param right: Right padding
    :return: Padded matrix
    """
    mx, my = matrix.shape
    integral_matrix_padded = np.zeros((mx + top + bottom, my + left + right), dtype=np.float32)   # padding (edge mode)
    if mode == 1:
        for i in range(integral_matrix_padded.shape[0]):
            for j in range(integral_matrix_padded.shape[1]):
                # Top padding (first few rows)
                if i < top:
                    if j < left:  # top-left corner
                        integral_matrix_padded[i, j] = matrix[0, 0]
                    elif j >= my + left:  # top-right corner
                        integral_matrix_padded[i, j] = matrix[0, my - 1]
                    else:  # first row, between left and right padding
                        integral_matrix_padded[i, j] = matrix[0, j - left]
                # Bottom padding (last few rows)
                elif i >= mx + top:
                    if j < left:  # bottom-left corner
                        integral_matrix_padded[i, j] = matrix[mx - 1, 0]
                    elif j >= my + left:  # bottom-right corner
                        integral_matrix_padded[i, j] = matrix[mx - 1, my - 1]
                    else:  # last row, between left and right padding
                        integral_matrix_padded[i, j] = matrix[mx - 1, j - left]
                # Left padding (first few columns)
                elif j < left:
                    if i < top:  # top-left corner
                        integral_matrix_padded[i, j] = matrix[0, 0]
                    elif i >= mx + top:  # bottom-left corner
                        integral_matrix_padded[i, j] = matrix[mx - 1, 0]
                    else:  # between top and bottom rows, first column
                        integral_matrix_padded[i, j] = matrix[i - top, 0]
                # Right padding (last few columns)
                elif j >= my + left:
                    if i < top:  # top-right corner
                        integral_matrix_padded[i, j] = matrix[0, my - 1]
                    elif i >= mx + top:  # bottom-right corner
                        integral_matrix_padded[i, j] = matrix[mx - 1, my - 1]
                    else:  # between top and bottom rows, last column
                        integral_matrix_padded[i, j] = matrix[i - top, my - 1]
                # Non-padded region (inside the matrix)
                else:
                    integral_matrix_padded[i, j] = matrix[i - top, j - left]
    else:
        for i in range(top, integral_matrix_padded.shape[0]-bottom):
            for j in range(left, integral_matrix_padded.shape[1]-right):
                integral_matrix_padded[i, j] = matrix[i-top, j-left]
    return integral_matrix_padded

@njit(void(float32[:], float32[:, :], int8[:, :], int64, int64))
def numba_masked_1d_copy_to_matrix(src, dst, mask, index, axis):
    if axis == 1:
        for i in range(dst.shape[0]):
            if mask[i, index] == 1:
                dst[i, index] = src[i]
    else:
        for i in range(dst.shape[1]):
            if mask[index, i] == 1:
                dst[index, i] = src[i]

def get_separable_vectors(matrix: np.ndarray):
    """
    Separate a 2D matrix into its row and columns vectors via matrix decomposition.
    
    :param matrix: 2D matrix
    :return: Row and column vector
    """
    U, S, Vt = np.linalg.svd(matrix)
    sigma1 = S[0]
    u1 = U[:, 0]
    v1 = Vt[0, :]
    u = np.sqrt(sigma1) * u1
    v = np.sqrt(sigma1) * v1
    if np.all(u < 0):
        u *= -1
    if np.all(v < 0):
        v *= -1
    return u, v

@njit(float32[:, :](float32[:, :], int64))
def get_integral_matrix(matrix: np.ndarray, offset: int):
    pad_top = offset // 2 + 1
    pad_bottom = offset // 2
    pad_left = offset // 2 + 1
    pad_right = offset // 2
    integral_matrix_padded = numba_pad_matrix(matrix, 1, pad_top, pad_bottom, pad_left, pad_right)
    # Perform the cumulative sum along axis 0 (rows) followed by cumulative sum along axis 1 (columns)
    for i in range(1, integral_matrix_padded.shape[0]):
        for j in range(integral_matrix_padded.shape[1]):
            integral_matrix_padded[i, j] += integral_matrix_padded[i - 1, j]
    for i in range(integral_matrix_padded.shape[0]):
        for j in range(1, integral_matrix_padded.shape[1]):
            integral_matrix_padded[i, j] += integral_matrix_padded[i, j - 1]
    return integral_matrix_padded

@njit
def sequence_gen(i, j, choice, theta=None):
    """
    Generate the next value of a unique series/sequence (specified by ``choice``) for a given coordinate.
    
    :param i: X (Row) index
    :param j: Y (Column) index
    :param theta: Optional coefficient
    :param choice: Sequence id
    :return: Next arbitrary value from chosen series/sequence
    """
    if choice == 0:
        y = ((16807 * i * j) % 2147483647) % 256
    elif choice == 1:
        y = ((16807 * i + j >> 2) % 2147483647) % 256
    elif choice == 2:
        y = ((16807 * j + i >> 2) % 2147483647) % 256
    elif choice == 3:
        y = ((16807 * i) % 2147483647) % 256
    elif choice == 4:
        y = ((16807 * j) % 2147483647) % 256
    elif choice == 5:
        y = ((16807 * 9 * i) % 2147483647) % 256
    elif choice == 6:
        y = ((16807 * 9 * j) % 2147483647) % 256
    elif choice == 7:
        y = ((16807 * 6 * i) % 2147483647) % 256
    elif choice == 8:
        y = ((16807 * 6 * j) % 2147483647) % 256
    elif choice == 9:
        y = ((16807 * sin(i)) % 2147483647) % 256
    elif choice == 10:
        y = ((16807 * sin(j)) % 2147483647) % 256
    elif choice == 11:
        y = ((16807 * radians(i)) % 2147483647) % 256
    elif choice == 12:
        y = ((16807 * radians(j)) % 2147483647) % 256
    elif choice == 13:
        y = ((16807 * gcd(i, j)) % 2147483647) % 256
    elif choice == 14:
        y = ((16807 * gcd(i, theta)) % 2147483647) % 256
    elif choice == 15:
        y = ((16807 * gcd(j, theta)) % 2147483647) % 256
    elif choice == 16:
        y = ((16807 * gcd(i * j, theta)) % 2147483647) % 256
    elif choice == 17:
        y = ((16807 * log1p(i)) % 2147483647) % 256
    elif choice == 18:
        y = ((16807 * cos(pi * i)) % 2147483647) % 256
    else:
        y = 255 * random()
    return y

@njit
def value_modifier(code, arr, x, y, threshold, channel=None, theta=1):
    """
    Apply threshold modification to pixel of image matrix using a method specified by ``code``.
    
    :param code: Method id
    :param arr: Matrix
    :param x: Row index
    :param y: Column index
    :param threshold: Threshold/cutoff value
    :param channel: Optional channel index (necessary for 2D image matrix)
    :param theta: Optional coefficient
    :return: Modified pixel value
    """
    check = channel is not None
    if check:
        if code == 0:       # Min-Max
            return 0 if arr[x, y, channel] < threshold else 255
        if code == 1:       # Min-Max (Inverted)
            return 255 if arr[x, y, channel] < threshold else 0
        if code == 2:       # Set to Matrix
            return arr[x, y, channel] if arr[x, y, channel] < threshold else threshold*2
        if code == 3:       # Set to Matrix (Inverted)
            return arr[x, y, channel]*2 if arr[x, y, channel] < threshold else threshold
        if code == 4:       # Round
            return (arr[x, y, channel]/theta)*5 if arr[x, y, channel] < threshold else arr[x, y, channel]
        if code == 5:       # Rounded Modulo
            return (arr[x, y, channel]+threshold)%255 if arr[x, y, channel] < threshold else ((arr[x, y, channel]-threshold)%255)*2
        if code == 6:       # Gamma Correct
            gamma = theta + ((theta - 5) / 245) * 1.5
            return arr[x, y, channel]**(1/gamma) if arr[x, y, channel] ** (1/gamma) < threshold else arr[x, y, channel]**(1/(gamma-0.05))
        return arr[x, y, channel]
    else:
        if code == 0:  # Min-Max
            return 0 if arr[x, y] < threshold else 255
        if code == 1:  # Min-Max (Inverted)
            return 255 if arr[x, y] < threshold else 0
        if code == 2:  # Set to Matrix
            return arr[x, y] if arr[x, y] < threshold else threshold * 2
        if code == 3:  # Set to Matrix (Inverted)
            return arr[x, y] * 2 if arr[x, y] < threshold else threshold
        if code == 4:  # Round
            return (arr[x, y] / theta) * 5 if arr[x, y] < threshold else arr[x, y]
        if code == 5:  # Rounded Modulo
            return (arr[x, y] + threshold) % 255 if arr[x, y] < threshold else ((arr[x, y] - threshold) % 255) * 2
        if code == 6:  # Gamma Correct
            gamma = theta + ((theta - 5) / 245) * 1.5
            return arr[x, y] ** (1 / gamma) if arr[x, y] ** (1 / gamma) < threshold else arr[x, y] ** (1 / (gamma - 0.05))
        return arr[x, y]
