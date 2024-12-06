from math import sqrt
from random import randint
from PIL import Image
import numpy as np
from typing import Iterable
from numba import njit, float32, int64, prange, void, int32, boolean
from numba.core.types import Tuple

from filterkit.tools.common import closest_color, closest_level, channel_handler, preserve_transparency, allow_mask

def quantize_handler(quantize):
    """
    Wrapper to handle parameter management and assignment for all quantization methods.

    :param quantize: Quantization function
    :return:
    """
    def wrapper(matrix: np.ndarray | Iterable[Iterable[int | float]] | Iterable[Iterable[Iterable[int | float]]],
                palette: np.ndarray | Iterable[int | float] | Iterable[Iterable[int | float]] = None, **kwargs):
        if not palette:
            if len(matrix.shape) == 3 and matrix.shape[2] == 3:     # Custom default 'watercolor' palette
                palette = [(23, 32, 56), (37, 58, 94), (60, 94, 139), (79, 143, 186), (115, 190, 211), (164, 221, 219), (25, 51, 45), (37, 86, 46), (70, 130, 50), (117, 167, 67), (168, 202, 88), (208, 218, 145), (77, 43, 50), (122, 72, 65), (173, 119, 87), (192, 148, 115), (215, 181, 148), (231, 213, 179),
                           (52, 28, 39), (96, 44, 44), (136, 75, 43), (190, 119, 43), (222, 158, 65), (232, 193, 112), (36, 21, 39), (65, 29, 49), (117, 36, 56), (165, 48, 48), (207, 87, 60), (218, 134, 62), (30, 29, 57), (64, 39, 81), (122, 54, 123), (162, 62, 140), (198, 81, 151), (223, 132, 165),
                           (9, 10, 20), (16, 20, 31), (21, 29, 40), (32, 46, 55), (57, 74, 80), (87, 114, 119), (129, 151, 150), (168, 181, 178), (199, 207, 204), (235, 237, 233)]
            elif len(matrix.shape) == 2:
                palette = [0, 64, 128, 192, 255]  # grayscale
        metric = kwargs.get('metric', 2)
        metric = max(0, min(9, metric)) if metric is not None else 2
        num_colors = kwargs.get('num_colors', 8)
        num_colors = max(1, min(512, num_colors)) if num_colors is not None else 8
        blur_radius = kwargs.get('blur_radius', 3)
        blur_radius = max(1, min(100, blur_radius)) if blur_radius is not None else 3
        clustering_iterations = kwargs.get('clustering_iterations', 1)
        clustering_iterations = max(1, min(16, clustering_iterations)) if clustering_iterations is not None else 1
        cluster_init_method = kwargs.get('cluster_init_method', 0)
        cluster_init_method = max(0, min(2, cluster_init_method)) if cluster_init_method is not None else 0
        levels_range_adjusted = kwargs.get('levels_range_adjusted', False)
        levels_range_adjusted = False if levels_range_adjusted is None else levels_range_adjusted
        flipped_centroid_orient = kwargs.get('flipped_centroid_orient', False)
        flipped_centroid_orient = False if flipped_centroid_orient is None else flipped_centroid_orient
        matrix = matrix.astype(np.float32) if matrix.dtype != np.float32 else matrix
        palette = np.array(palette, dtype=np.float32) if not isinstance(palette, np.ndarray) else palette
        palette = palette.astype(np.float32) if palette.dtype != np.float32 else palette
        if len(matrix.shape) == 3 and matrix.shape[2] == 3:
            palette = np.unique(palette, axis=0)
        elif len(matrix.shape) == 2:
            palette = np.unique(palette)
        if "normal" in quantize.__name__:
            return quantize(matrix, palette, metric)
        elif "grayscale" in quantize.__name__:
            return quantize(matrix, num_colors, metric, levels_range_adjusted)
        elif "clustering" in quantize.__name__:
            return quantize(matrix, num_colors, clustering_iterations, cluster_init_method, flipped_centroid_orient)
        elif "blur" in quantize.__name__:
            return quantize(matrix, num_colors, blur_radius)
    return wrapper

@channel_handler
@preserve_transparency
def apply_quantization(image: Image.Image, method: int = 0,
                       palette: np.ndarray | Iterable[int | float] | Iterable[Iterable[int | float]] = None,
                       metric: int = None, num_colors: int = None, blur_radius: int = None, levels_range_adjusted: bool = False,
                       clustering_iterations: int = None, cluster_init_method: int = None, flipped_centroid_orient: bool = False, **kwargs):
    """
    Quantize an image to a palette or a set number of colors with the quantization method specified by ``method``.\n
    The method id can range from 0 to 3 corresponding to quantization via distance metric, quantization via grayscale
    image (only for RGB images), k-means clustering quantization, or blur quantization.\n
    If ``palette`` is specified, it must be a list/tuple of color tuples/lists or a list/tuple of intensity levels.\n
    If ``num_colors`` is specified, any specified palette may be ignored since the algorithm being used most likely is
    quantizing the image to this number of colors.\n
    ``metric`` corresponds to the distance metric method being used, if the algorithm uses it, and can range from 0-9.
    If the method id corresponds to blur quantization, the ``blur_radius`` may be specified, and represents the gaussian
    blur kernel's radius; the greater the radius, the stronger the blur/quantizing effect.\n
    When using quantization via grayscale image, ``levels_range_adjusted`` may be specified which may/may not quantize
    the image more fittingly.\n
    Other optional parameters like ``clustering_iterations, cluster_init_method, flipped_centroid_orient`` can be given
    when using k-means clustering for quantization.\n
    Note: Transparent images will not have their alpha channels modified.

    :param image: PIL Image
    :param method: Quantization method id [0-3]
    :param palette: Color palette
    :param metric: Distance metric method id [0-9]
    :param num_colors: Number of colors to quantize image to
    :param blur_radius: Gaussian blur kernel radius [1-100] (Optional)
    :param levels_range_adjusted: If true, adjust min/max intensity range (Optional)
    :param clustering_iterations: Number of times k-means clustering is done [1-10] (Optional)
    :param cluster_init_method: Method id for initialising centroids in k-means clustering [0-2] (Optional)
    :param flipped_centroid_orient: If true, centroids created on a vertical basis, else horizontally in k-means
            clustering (Optional)
    :return: Quantized image
    """
    # TODO: median cut quantization
    kwargs = {**{key: value for key, value in locals().items() if key not in ['image', 'method', 'kwargs']}, **kwargs}
    gray = image.mode == 'L'
    image_np = np.array(image).astype(np.float32)
    if method == 1:
        quantized = _quantize_with_grayscale(image_np, **kwargs) if not gray else image_np
    elif method == 2:
        quantized = _quantize_with_kmeans_clustering(image_np, **kwargs)
    elif method == 3:
        quantized = _quantize_with_blur(image_np, **kwargs)
    else:
        quantized = _quantize_normal(image_np, **kwargs)
    quantized_image = Image.fromarray(quantized.astype(np.uint8))
    return quantized_image

@allow_mask
@quantize_handler
@njit(['float32[:, :, :](float32[:, :, :], float32[:, :], int64)', 'float32[:, :](float32[:, :], float32[:], int64)'], parallel=True)
def _quantize_normal(matrix, palette, metric) -> np.ndarray:
    """
    General image quantization using a given distance metric method.\n
    Metric id can be any of the following:
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

    :param matrix: Image matrix
    :param palette: Color palette
    :param metric: id for distance metric calculation [0-9]
    :return:
    """
    lx, ly = matrix.shape[:2]
    gray = isinstance(matrix[0, 0], np.float32)
    for i in prange(lx):
        for j in range(ly):
            if gray:
                matrix[i, j] = closest_level(matrix[i, j], palette)
            else:
                matrix[i, j][:] = closest_color(matrix[i, j], palette, metric)
    return matrix

@allow_mask
@quantize_handler
@njit(float32[:, :, :](float32[:, :, :], int64, int64, boolean), parallel=True)
def _quantize_with_grayscale(matrix, n, metric, range_adjusted) -> np.ndarray:
    """
    Image quantization using the grayscale method. Only supported for color (RGB) images.

    :param matrix: Image matrix
    :param n: Number of colors image is to be quantized to
    :param metric: id for distance metric calculation [0-9]
    :param range_adjusted: If this is true, the quantized levels will range from the min intensity to the max intensity
            of the image's grayscale version, otherwise defaults from 0 to 255
    :return: Quantized image (RGB)
    """
    lx, ly = matrix.shape[:2]
    gray = np.float32(0.2989) * matrix[:, :, 0] + np.float32(0.5870) * matrix[:, :, 1] + np.float32(0.1140) * matrix[:, :, 2]
    if range_adjusted:
        unique_gray_values = sorted(set([int(g) for row in gray for g in row]))
        levels = [min(unique_gray_values) + i * (max(unique_gray_values) - min(unique_gray_values)) / (n - 1) for i in range(n)]
    else:
        levels = [(i * 256 / n + (256 / n) * (i + 1)) / 2 for i in range(n)]
    colors = np.zeros((n, 3), dtype=np.float32)
    for li, level in enumerate(levels):
        closest_distance = 2 << 20
        closest_index = [0, 0]
        for i in range(lx):
            for j in range(ly):
                distance = abs(gray[i, j] - level)
                if distance < closest_distance:
                    closest_distance = distance
                    closest_index[:] = [i, j]
        i, j = closest_index[0], closest_index[1]
        colors[li][:] = matrix[i, j]
    for i in prange(lx):
        for j in range(ly):
            color = closest_color(matrix[i, j], colors, metric)
            matrix[i, j, 0] = color[0]
            matrix[i, j, 1] = color[1]
            matrix[i, j, 2] = color[2]
    return matrix

@njit(void(float32[:, :, :], float32[:, :, :], float32[:, :], int64, int64), parallel=True)
def _qblur_routine(matrix, ret, ks, c, s):
    for i in prange(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            r, g, b = 0, 0, 0
            for p in range(-s, s + 1):
                for q in range(-s, s + 1):
                    x = max(0, min(matrix.shape[0]-1, i + p))
                    y = max(0, min(matrix.shape[1]-1, j + q))
                    r += matrix[x, y, 0] * ks[p + s, q + s]
                    g += matrix[x, y, 1] * ks[p + s, q + s]
                    b += matrix[x, y, 2] * ks[p + s, q + s]
            ret[i, j, 0] = round(r) // c * c
            ret[i, j, 1] = round(g) // c * c
            ret[i, j, 2] = round(b) // c * c

@njit(void(float32[:, :], float32[:, :], float32[:, :], int64, int64), parallel=True)
def _qblur_routine_2d(matrix, ret, ks, c, s):
    for i in prange(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            g = 0
            for p in range(-s, s + 1):
                for q in range(-s, s + 1):
                    x = max(0, min(matrix.shape[0]-1, i + p))
                    y = max(0, min(matrix.shape[1]-1, j + q))
                    g += matrix[x, y] * ks[p + s, q + s]
            ret[i, j] = round(g) // c * c

@allow_mask
@quantize_handler
def _quantize_with_blur(matrix, c: int = 12, s: int = 3) -> np.ndarray:    # 1 <= c <= 255, 1<= s <= 100, larger s = more processing time
    """
    Image quantization using gaussian blur.\n
    This is experimental and may not quantise image's properly for large values of ``c``, hence it is recommended
    to keep ``c`` within the range [1, 255]. Larger values of ``s`` will *greatly* increase processing time, and it is
    recommended to keep ``s`` within the range [1, 100].
    Warning: This method may be **very slow** if the image is large and ``s``> 20
    
    :param matrix: Image matrix
    :param c: The greater the value of c, the more quantised the image
    :param s: Gaussian blur radius
    :return:
    """
    ret, kernel = np.zeros_like(matrix), np.zeros((2 * s + 1, 2 * s + 1), dtype=np.float32)
    c, s = max(1, min(c, 255)), max(1, min(s, 100))
    for p in range(-s, s + 1):
        for q in range(-s, s + 1):
            kernel[p + s, q + s] = (1. - min(s, int(sqrt(p ** 2 + q ** 2))) / s)
    kernel /= np.sum(kernel)
    if len(matrix.shape) == 2:
        _qblur_routine_2d(matrix, ret, kernel, c, s)
    else:
        _qblur_routine(matrix, ret, kernel, c, s)
    return ret

@njit(Tuple((int32[:, :], int32[:]))(float32[:, :], int32[:, :], int64, int64))
def _kmeans_clustering(points, centroids, iterations, width):
    """
    k-means clustering specifically for image matrices.
    
    :param points: Image matrix with shape (width x height, number of channels) where each 1D array corresponds to the
    values of the 2D channel matrix at that channel index
    :param centroids: List of initial (k) coordinate centers from the image matrix
    :param iterations: Number of times clustering is repeated. Generally achieves convergence within 10 loops
    :param width: Image width
    :return: list of k cluster centers and index-labeled cluster map for image matrix with shape (width x height,)
    """
    k = centroids.shape[0]
    gray = points.shape[1] == 1
    cluster_map = np.zeros((points.shape[0],), dtype=np.int32)
    histogram = [0 for _ in range(k)]
    distances = [0.0 for _ in range(k)]
    kmeans = [[0] * (1 if gray else 3) for _ in range(k)]
    min_dist, min_dist_index = float('inf'), 0
    for _ in range(iterations):
        for i in range(len(points)):
            for j in range(k):
                if not gray:
                    distances[j] = sqrt((points[i][0] - points[(centroids[j][0] + 1) * (centroids[j][1] + 1)][0]) ** 2 +
                                        (points[i][1] - points[(centroids[j][0] + 1) * (centroids[j][1] + 1)][1]) ** 2 +
                                        (points[i][2] - points[(centroids[j][0] + 1) * (centroids[j][1] + 1)][2]) ** 2)
                else:
                    distances[j] = abs(points[i][0] - points[(centroids[j][0] + 1) * (centroids[j][1] + 1)][0])
                if j == 0:
                    min_dist, min_dist_index = distances[0], 0
                if distances[j] < min_dist:
                    min_dist, min_dist_index = distances[j], j
            cluster_map[i] = min_dist_index
            histogram[min_dist_index] += 1
        for i in range(len(points)):
            cluster_index = cluster_map[i]
            kmeans[cluster_index][0] = (kmeans[cluster_index][0] + points[i][0])
            if not gray:
                kmeans[cluster_index][1] = (kmeans[cluster_index][1] + points[i][1])
                kmeans[cluster_index][2] = (kmeans[cluster_index][2] + points[i][2])
        for i in range(k):
            if histogram[i] == 0:
                continue
            kmeans[i][0] /= histogram[i]
            if not gray:
                kmeans[i][1] /= histogram[i]
                kmeans[i][2] /= histogram[i]
        for i in range(k):
            mean_rgb = kmeans[i]
            min_dist = 2 ** 20
            min_dist_index = -1
            for j in range(len(points)):
                if not gray:
                    dist = sqrt((points[j][0] - mean_rgb[0]) ** 2 +
                                (points[j][1] - mean_rgb[1]) ** 2 +
                                (points[j][2] - mean_rgb[2]) ** 2)
                else:
                    dist = abs(points[j][0] - mean_rgb[0])
                if dist < min_dist:
                    min_dist = dist
                    min_dist_index = j
            centroids[i] = [min_dist_index // width, min_dist_index % width]
        for i in range(k):
            histogram[i] = 0
            if not gray:
                kmeans[i][:] = [0, 0, 0]
            else:
                kmeans[i][:] = [0]
    return centroids, cluster_map

@allow_mask
@quantize_handler
def _quantize_with_kmeans_clustering(matrix: np.ndarray, k: int = 8, iterations: int = 3, initialise_method: int = 0, flipped_centroid_orient: bool = False) -> np.ndarray:
    """
    Image quantization via k-means clustering.\n
    Here, k represents the number of colors the image is to be quantized to.
    If iterations is specified, the algorithm will be repeated that many times instead of repeating till convergence,
    which may or may smaller than the provided value for `iterations`. Generally, the algorithm reaches convergence
    in less than ten iterations, but this can be reduced as mentioned, which will make the process much faster, at the
    cost of slightly poor results.
    
    :param matrix: Image matrix
    :param k: Number of colors to quantize image to [1-512]
    :param iterations: Number of times to perform clustering; if not specified will always be less than 10 [1-20] (Optional)
    :param initialise_method: Specifies the way to create the initial k-centroids [0-2] (Optional)
    :param flipped_centroid_orient: If true, centroids are created column-wise, else row-wise (Optional)
    :return: Quantized image matrix
    """
    def init_midpoint_centroids(data, k, orientation=0):
        ret = []
        for i, p in enumerate(np.array_split(data, k, axis=orientation)):
            gap = i * p.shape[0]
            ret.append((p.shape[:2][0] // 2 + gap, p.shape[:2][1] // 2))
        return ret
    
    def init_fixed_centroids(data, k):
        side_length = int(np.ceil(np.sqrt(k)))  # Ensure we have enough centroids
        centroids_per_dim = [side_length, (k + side_length - 1) // side_length]
        step_sizes = [data.shape[i] // centroids_per_dim[i] for i in range(2)]
        centroids = []
        for i in range(centroids_per_dim[0]):
            for j in range(centroids_per_dim[1]):
                centroid = [i * step_sizes[0], j * step_sizes[1]]
                centroids.append(centroid)
                if len(centroids) == k:
                    break
            if len(centroids) == k:
                break
        centroids = np.array(centroids)
        return centroids
    
    height, width = matrix.shape[:2]
    if len(matrix.shape) == 2:
        channels = 1
    else:
        channels = matrix.shape[2]
    k = max(1, min(k, 512)) if k is not None else 8
    iterations = max(1, min(iterations, 20)) if iterations is not None else 3
    if iterations > 1:
        if height * width > 22000000:
            iterations = 2 if iterations > 2 else iterations
            k = 12 if k > 12 else k
        elif height * width > 12000000:
            iterations = 3 if iterations > 3 else iterations
            k = 14 if k > 14 else k
        elif height * width >= 8000000:
            iterations = 5 if iterations > 5 else iterations
            k = 20 if k > 20 else k
        elif height * width > 2000000:
            iterations = 10 if iterations > 10 else iterations
            k = 40 if k > 40 else k
        elif height * width > 750000 and iterations > 16:
            iterations = 16
            k = 60 if k > 60 else k
        elif k > 50:
            iterations = 1
    else:
        if height * width > 22000000 and k > 64:
            k = 64
        elif height * width > 12000000 and k > 128:
            k = 128
        elif height * width > 8000000 and k > 192:
            k = 192
        elif height * width >= 4000000 and k > 256:
            k = 256
        elif height * width >= 2000000 and k > 512:
            k = 512
    if initialise_method == 1:
        centroids = init_midpoint_centroids(matrix, k, 1 if flipped_centroid_orient else 0)
    elif initialise_method == 2:
        centroids = init_fixed_centroids(matrix, k)
    else:
        centroids = [[randint(0, height - 1), randint(0, width - 1)] for _ in range(k)]
    centroids, cluster_map = _kmeans_clustering(matrix.reshape((height * width, channels)),
                                                np.array(centroids, dtype=np.int32), iterations, width)
    cluster_map = cluster_map.reshape((height, width))
    centroid_values = np.array([matrix[centroids[i, 0], centroids[i, 1]] for i in range(k)])
    segmented_image = centroid_values[cluster_map]
    return segmented_image
