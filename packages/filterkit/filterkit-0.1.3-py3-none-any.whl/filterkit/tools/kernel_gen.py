import numpy as _np

def get_footprint(size: int, shape: int = 0, rgb: bool = False):     # binary kernel generator of given shape
    """
    Creates a binary kernel-sized mask specifying the corresponding value to include (1) or not to include (0) in the
    mask's neighborhood, when applied to a matrix.\n
    
    :param size: Mask radius
    :param shape: Geometric shape of the mask
    :param rgb: If true, returns a 3-dimensional version of the mask
    :return: Binary mask
    """
    size = int(size) if size is not None else 3
    if shape == 0:
        fp = square(size)
    elif shape == 1:
        fp = circle(size)
    elif shape == 2:
        fp = diamond(size)
    else:
        fp = octagon(size, size-1)
    return fp if not rgb else _np.stack((fp, fp, fp))

def circle(radius=3):
    l = _np.arange(-radius, radius + 1)
    x, y = _np.meshgrid(l, l)
    radius += 0.5
    return _np.array((x**2 + y**2) <= radius**2, dtype=int)

def square(width=3):
    width = 2*width+1
    return _np.ones((width, width), dtype=int)

def diamond(radius=3):
    l = _np.arange(0, radius * 2 + 1)
    i, j = _np.meshgrid(l, l)
    return _np.array(_np.abs(i - radius) + _np.abs(j - radius) <= radius, dtype=int)

def octagon(m=4, n=None):
    # TODO: needs work, only makes borders
    if not n:
        n = m-1
    footprint = _np.zeros((m + 2 * n, m + 2 * n))
    footprint[0, n] = 1
    footprint[n, 0] = 1
    footprint[0, m + n - 1] = 1
    footprint[m + n - 1, 0] = 1
    footprint[-1, n] = 1
    footprint[n, -1] = 1
    footprint[-1, m + n - 1] = 1
    footprint[m + n - 1, -1] = 1
    return footprint

def box_blur_kernel(radius) -> _np.ndarray:
    """
    Creates a square, separable kernel of given radius which when convolved produces a box blur effect.\n
    
    :param radius:
    :return: Box blur (mean) kernel
    """
    size = 2 * radius + 1
    weight = 1 / (size * size)
    kernel = _np.full((size, size), weight)
    return kernel

def gaussian_kernel(radius) -> _np.ndarray:
    """
    Creates a square, separable kernel of given radius which when convolved produces a gaussian blur effect.\n
    
    :param radius: Kernel radius
    :return: Gaussian kernel
    """
    sigma = radius / 2
    size = int(2 * _np.ceil(2 * sigma) + 1)
    x = _np.arange(-size // 2 + 1, size // 2 + 1)
    y = _np.arange(-size // 2 + 1, size // 2 + 1)
    x, y = _np.meshgrid(x, y)
    kernel = _np.exp(-(x ** 2 + y ** 2) / (2 * sigma ** 2))
    kernel /= 2 * _np.pi * sigma ** 2
    kernel /= kernel.sum()
    return kernel

def gaussian_kernel_1d(sigma, order=0):
    """
    Creates a 1d gaussian kernel/vector.\n
    Reference: https://github.com/scipy/scipy/blob/v1.14.1/scipy/ndimage/_filters.py#L186
    
    :param sigma: Standard deviation of kernel; this is directly proportional to the kernel radius
    :param order: If 0, returns a normal gaussian kernel, if 1, returns the derivative of the gaussian kernel
    :return: 1-dimensional gaussian kernel (ndarray)
    """
    radius = int(4.0 * sigma + 0.5)
    exponent_range = _np.arange(order + 1)
    sigma2 = sigma * sigma
    x = _np.arange(-radius, radius + 1)
    phi_x = _np.exp(-0.5 / sigma2 * x ** 2)
    phi_x = phi_x / phi_x.sum()
    if order == 0:
        return phi_x.astype(_np.float32)
    else:
        q = _np.zeros(order + 1)
        q[0] = 1
        D = _np.diag(exponent_range[1:], 1)  # D @ q(x) = q'(x)
        P = _np.diag(_np.ones(order) / -sigma2, -1)  # P @ q(x) = q(x) * p'(x)
        Q_deriv = D + P
        for _ in range(order):
            q = Q_deriv.dot(q)
        q = (x[:, None] ** exponent_range).dot(q)
        return (q * phi_x).astype(_np.float32)

def triangle_blur_kernel(radius: int) -> _np.ndarray:
    """
    Creates a square, separable kernel of given radius which when convolved produces a triangle blur effect.\n
    
    :param radius: Kernel radius
    :return: Triangle blur kernel
    """
    size = 2 * radius + 1
    kernel = _np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            kernel[i, j] = (radius - abs(i - radius)) * (radius - abs(j - radius))
    kernel /= kernel.sum()
    return kernel

def motion_blur_kernel(radius: int, angle: int) -> _np.ndarray:
    """
    Creates a square kernel of given radius which when convolved produces a motion blur effect.\n
    The direction of the blur can be adjusted by setting the angle.
    
    :param radius: Kernel radius
    :param angle: Relative direction of motion blur [0-360]
    :return: Motion blur kernel
    """
    size = 2 * radius + 1
    kernel = _np.zeros((size, size), dtype=_np.float32)
    angle_rad = _np.deg2rad(angle)
    center = radius
    x1 = center + radius * _np.cos(angle_rad)
    y1 = center + radius * _np.sin(angle_rad)
    x2 = center - radius * _np.cos(angle_rad)
    y2 = center - radius * _np.sin(angle_rad)
    if abs(x2 - x1) > abs(y2 - y1):
        x = _np.arange(size)
        y = _np.round((y2 - y1) / (x2 - x1) * (x - x1) + y1).astype(int)
        valid_indices = (y >= 0) & (y < size)
        kernel[y[valid_indices], x[valid_indices]] = 1
    else:
        y = _np.arange(size)
        x = _np.round((x2 - x1) / (y2 - y1) * (y - y1) + x1).astype(int)
        valid_indices = (x >= 0) & (x < size)
        kernel[y[valid_indices], x[valid_indices]] = 1
    kernel /= kernel.sum()
    return kernel

def emboss_kernel(radius, angle) -> _np.ndarray:
    """
    Creates a square kernel of given radius which when convolved produces an emboss effect.\n
    The direction of the effect can be adjusted by setting the angle.
    
    :param radius: Kernel radius
    :param angle: Relative direction of embossing [0-360]
    :return: Emboss kernel
    """
    size = 2 * radius + 1
    kernel = _np.zeros((size, size), dtype=_np.float32)
    angle_rad = _np.deg2rad(angle)
    center = radius
    x1 = center + radius * _np.cos(angle_rad)
    y1 = center + radius * _np.sin(angle_rad)
    x2 = center - radius * _np.cos(angle_rad)
    y2 = center - radius * _np.sin(angle_rad)
    if abs(x2 - x1) > abs(y2 - y1):
        x = _np.arange(size)
        y = _np.round((y2 - y1) / (x2 - x1) * (x - x1) + y1).astype(int)
        valid_indices = (y >= 0) & (y < size)
        half_size = size // 2
        kernel[y[:half_size][valid_indices[:half_size]], x[:half_size][valid_indices[:half_size]]] = -1
        kernel[y[half_size:][valid_indices[half_size:]], x[half_size:][valid_indices[half_size:]]] = 1
    else:
        y = _np.arange(size)
        x = _np.round((x2 - x1) / (y2 - y1) * (y - y1) + x1).astype(int)
        valid_indices = (x >= 0) & (x < size)
        half_size = size // 2
        kernel[y[:half_size][valid_indices[:half_size]], x[:half_size][valid_indices[:half_size]]] = -1
        kernel[y[half_size:][valid_indices[half_size:]], x[half_size:][valid_indices[half_size:]]] = 1
    kernel[radius, radius] = 1
    return kernel
