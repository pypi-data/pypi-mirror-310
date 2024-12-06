# TODO: this module is a work in progress and experimental
# TODO: updated documentation soon
from PIL import Image
from math import sqrt
from numba import njit, prange, float32, float64, int64, boolean
import numpy as np

from filterkit.tools.common import mode_exclusive, get_integral_matrix, preserve_transparency
from filterkit.tools.kernel_gen import gaussian_kernel_1d
from filterkit.core.convolution import _correlate_vector, convolve_separate

def filter_handler(_filter):
    """
    Wrapper to handle parameter management for miscellaneous image filtering functions.
    
    :param _filter: Image filter function
    :return:
    """
    def wrapper(*args, **kwargs):
        image = args[0]
        image_np = np.array(image).astype(np.float32) if not isinstance(image, np.ndarray) else image
        image_np = image_np.astype(np.float32) if isinstance(image_np, np.ndarray) and image_np.dtype != np.float32 else image_np
        filtered = _filter(image_np, *args[1:], **kwargs)
        return Image.fromarray(filtered.astype(np.uint8))
    return wrapper

@njit
def _mean_and_variance(matrix, window_size):
    """
    Get the mean and variance matrices by computing them locally within a radius ``window_size`` for every value in
    ``matrix``.\n
    
    :param matrix: 2D matrix (ndarray)
    :param window_size: Window/Neighborhood size
    :return: Mean and Variance matrices (tuple)
    """
    k = window_size
    mean = np.zeros_like(matrix)
    variance = np.zeros_like(matrix)
    integral = get_integral_matrix(matrix, k)
    integral_squares = get_integral_matrix(matrix * matrix, k)
    for i in prange(k, integral.shape[0]):
        for j in range(k, integral.shape[1]):
            window_mean = (integral[i, j] + integral[i - k, j - k] -
                           integral[i, j - k] - integral[i - k, j]) / (k ** 2)
            window_squares_mean = (integral_squares[i, j] + integral_squares[i - k, j - k] -
                                   integral_squares[i, j - k] - integral_squares[i - k, j]) / (k ** 2)
            window_variance = window_squares_mean - window_mean ** 2
            mean[i - k, j - k] = max(0.0, min(255.0, window_mean))
            variance[i - k, j - k] = max(0.0, min(255.0, window_variance))
    return mean, variance

@mode_exclusive('L')
@filter_handler
@njit(float32[:, :](float32[:, :], int64, float64, boolean), parallel=True)
def apply_niblack_threshold(matrix: np.ndarray, window_size: int, coefficient: float, invert: bool):    # sketching like effect; good for OCR
    """
    Thresholding technique using the local neighborhood around a pixel to find the difference of local mean and
    standard deviation.\n
    
    :param matrix: Image matrix (2D)
    :param window_size: Window/neighborhood radius
    :param coefficient: Coefficient for std. deviation
    :param invert: If true, returns inverted threshold result
    :return: Thresholded image
    """
    k = 2 * window_size + 1
    coefficient = max(-4.0, min(4.0, coefficient))      # -4.0 <= coefficient <= 4.0
    mean, variance = _mean_and_variance(matrix, k)
    std_dev = np.sqrt(variance)
    threshold_mask = mean - std_dev * np.float32(coefficient)
    threshold_mask = np.clip(threshold_mask, 0.0, 255.0)
    for i in prange(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            matrix[i, j] = (255.0 if matrix[i, j] < threshold_mask[i, j] else 0.0) if not invert else \
                           (0.0 if matrix[i, j] < threshold_mask[i, j] else 255.0)
    return matrix

@mode_exclusive('L')
@filter_handler
@njit(float32[:, :](float32[:, :], int64, float64, boolean), parallel=True)
def apply_sauvola_threshold(matrix: np.ndarray, window_size: int, coefficient: float, invert: bool):      # blackboard like effect; good for OCR
    """
    Modification of the Niblack thresholding algorithm that gives potentially less noisy results.\n
    
    :param matrix: Image matrix (2D)
    :param window_size: Window/neighborhood radius
    :param coefficient: Coefficient for std. deviation
    :param invert: If true, returns inverted threshold result
    :return: Thresholded image
    """
    k = 2 * window_size + 1
    coefficient = max(-4.0, min(4.0, coefficient))  # -4.0 <= coefficient <= 4.0
    mean, variance = _mean_and_variance(matrix, k)
    std_dev = np.sqrt(variance)
    threshold_mask = mean * (1 + np.float32(coefficient) * ((std_dev / 1.0) - 1))       # R has been set to 1.0 for now
    threshold_mask = np.clip(threshold_mask, 0.0, 255.0)
    for i in prange(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            matrix[i, j] = (255.0 if matrix[i, j] < threshold_mask[i, j] else 0.0) if not invert else \
                (0.0 if matrix[i, j] < threshold_mask[i, j] else 255.0)
    return matrix

def pixelize(image: Image.Image, strength: float | int):
    """
    Pixelates an image with given strength.\n

    :param image: PIL Image
    :param strength: Pixelation strength [1-999]
    :return: Pixelated image
    """
    strength = (920 if strength > 999 or strength < 1 else strength) if strength is not None else 920
    try:
        original_size = image.size
        pixelated = image.resize((int(image.width * (1000 - strength) / 1000),
                                  int(image.height * (1000 - strength) / 1000)))
        pixelated = pixelated.resize(original_size, Image.NEAREST)
    except ValueError:
        return image
    return pixelated

@preserve_transparency
@mode_exclusive('RGB')
@filter_handler
@njit(float32[:, :, :](float32[:, :, :], float64, float64))
def matrixify(matrix: np.ndarray, K: int, M: int):                      # 1 <= K <= 10000 ; 1 <= M <= 300
    # black and white matrix like filter
    height, width = matrix.shape[:2]
    dists = np.full(matrix.shape[:2], np.inf, dtype=matrix.dtype)
    cluster_map = np.full(matrix.shape[:2], -1, dtype=np.int16)
    K, M = max(1, min(K, 10000)), max(1, min(300, M))
    N = matrix.shape[0] * matrix.shape[1]
    S = int(sqrt(N / K))
    h = S // 2
    w = S // 2
    centers = []
    clusters = []
    while h < height:
        while w < width:
            centers.append([h, w, matrix[h, w, 0], matrix[h, w, 1], matrix[h, w, 2]])
            w += S
        w = S // 2
        h += S
    for cid in range(len(centers)):
        center = centers[cid]
        cluster = []
        cy, cx = center[0], center[1]
        start_y = max(cy - S // 2, 0)
        end_y = min(cy + S // 2, height)
        start_x = max(cx - S // 2, 0)
        end_x = min(cx + S // 2, width)
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                d_rgb = sqrt((matrix[y, x, 0] - center[2]) ** 2 + (matrix[y, x, 1] - center[3]) ** 2 +
                                (matrix[y, x, 2] - center[4]) ** 2)
                d_xy = sqrt((y - center[0]) ** 2 + (x - center[1]) ** 2)
                Ds = d_rgb + (M / S) * d_xy
                if Ds < dists[y, x]:
                    cluster.append([y, x])
                    cluster_map[y, x] = cid
                    dists[y, x] = Ds
        clusters.append(cluster)
    out = np.clip(dists, 0.0, 255.0)
    return np.stack((out, out, out), axis=-1)

@preserve_transparency
@mode_exclusive('RGB')
@filter_handler
@njit(float32[:, :, :](float32[:, :, :], int64, int64, int64), parallel=True)
def superpixelate(matrix: np.ndarray, count: int, similarity: int, iterations: int):
    """
    Clusters pixels similar in color together over the entire matrix, creating a 'superpixel' like effect.\n
    ``count`` specifies the number of superpixels to create, while ``similarity`` determines how similar every superpixel
    is to each other; in general, the greater this value, the more square/uniformly shaped the superpixel.\n
    The clustering algorithm used is related to the SLIC-segmentation algorithm.\n
    
    :param matrix: Image matrix (RGB only)
    :param count: Approximate number of superpixels
    :param similarity: 'Square' factor; the bigger this is, the more square/similar the superpixels will be in shape
    :param iterations: Number of times to perform clustering; more iterations means a cleaner result, but is capped at 30
            (Optional)
    :return: Superpixelated image
    """
    height, width = matrix.shape[:2]
    count, similarity, iterations = max(1, min(20000, count)), max(1, min(4000, similarity)), max(1, min(30, iterations))
    S = int(sqrt(height * width / count))           # average size of each superpixel
    centers = []
    for h in range(int(S / 2), height, S):
        for w in range(int(S / 2), width, S):       # superpixel center (format: x, y, red(x,y), green(x,y), blue(x,y) )
            centers.append([h, w, matrix[h, w, 0], matrix[h, w, 1], matrix[h, w, 2]])
    centers = np.array(centers, dtype=np.float32)
    next_centers = np.zeros((len(centers), 5), np.float32)
    cluster_sizes = np.zeros(len(centers), np.float32)
    dists = np.full((height, width), np.inf, dtype=np.float32)
    cluster_map = np.full((height, width), -1, dtype=np.int32)
    for i in range(iterations):
        cluster_map[:] = -1
        dists[:] = np.inf
        for cid in prange(len(centers)):
            c = centers[cid]
            start_h = max(int(c[0] - S), 0)
            end_h = min(int(c[0] + S), height)
            start_w = max(int(c[1] - S), 0)
            end_w = min(int(c[1] + S), width)
            for h in range(start_h, end_h):
                for w in range(start_w, end_w):
                    r, g, b = matrix[h, w, 0], matrix[h, w, 1], matrix[h, w, 2]
                    Dc = sqrt((r - c[2]) ** 2 + (g - c[3]) ** 2 + (b - c[4]) ** 2)
                    Ds = sqrt((h - c[0]) ** 2 + (w - c[1]) ** 2)
                    D = Dc + similarity * Ds / S        # updating superpixel centroid score
                    if D < dists[h, w]:
                        cluster_map[h, w] = cid         # update centroid cluster based on score
                        dists[h, w] = D
        for h in range(height):
            for w in range(width):
                cid = cluster_map[h, w]
                next_centers[cid, 0] += h               # update centroid
                next_centers[cid, 1] += w
                next_centers[cid, 2] += matrix[h, w, 0]
                next_centers[cid, 3] += matrix[h, w, 1]
                next_centers[cid, 4] += matrix[h, w, 2]
                cluster_sizes[cid] += 1
        for cid in range(len(centers)):
            if cluster_sizes[cid]:
                next_centers[cid] //= cluster_sizes[cid]
                centers[cid][:] = next_centers[cid]
        next_centers[:] = 0
        cluster_sizes[:] = 0
    for x in range(height):
        for y in range(width):
            center = centers[cluster_map[x, y]]
            matrix[x, y] = center[2], center[3], center[4]
    return matrix

@preserve_transparency
@mode_exclusive('RGB')
@filter_handler
def xray(matrix: np.ndarray, sigma: float | int, alpha: int, grayscale: bool = True):  # 0.2 <= sigma <= 31.8; 1 <= alpha <= 100
    # # x-ray like ghostly effect
    sigma, alpha = max(0.2, min(50, sigma)), max(1, min(100, alpha))
    g0, g1 = gaussian_kernel_1d(sigma, 0), gaussian_kernel_1d(sigma, 1)
    ret1 = convolve_separate(matrix, g1, g0)
    ret2 = convolve_separate(matrix, g0, g1)
    ret3_ax3 = np.zeros_like(matrix)
    ret3 = convolve_separate(matrix, g0, g0)
    _correlate_vector(ret3, ret3_ax3, g1, 2)
    out = np.sqrt(ret1 ** 2 + ret2 ** 2 + ret3_ax3 ** 2)
    out = (1.0 / np.sqrt(1.0 + alpha * out)) * 255
    if not grayscale:
        return out
    else:
        gray = np.mean(out, axis=-1)
        return np.stack((gray, gray, gray), axis=-1)

# TODO: check out more scikitimage rank based
# TODO: check out scikitimage morphology
# TODO: flood fill
