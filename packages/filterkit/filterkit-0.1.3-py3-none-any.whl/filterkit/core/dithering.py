import numpy as np
from PIL import Image
from random import randint
from numba import njit, float32, float64, int64, prange
from typing import Iterable

from filterkit.tools.common import closest_level, closest_color, sequence_gen, value_modifier, \
    preserve_transparency, channel_handler, allow_mask

def dither_handler(dither):
    """
    Wrapper to handle parameter management and assignment for dither functions.
    
    :param dither: Dither function
    :return:
    """
    def wrapper(matrix: np.ndarray | Iterable[Iterable[int | float]] | Iterable[Iterable[Iterable[int | float]]],
                kernel: np.ndarray | Iterable[Iterable[int | float]] = None,
                palette: np.ndarray | Iterable[int | float] | Iterable[Iterable[int | float]] = None,
                **kwargs):
        method = kwargs.get('method', 0)
        method = method if method is not None else 0
        threshold = kwargs.get('threshold', 127.0)
        threshold = max(0.0, min(255.0, threshold)) if threshold is not None else 127.0
        pattern = kwargs.get('pattern', -1)
        pattern = pattern if pattern is not None else -1
        theta = kwargs.get('theta', 0.8)
        theta = max(-2.0, min(2.0, theta)) if theta is not None else 0.8
        default_rgb = kwargs.get('default_rgb', True)
        default_rgb = True if default_rgb is None else default_rgb
        if "ordered" not in dither.__name__:
            method = 1 if method else 0
        else:
            theta = max(0.1, min(1.2, theta))
        if not kernel:
            if "ordered" in dither.__name__:
                kernel = ((0, 0.5, 0.125, 0.625), (0.75, 0.25, 0.875, 0.375), (0.1875, 0.6875, 0.0625, 0.5625),
                          (0.9375, 0.4375, 0.8125, 0.3125))                         # Bayer dither
            else:
                kernel = ((0, 0, 0), (0, 0, 0.4375), (0.1875, 0.3125, 0.0625))      # Floyd Steinberg dither
        if not palette:
            if len(matrix.shape) == 3:
                if default_rgb:
                    palette = [[0, 0, 0], [255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 255]]         # RGB palette
                else:
                    palette = [[0, 0, 0], [255, 255, 0], [255, 0, 255], [0, 255, 255], [255, 255, 255]]  # CMYK palette
            elif len(matrix.shape) == 2:
                palette = [0, 255]      # grayscale
        kernel = np.array(kernel, dtype=np.float32) if not isinstance(kernel, np.ndarray) else kernel
        palette = np.array(palette, dtype=np.float32) if not isinstance(palette, np.ndarray) else palette
        kernel = kernel.astype(np.float32) if kernel.dtype != np.float32 else kernel
        matrix = matrix.astype(np.float32) if matrix.dtype != np.float32 else matrix
        palette = palette.astype(np.float32) if palette.dtype != np.float32 else palette
        if len(matrix.shape) == 3 and matrix.shape[2] == 3:
            palette = np.unique(palette, axis=0)    # Remove duplicate RGB
        elif len(matrix.shape) == 2:
            palette = np.unique(palette)            # Remove duplicate levels/reshapes 2D palette to 1D
        if len(matrix.shape) == 3 and len(palette.shape) == 1:
            palette_pad = (3 - len(palette) % 3) % 3  # Padding gives the number of elements to add, if any channel missing in tuples
            palette = np.pad(palette, (0, palette_pad), mode='constant', constant_values=0)  # Missing channels are set to 0
            palette = palette[:len(palette) // 3 * 3].reshape(-1, 3)  # Group into RGB
        if "normal" in dither.__name__:
            return dither(matrix, kernel, palette, theta)
        elif "ordered" in dither.__name__:
            return dither(matrix, kernel, palette, theta, method)
        elif "directional" in dither.__name__:
            return dither(matrix, kernel, palette, theta, method)
        elif "uniform" in dither.__name__:
            return dither(matrix, palette, threshold, method)
        elif "random" in dither.__name__:
            return dither(matrix, palette, threshold, method, pattern)
    return wrapper

@channel_handler
@preserve_transparency
def apply_dithering(image: Image.Image, style: int = 1, kernel: np.ndarray | Iterable[Iterable[int | float]] = None,
                    palette: np.ndarray | Iterable[int | float] | Iterable[Iterable[int | float]] = None,
                    threshold: float | int = None, theta: float | int = None, method: int = None, pattern: int = None,
                    default_rgb: bool = True, **kwargs) -> Image.Image:
    """
    Apply error diffusion/ordered dithering to an image with the dithering method specified by ``style``.\n
    The dithering style value can range from 0 to 5 corresponding to Random dithering, Normal error diffusion,
    Uniform error diffusion, Vertical error diffusion, Horizontal error diffusion, Ordered dithering, in order.\n
    A kernel can only be specified when applying normal/horizontal/vertical error diffusion in list/tuple/numpy
    array format and must be square, with the elements not part of the original matrix being set to 0.\n
    The color palette to be used while dithering can also be specified in a similar format, otherwise it will
    default to a basic RGB palette or CMYK palette (if ``default_rgb`` is False).\n
    Normal/horizontal/vertical dithers accept a theta parameter, which is used as a coefficient/multiplier for
    modifying the base dithering behaviour.\n
    Similarly, the ``threshold`` parameter can be specified when using the uniform/random dithers, to dither only those
    pixels whose intensity is within a threshold.\n
    The ``method`` parameter can be specified for uniform/random/ordered dithers to modify the dither behaviour.\n
    Additionally, the random dither accepts a ``pattern`` parameter specifying the id of the method to generate
    randomized patterns while dithering.\n
    If no palette is specified, the dither will use a basic RGB palette unless ``default_rgb`` is False, whereby a CMYK
    palette will be used instead.\n
    Note: Transparent images will not have their alpha channels modified.

    :param image: PIL Image
    :param style: Dithering style [0 - 4]
    :param kernel: Dither matrix/kernel
    :param palette: Color palette
    :param threshold: Intensity threshold
    :param theta: Coefficient/multiplier
    :param method: Alternate dithering behaviour (integer)
    :param pattern: Dither pattern id for random dither
    :param default_rgb: Use RGB instead of CMYK if no palette specified (True or False)
    :return: Dithered image
    """
    # TODO: pattern dither
    kwargs = {**{key: value for key, value in locals().items() if key not in ['image', 'style', 'kwargs']}, **kwargs}
    gray = image.mode == 'L'
    image_np = np.array(image).astype(np.float32)
    if style == 0:
        dithered = (_random_dither, _random_dither_2d)[gray](image_np, **kwargs)
    elif style == 2:
        dithered = (_error_diffuse_uniform, _error_diffuse_uniform_2d)[gray](image_np, **kwargs)
    elif style == 3:
        dithered = (_error_diffuse_directional, _error_diffuse_directional_2d)[gray](image_np, **kwargs)
    elif style == 4:
        dithered = (_ordered_dither, _ordered_dither_2d)[gray](image_np, **kwargs)
    else:
        dithered = (_error_diffuse_normal, _error_diffuse_normal_2d)[gray](image_np, **kwargs)
    dithered_image = Image.fromarray(dithered.astype(np.uint8))
    return dithered_image

@allow_mask
@dither_handler
@njit(float32[:, :, :](float32[:, :, :], float32[:, :], float32[:, :], float64))
def _error_diffuse_normal(matrix, kernel, palette, theta) -> np.ndarray:		# requires kernel to be square
    lx, ly = matrix.shape[:2]
    start = -(len(kernel) // 2)
    end = -start
    range_end = -start + 1
    error = [0, 0, 0]
    for y in range(lx):
        for x in range(ly):
            rounded = closest_color(matrix[y, x], palette, 2)
            error[0] = (matrix[y, x][0] - rounded[0])
            error[1] = (matrix[y, x][1] - rounded[1])
            error[2] = (matrix[y, x][2] - rounded[2])
            error[0], error[1], error[2] = error[0] * theta, error[1] * theta, error[2] * theta
            matrix[y, x][0], matrix[y, x][1], matrix[y, x][2] = rounded[0], rounded[1], rounded[2]
            for m in range(start, range_end):
                for n in range(start, range_end):
                    if kernel[m + end, n + end] != 0:
                        if 0 <= y + m < lx and 0 <= x + n < ly:
                            matrix[y + m, x + n][0] += kernel[m + end, n + end] * error[0]
                            matrix[y + m, x + n][1] += kernel[m + end, n + end] * error[1]
                            matrix[y + m, x + n][2] += kernel[m + end, n + end] * error[2]
    return matrix

@allow_mask
@dither_handler
@njit(float32[:, :](float32[:, :], float32[:, :], float32[:], float64))
def _error_diffuse_normal_2d(matrix, kernel, palette, theta) -> np.ndarray:
    lx, ly = matrix.shape[:2]
    start = -(len(kernel) // 2)
    end = -start
    range_end = -start + 1
    for y in range(lx):
        for x in range(ly):
            rounded = closest_level(matrix[y, x], palette)
            error = (matrix[y, x] - rounded) * theta
            matrix[y, x] = rounded
            for m in range(start, range_end):
                for n in range(start, range_end):
                    if kernel[m + end, n + end] != 0:
                        if 0 <= y + m < lx and 0 <= x + n < ly:
                            matrix[y + m, x + n] += kernel[m + end, n + end] * error
    return matrix

@allow_mask
@dither_handler
@njit(float32[:, :, :](float32[:, :, :], float32[:, :], float32[:, :], float64, int64))
def _error_diffuse_directional(matrix, kernel, palette, theta, alt) -> np.ndarray:
    lx, ly, lz = matrix.shape
    kx, ky = kernel.shape
    kh, kw = kx // 2, ky // 2
    duotone = len(palette) == 2
    error_matrix = np.zeros((lx + 2 * kh, ly + 2 * kw, 3), dtype=np.float32)
    error_matrix[kh:-kh, kw:-kw] = matrix[:, :]
    result = np.zeros((lx, ly, lz), dtype=np.float32)
    for x in range((lx, ly)[alt]):
        if alt:
            old_value = error_matrix[kh:-kh, x]
        else:
            old_value = error_matrix[x, kw:-kw]
        if duotone:
            for y in range((ly, lx)[alt]):
                dist1 = (abs(old_value[y][0] - palette[0][0]) + abs(old_value[y][1] - palette[0][1]) +
                         abs(old_value[y][2] - palette[0][2]))
                dist2 = (abs(old_value[y][0] - palette[1][0]) + abs(old_value[y][1] - palette[1][1]) +
                         abs(old_value[y][2] - palette[1][2]))
                if alt:
                    result[:, x][y] = palette[0] if dist1 < dist2 else palette[1]
                else:
                    result[x][y] = palette[0] if dist1 < dist2 else palette[1]
        else:
            for y in range((ly, lx)[alt]):
                if alt:
                    result[:, x][y] = closest_color(old_value[y], palette, 2)
                else:
                    result[x][y] = closest_color(old_value[y], palette, 2)
        error = np.zeros(((ly, lx)[alt], 3), dtype=np.float32)
        for y in range((ly, lx)[alt]):
            error[y][0] = (old_value[y][0] - (result[x][y][0], result[:, x][y][0])[alt]) * theta
            error[y][1] = (old_value[y][1] - (result[x][y][1], result[:, x][y][1])[alt]) * theta
            error[y][2] = (old_value[y][2] - (result[x][y][2], result[:, x][y][2])[alt]) * theta
        for m in range(-kh, kh + 1):
            for n in range(-kw, kw + 1):
                if kernel[m + kh, n + kw] != 0:
                    if 0 <= (x + m, x + n)[alt] < (lx, ly)[alt]:
                        for y in range((ly, lx)[alt]):
                            if alt:
                                error_matrix[kh + n + y, x + m][0] += error[y][0] * kernel[m + kh, n + kw]
                                error_matrix[kh + n + y, x + m][1] += error[y][1] * kernel[m + kh, n + kw]
                                error_matrix[kh + n + y, x + m][2] += error[y][2] * kernel[m + kh, n + kw]
                            else:
                                error_matrix[x + m, kw + n + y][0] += error[y][0] * kernel[m + kh, n + kw]
                                error_matrix[x + m, kw + n + y][1] += error[y][1] * kernel[m + kh, n + kw]
                                error_matrix[x + m, kw + n + y][2] += error[y][2] * kernel[m + kh, n + kw]
    return result

@allow_mask
@dither_handler
@njit(float32[:, :](float32[:, :], float32[:, :], float32[:], float64, int64))
def _error_diffuse_directional_2d(matrix, kernel, palette, theta, alt) -> np.ndarray:
    lx, ly = matrix.shape
    kx, ky = kernel.shape
    kh, kw = kx // 2, ky // 2
    duotone = len(palette) == 2
    error_matrix = np.zeros((lx + 2 * kh, ly + 2 * kw), dtype=np.float32)
    error_matrix[kh:-kh, kw:-kw] = matrix[:, :]
    result = np.zeros((lx, ly), dtype=np.float32)
    for x in range((lx, ly)[alt]):
        if alt:
            old_value = error_matrix[kh:-kh, x]
        else:
            old_value = error_matrix[x, kw:-kw]
        if duotone:
            for y in range((ly, lx)[alt]):
                dist1 = old_value[y] - palette[0]
                dist2 = old_value[y] - palette[1]
                if alt:
                    result[:, x][y] = palette[0] if dist1 < dist2 else palette[1]
                else:
                    result[x][y] = palette[0] if dist1 < dist2 else palette[1]
        else:
            for y in range((ly, lx)[alt]):
                if alt:
                    result[:, x][y] = closest_level(old_value[y], palette)
                else:
                    result[x][y] = closest_level(old_value[y], palette)
        error = np.zeros(((ly, lx)[alt],), dtype=np.float32)
        for y in range((ly, lx)[alt]):
            error[y] = (old_value[y] - (result[x][y], result[:, x][y])[alt]) * theta
        for m in range(-kh, kh + 1):
            for n in range(-kw, kw + 1):
                if kernel[m + kh, n + kw] != 0:
                    if 0 <= (x + m, x + n)[alt] < (lx, ly)[alt]:
                        for y in range((ly, lx)[alt]):
                            if alt:
                                error_matrix[kh + n + y, x + m] += error[y] * kernel[m + kh, n + kw]
                            else:
                                error_matrix[x + m, kw + n + y] += error[y] * kernel[m + kh, n + kw]
    return result

@njit
def _uniform_error(i, j, alt):
    return ((((i ^ (j * 149)) * 1234 & 511) / 511.0) * 255 - 127.5,
            (((i + (j * 237)) * 119 & 255) / 255.0) * 255 - 127.5)[alt]  # xor if method=0, add if method=1

@allow_mask
@dither_handler
@njit(float32[:, :, :](float32[:, :, :], float32[:, :], float64, int64))
def _error_diffuse_uniform(matrix, palette, threshold, alt) -> np.ndarray:       # fast (ordered) error diffusion
    lx, ly, _ = matrix.shape
    duotone = len(palette) == 2
    value = np.array([0.0, 0.0, 0.0], dtype=np.float32)
    r = 1 / 2 ** (1 / 3) if palette is None else 1 / len(palette) ** (1 / 3)
    for j in range(ly):
        for i in range(lx):
            err = _uniform_error(i, j, alt)
            if duotone:
                intensity = matrix[i, j][0] * 0.2126 + matrix[i, j][1] * 0.7152 + matrix[i, j][2] * 0.0722
                if intensity + r * err >= threshold:
                    matrix[i, j] = palette[1]
                else:
                    matrix[i, j] = palette[0]
            else:
                value[0] = matrix[i, j][0] + r * err
                value[1] = matrix[i, j][1] + r * err
                value[2] = matrix[i, j][2] + r * err
                matrix[i, j] = closest_color(value, palette, 2)
    return matrix

@allow_mask
@dither_handler
@njit(float32[:, :](float32[:, :], float32[:], float64, int64))
def _error_diffuse_uniform_2d(matrix, palette, threshold, alt) -> np.ndarray:       # fast (ordered) error diffusion
    lx, ly = matrix.shape
    duotone = len(palette) == 2
    r = 1 / 2 ** (1 / 3) if palette is None else 1 / len(palette) ** (1 / 3)
    for j in range(ly):
        for i in range(lx):
            err = _uniform_error(i, j, alt)
            if duotone:
                intensity = matrix[i, j]
                if intensity + r * err >= threshold:
                    matrix[i, j] = palette[1]
                else:
                    matrix[i, j] = palette[0]
            else:
                value = matrix[i, j] + r * err
                matrix[i, j] = closest_level(value, palette)
    return matrix

@njit
def _random_dither_common_routine(x, y, palette, weights, intensity, threshold, alt, pattern, duotone):
    if intensity <= threshold:
        rand = sequence_gen(x, y, pattern, intensity)
        if duotone:
            color = palette[1] if alt else palette[0] if intensity > rand else (palette[0] if alt else palette[1])
        else:
            choice = randint(0, len(palette) - 1)
            color = (palette[choice]) if intensity * 1.5 > rand else (palette[np.argmin(weights)] if alt else palette[np.argmax(weights)])
    else:
        color = palette[1] if duotone else palette[0]
    return color

@allow_mask
@dither_handler
@njit(float32[:, :, :](float32[:, :, :], float32[:, :], float64, int64, int64), parallel=True)
def _random_dither(matrix, palette, threshold, alt, pattern) -> np.ndarray:
    lx, ly = matrix.shape[:2]
    duotone = len(palette) == 2
    weights = np.array([sum(clr) / 3 for clr in palette], dtype=np.float32)
    for i in prange(lx):
        for j in range(ly):
            intensity = (matrix[i, j, 0] + matrix[i, j, 1] + matrix[i, j, 2])/3
            color = _random_dither_common_routine(i, j, palette, weights, intensity, threshold, alt, pattern, duotone)
            matrix[i, j] = color[0], color[1], color[2]
    return matrix

@allow_mask
@dither_handler
@njit(float32[:, :](float32[:, :], float32[:], float64, int64, int64), parallel=True)
def _random_dither_2d(matrix, palette, threshold, alt, pattern) -> np.ndarray:
    lx, ly = matrix.shape
    duotone = len(palette) == 2
    weights = np.array([clr for clr in palette], dtype=np.float32)
    for i in prange(lx):
        for j in range(ly):
            intensity = matrix[i, j]
            color = _random_dither_common_routine(i, j, palette, weights, intensity, threshold, alt, pattern, duotone)
            matrix[i, j] = color
    return matrix

@allow_mask
@dither_handler
@njit(float32[:, :, :](float32[:, :, :], float32[:, :], float32[:, :], float64, int64), parallel=True)
def _ordered_dither(matrix, kernel, palette, theta, method) -> np.ndarray:        # 0.1 <= theta <= 1.2
    kernel = kernel * 255
    x_shape, y_shape = matrix.shape[0], matrix.shape[1]
    kernel_x_shape, kernel_y_shape = kernel.shape[0], kernel.shape[1]
    for i in prange(x_shape):
        for j in range(y_shape):
            x_index = i % kernel_x_shape
            y_index = j % kernel_y_shape
            check_value = kernel[x_index, y_index]
            if method != 7:     # if method == 7, just apply the palette quantization below
                matrix[i, j][0] = value_modifier(method, matrix, i, j, check_value, 0, theta)
                matrix[i, j][1] = value_modifier(method, matrix, i, j, check_value, 1, theta)
                matrix[i, j][2] = value_modifier(method, matrix, i, j, check_value, 2, theta)
            matrix[i, j][:] = closest_color(matrix[i, j], palette, 2)
    return matrix

@allow_mask
@dither_handler
@njit(float32[:, :](float32[:, :], float32[:, :], float32[:], float64, int64), parallel=True)
def _ordered_dither_2d(matrix, kernel, palette, theta, method) -> np.ndarray:
    kernel = kernel * 255
    x_shape, y_shape = matrix.shape[0], matrix.shape[1]
    kernel_x_shape, kernel_y_shape = kernel.shape[0], kernel.shape[1]
    for i in prange(x_shape):
        for j in range(y_shape):
            x_index = i % kernel_x_shape
            y_index = j % kernel_y_shape
            check_value = kernel[x_index, y_index]
            if method != 7:     # if method == 7, just apply the palette quantization below
                matrix[i, j] = value_modifier(method, matrix, i, j, check_value, theta=theta)
            matrix[i, j] = closest_level(matrix[i, j], palette)
    return matrix
