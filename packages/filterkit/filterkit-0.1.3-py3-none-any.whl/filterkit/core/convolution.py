import numpy as np
from numba import njit, prange, float32, int64, void
from PIL import Image
from typing import Iterable

from filterkit.tools.common import preserve_transparency, numba_pad_matrix, get_separable_vectors, \
    func_to_channel_parallel, channel_handler, allow_mask, get_integral_matrix, ensure_valid_kernel, \
    check_kernel_oversized

CONV_NORMAL_LIM = 18
CONV_SEPARABLE_LIM = 100

def convolve_handler(convolve):
    """
    Wrapper to handle parameter management and assignment for convolution functions.
    
    :param convolve: Convolution function
    :return:
    """
    def wrapper(matrix: np.ndarray | Iterable[Iterable[int | float]] | Iterable[Iterable[Iterable[int | float]]],
                *kernels: np.ndarray | Iterable[Iterable[int | float]], **kwargs):
        matrix = matrix.astype(np.float32) if matrix.dtype != np.float32 else matrix
        multi_kernel = len(kernels) > 1
        conv_kernels = []
        if multi_kernel:
            for kernel in kernels:
                if type(kernel) != np.ndarray:
                    kernel = np.array(kernel, dtype=np.float32) if not isinstance(kernel, np.ndarray) else kernel
                elif kernel.dtype != float32:
                    kernel = kernel.astype(np.float32) if kernel.dtype != np.float32 else kernel
                conv_kernels.append(kernel)
        else:
            kernel = np.array(kernels[0], dtype=np.float32) if not isinstance(kernels[0], np.ndarray) else kernels[0]
            kernel = kernel.astype(np.float32) if kernel.dtype != np.float32 else kernel
        if "constant_time" in convolve.__name__:
            if 'handle_boundary' in kwargs:
                handle_boundary = kwargs['handle_boundary']
                kwargs.pop('handle_boundary')
            else:
                handle_boundary = False
            return convolve(matrix, kernel, handle_boundary=handle_boundary)
        elif multi_kernel:
            return convolve(matrix, tuple(conv_kernels))
        else:
            return convolve(matrix, (kernel,) if "normal" in convolve.__name__ else kernel)
    return wrapper

@channel_handler
@preserve_transparency
def apply_convolution(image: Image.Image, *kernels: np.ndarray | Iterable[Iterable[int | float]],
                      separable: bool = False, handle_boundary: bool = True, **kwargs):
    """
    Apply a kernel filter to an image via convolution.\n
    A kernel or set of kernels (e.g. directional kernels for edge detection filters), passed in as individual argument
    parameters, may be provided.\n
    If ``separable`` is specified, it would imply the kernel is separable and an optimized convolution algorithm will be
    used instead. However, if ``separable`` is true and the provided kernel is not separable, the resulting image *will*
    be defective. In general, the convolution process by default tries to use the ideal convolution algorithm for the
    given kernel unless ``separable`` is specified.\n
    ``handle_boundary`` if on, removes any boundary artifacts that may get created when the constant-time convolution
    algorithm is being used, if at all. When off, the convolution process will be faster for the given kernel, but
    boundary artifacts may be visible.\n
    Optional keyword arguments may include ``mask`` which must be a 2D binary matrix which makes the output retain parts
    of the original image where mask == 0.\n
    
    :param image: PIL Image
    :param separable: If true, uses separable convolution
    :param handle_boundary: If true, removes edge effects when constant-time convolution is being used
    :return: Filtered image (if kernel specified)
    """
    # TODO: constant time unsharp mask
    # TODO: check if kernel not bigger than image
    image_np = np.array(image).astype(np.float32)
    if len(kernels) > 1:
        kernels = [ensure_valid_kernel(kernel) for kernel in kernels]
        for kernel in [np.array(kernel) for kernel in kernels]:
            if check_kernel_oversized(kernel, image_np):
                return image
        convolved = convolve_normal(image_np, *kernels, **kwargs)
    elif len(kernels) == 1:
        kernel = ensure_valid_kernel(kernels[0])
        kernel_np = np.array(kernel) if not isinstance(kernel, np.ndarray) else kernel
        if check_kernel_oversized(kernel_np, image_np):
            return image
        if len(kernel_np.shape) == 2 and np.all(kernel_np == kernel[0][0]):
            convolved = box_blur(image_np, len(kernel), **kwargs)
        elif separable:
            if len(kernel) <= CONV_SEPARABLE_LIM:
                convolved = convolve_separate(image_np, kernel_np, **kwargs)
            else:
                convolved = convolve_constant_time(image_np, kernel_np, handle_boundary=handle_boundary, **kwargs)
        else:
            if len(kernel) <= CONV_NORMAL_LIM:
                convolved = convolve_normal(image_np, kernel_np, **kwargs)
            else:
                convolved = convolve_constant_time(image_np, kernel_np, **kwargs)
    else:
        return image
    convolved_image = Image.fromarray(convolved.astype(np.uint8))
    return convolved_image

@allow_mask
@convolve_handler
def convolve_normal(matrix: np.ndarray, kernels):          # best only when kernel radius <= 9
    """
    Convolve a kernel or set of kernels with a 2D matrix.\n
    Kernel must be square. If multiple kernels are provided, each must have the same shape, and will be applied
    successively.\n
    Note: This does *not* convolve in constant time. Hence, it is best to use this for kernels with a radius <=9

    :param matrix: 2D matrix
    :param kernels: Square matrix or tuple of square matrices
    :return: Convolved matrix
    """
    kernel_packed = np.stack(kernels, axis=-1)
    convolved = np.zeros_like(matrix)
    if len(matrix.shape) == 2:
        _convolve2d(matrix, convolved, kernel_packed)
    elif len(matrix.shape) == 3:
        func_to_channel_parallel(_convolve2d, matrix, kernel_packed, output=convolved)
    return convolved

@allow_mask
@convolve_handler
def convolve_separate(matrix: np.ndarray, kernel: np.ndarray):      # great for box/triangle/gaussian blurs
    """
    Convolves a separable kernel matrix with a given 2D matrix in two separate passes by splitting the kernel via matrix
    decomposition, resulting in near constant (yet linear) convolutions for kernels of any radius.\n
    Note: Kernel *must* be separable for this, otherwise convolution result will be faulty.

    :param matrix: 2D matrix
    :param kernel: Separable matrix (2d matrix or tuple of two 1d vectors)
    :return: Convolved matrix
    """
    # TODO: remove slight edge effect
    if not isinstance(kernel, tuple):
        v1, v2 = get_separable_vectors(kernel)
    else:
        if len(kernel) == 2:
            v1, v2 = kernel[0], kernel[1]
        else:
            v1, v2 = kernel[0], kernel[0]
    convolved = np.zeros_like(matrix)
    if len(matrix.shape) == 2:
        _convolve_vectors(matrix, convolved, v1, v2)
    elif len(matrix.shape) == 3:
        func_to_channel_parallel(_convolve_vectors, matrix, v1, v2, output=convolved)
    return convolved

@allow_mask
@convolve_handler
def convolve_constant_time(matrix: np.ndarray, kernel: np.ndarray, handle_boundary: bool = True):
    """
    Convolves a 2D matrix with any odd-sized kernel in near constant time, using the Fast Fourier Transform.\n
    
    :param matrix: 2D matrix
    :param kernel: Separable matrix
    :param handle_boundary: If true, removes boundary artifacts caused by FFT (takes more processing time)
    :return: Convolved matrix
    """
    convolved = np.zeros_like(matrix)
    if len(matrix.shape) == 2:
        _fft_convolve(matrix, convolved, kernel, handle_boundary)
    elif len(matrix.shape) == 3:
        func_to_channel_parallel(_fft_convolve, matrix, kernel, handle_boundary, output=convolved)
    return convolved

@allow_mask
def box_blur(matrix: np.ndarray, radius: int, **kwargs):  # fast box blur
    """
    Optimized box blur implementation for image matrix using integral matrices.\n

    :param matrix: 2D matrix
    :param radius: Kernel radius
    :return: Blurred image matrix
    """
    res = np.zeros_like(matrix)
    if len(matrix.shape) == 2:
        res[:] = _box_blur_routine(matrix, radius)
    elif len(matrix.shape) == 3:
        res[:, :, 0] = _box_blur_routine(matrix[:, :, 0], radius)
        res[:, :, 1] = _box_blur_routine(matrix[:, :, 1], radius)
        res[:, :, 2] = _box_blur_routine(matrix[:, :, 2], radius)
    return res

def _convolve_vectors(matrix: np.ndarray, output: np.ndarray, v1: np.ndarray, v2: np.ndarray, index: int = None):
    # TODO: see if _correlate1d is better here
    half = np.apply_along_axis(lambda m: np.convolve(m, v1, mode='same'), axis=0, arr=matrix)
    result = np.apply_along_axis(lambda m: np.convolve(m, v2, mode='same'), axis=1, arr=half)
    if index is None:
        output[:] = result[:]
    else:
        output[:, :, index] = result[:]
    
@njit(void(float32[:, :], float32[:, :], float32[:, :, :]), parallel=True)
def _convolve2d(matrix: np.ndarray, output: np.ndarray, kernels: np.ndarray):
    matrix_height, matrix_width = matrix.shape
    kernel_height, kernel_width = kernels.shape[:2]
    pad_height = kernel_height // 2
    pad_width = kernel_width // 2           # Pad the matrix with zeros around the edges
    padded_matrix = numba_pad_matrix(matrix, 1, pad_height, pad_height, pad_width, pad_width)
    for i in prange(matrix_height):
        for j in range(matrix_width):
            conv_sum = 0.0
            for k in range(kernels.shape[2]):
                conv_sum_k = 0.0
                for ki in range(kernel_height):
                    for kj in range(kernel_width):
                        row_idx = i + ki
                        col_idx = j + kj        # Perform element-wise multiplication and sum for each kernel
                        conv_sum_k += padded_matrix[row_idx, col_idx] * kernels[ki, kj, k]
                conv_sum += (conv_sum_k * conv_sum_k)
            output[i, j] = max(0, min(255, int(np.sqrt(conv_sum))))

@njit(void(float32[:, :], float32[:, :], float32[:], int64), parallel=True)
def _correlate_vector2d(matrix, output, weights, axis):
    k = len(weights)
    offset = k // 2
    axis = max(0, min(1, axis))
    n = matrix.shape[1] if axis == 0 else matrix.shape[0]
    offrange = (-offset, offset) if k % 2 == 0 else (-offset, offset + 1)
    if axis == 1:
        matrix = matrix.transpose((1, 0))
        output = output.transpose((1, 0))
    for i in prange(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            for k in range(*offrange):
                if j + k < 0:
                    tmp = matrix[i, abs(j + k) - 1]
                    output[i, j] += tmp * weights[k + offset]
                elif j + k >= n:
                    tmp = matrix[i, n - (j + k + 1)]
                    output[i, j] += tmp * weights[k + offset]
                else:
                    output[i, j] += matrix[i, j + k] * weights[k + offset]

@njit(void(float32[:, :, :], float32[:, :, :], float32[:], int64), parallel=True)
def _correlate_vector(matrix, output, weights, axis):
    # parallelized 1D correlation along specified axis for RGB matrix
    k = len(weights)
    offset = k // 2
    axis = max(0, min(2, axis))
    n = matrix.shape[1] if axis == 0 else matrix.shape[0] if axis == 1 else 3
    offrange = (-offset, offset) if k % 2 == 0 else (-offset, offset + 1)
    if axis == 0 or axis == 1:
        if axis == 1:
            matrix = matrix.transpose((1, 0, 2))
            output = output.transpose((1, 0, 2))
        for i in prange(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                for k in range(*offrange):
                    for c in range(3):
                        if j + k < 0:
                            tmp = matrix[i, abs(j + k) - 1, c]
                            output[i, j, c] += tmp * weights[k + offset]
                        elif j + k >= n:
                            tmp = matrix[i, n - (j + k + 1), c]
                            output[i, j, c] += tmp * weights[k + offset]
                        else:
                            output[i, j, c] += matrix[i, j + k, c] * weights[k + offset]
    else:
        for i in prange(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                for k in range(*offrange):
                    for c in range(3):
                        if c + k < 0:
                            output[i, j, c] += matrix[i, j, 0] * weights[k + offset]
                        elif c + k >= n:
                            output[i, j, c] += matrix[i, j, n - 1] * weights[k + offset]
                        else:
                            output[i, j, c] += matrix[i, j, c] * weights[k + offset]

def _fft_convolve(matrix: np.ndarray, output: np.ndarray, kernel: np.ndarray, handle_boundary: bool):
    if handle_boundary:
        kx, ky = kernel.shape
        matrix = np.pad(matrix, ((kx // 2, ky // 2), (kx // 2, ky // 2)), 'edge')
    sz = (matrix.shape[0] - kernel.shape[0], matrix.shape[1] - kernel.shape[1])     # Pad the kernel to be the same shape as the matrix
    kernel = np.pad(kernel, (((sz[0] + 1) // 2, sz[0] // 2), ((sz[1] + 1) // 2, sz[1] // 2)), 'constant')
    kernel = np.fft.ifftshift(kernel)       # Perform FFT routine on both kernel and matrix
    fft1 = np.fft.rfft2(kernel)
    if matrix.shape[1] % 2 == 1:
        fft2 = np.fft.rfft2(matrix[:, :-1])
    else:
        fft2 = np.fft.rfft2(matrix)
    inv_fft = np.fft.irfft2(fft1 * fft2)        # Perform element-wise multiplication of the FFTs to get the convolution
    if handle_boundary:
        inv_fft = inv_fft[kx // 2:-kx // 2 + 1, ky // 2:-ky // 2 + 1]  # Cropping the padded region if matrix was padded
    output[:] = np.clip(inv_fft, 0, 255)                               # removes the boundary artifacts

@njit(float32[:, :](float32[:, :], int64), parallel=True)
def _box_blur_routine(matrix: np.ndarray, k: int):      # basically get the mean of matrix given window size
    integral = get_integral_matrix(matrix, k)
    sum_matrix = np.zeros_like(matrix)
    for i in prange(k, integral.shape[0]):
        for j in range(k, integral.shape[1]):
            sum_matrix[i - k, j - k] = (integral[i, j] + integral[i - k, j - k] -
                                        integral[i, j - k] - integral[i - k, j]) / (k ** 2)
    return sum_matrix
    