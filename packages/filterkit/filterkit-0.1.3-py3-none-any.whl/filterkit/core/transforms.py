from PIL import Image
from math import cos, sin, ceil
from numba import njit, prange, float32, float64, int64
import numpy as np
from typing import Tuple, List

MAX_ALLOWED_WIDTH = 7680
MAX_ALLOWED_HEIGHT = 4320

def transform_handler(transform):
    """
    Wrapper to handle parameter management for image transformation functions.

    :param transform: Image transform function
    :return:
    """
    def wrapper(*args, **kwargs):
        image = args[0]
        image_np = np.array(image).astype(np.float32) if not isinstance(image, np.ndarray) else image
        image_np = image_np.astype(np.float32) if isinstance(image_np, np.ndarray) and image_np.dtype != np.float32 else image_np
        transformed = transform(image_np, *args[1:], **kwargs)
        return Image.fromarray(transformed.astype(np.uint8))
    return wrapper

@transform_handler
def rotate(matrix: np.ndarray, angle: int, center_x: int = None, center_y: int = None):
    """
    Rotate an image matrix by ``angle`` degrees at the coordinate (``center_x, center_y``), if specified.\n

    :param matrix: Image matrix
    :param angle: Rotation angle
    :param center_x: X coordinate (column index) of rotation center
    :param center_y: Y coordinate (row index) of rotation center
    :return: Rotated image
    """
    rgb = len(matrix.shape) == 3
    height, width = matrix.shape[:2]
    center_x = (width // 2 if center_x > width or center_x < 0 else center_x) if center_x is not None else width // 2
    center_y = (height // 2 if center_y > height or center_y < 0 else center_y) if center_y is not None else height // 2
    angle = max(0, min(360, angle)) if angle is not None else 90
    angle_rad = np.deg2rad(angle)
    args = (matrix, angle_rad, width, height, center_x, center_y)
    rotated = (_rotate2d, _rotate3d)[rgb](*args)
    return rotated

@njit(float32[:, :, :](float32[:, :, :], float64, int64, int64, int64, int64), parallel=True)
def _rotate3d(matrix, angle_rad, width, height, center_x, center_y):
    rotated = np.zeros_like(matrix)
    has_alpha = matrix.shape[2] == 4
    for y in prange(height):
        for x in range(width):
            new_x = center_x + (x - center_x) * cos(angle_rad) - (y - center_y) * sin(angle_rad)
            new_y = center_y + (x - center_x) * sin(angle_rad) + (y - center_y) * cos(angle_rad)
            if 0 <= new_x < width - 1 and 0 <= new_y < height - 1:
                x1, y1 = int(new_x), int(new_y)
                x2, y2 = x1 + 1, y1 + 1
                r1 = (x2 - new_x) * matrix[y1, x1, 0] + (new_x - x1) * matrix[y1, x2, 0]
                r2 = (x2 - new_x) * matrix[y2, x1, 0] + (new_x - x1) * matrix[y2, x2, 0]
                g1 = (x2 - new_x) * matrix[y1, x1, 1] + (new_x - x1) * matrix[y1, x2, 1]
                g2 = (x2 - new_x) * matrix[y2, x1, 1] + (new_x - x1) * matrix[y2, x2, 1]
                b1 = (x2 - new_x) * matrix[y1, x1, 2] + (new_x - x1) * matrix[y1, x2, 2]
                b2 = (x2 - new_x) * matrix[y2, x1, 2] + (new_x - x1) * matrix[y2, x2, 2]
                red_value = (y2 - new_y) * r1 + (new_y - y1) * r2
                green_value = (y2 - new_y) * g1 + (new_y - y1) * g2
                blue_value = (y2 - new_y) * b1 + (new_y - y1) * b2
                rotated[y, x, 0] = red_value
                rotated[y, x, 1] = green_value
                rotated[y, x, 2] = blue_value
                if has_alpha:
                    rotated[y, x, 3] = matrix[y, x, 3]
    return rotated

@njit(float32[:, :](float32[:, :], float64, int64, int64, int64, int64), parallel=True)
def _rotate2d(matrix, angle_rad, width, height, center_x, center_y):
    rotated = np.zeros_like(matrix)
    for y in prange(height):
        for x in range(width):
            new_x = center_x + (x - center_x) * cos(angle_rad) - (y - center_y) * sin(angle_rad)
            new_y = center_y + (x - center_x) * sin(angle_rad) + (y - center_y) * cos(angle_rad)
            if 0 <= new_x < width - 1 and 0 <= new_y < height - 1:
                x1, y1 = int(new_x), int(new_y)
                x2, y2 = x1 + 1, y1 + 1
                r1 = (x2 - new_x) * matrix[y1, x1] + (new_x - x1) * matrix[y1, x2]
                r2 = (x2 - new_x) * matrix[y2, x1] + (new_x - x1) * matrix[y2, x2]
                pixel_value = (y2 - new_y) * r1 + (new_y - y1) * r2
                rotated[y, x] = pixel_value
    return rotated

@transform_handler
def resize(matrix: np.ndarray, scale_x: float = 1.0, scale_y: float = 1.0, size: Tuple[int, int] = (None, None)):
    """
    Resize an image matrix to the given scaling factors, or to the ``size`` if specified.\n
    If both width and height are given in ``size``, any provided scaling factors will be ignored. If
    ``scale_x`` == ``scale_y`` or ``size[0]`` == ``size[1]``, it is equivalent to scaling the image by either scaling
    factor.\n
    
    :param matrix: Image matrix
    :param scale_x: Horizontal scaling factor
    :param scale_y: Vertical scaling factor
    :param size: Tuple of new width, and new height (Optional)
    :return: Resized image
    """
    # TODO: fix interpolation when down sampling
    rgb = len(matrix.shape) == 3
    height, width = matrix.shape[:2]
    scale_x = max(0.0, min(20.0, scale_x)) if scale_x is not None else 1.0
    scale_y = max(0.0, min(20.0, scale_y)) if scale_y is not None else 1.0
    if len(size) == 2:
        if size[0] is None and size[1] is not None:
            new_height, new_width = size[1], width * scale_x
        elif size[1] is None and size[0] is not None:
            new_height, new_width = height * scale_y, size[0]
        elif size[0] is None and size[1] is None:
            new_height, new_width = height * scale_y, width * scale_x
        else:
            new_height, new_width = size[1], size[0]
    else:
        new_height, new_width = height * scale_y, width * scale_x
    new_height, new_width = abs(int(new_height)), abs(int(new_width))
    new_width, new_height = max(0, min(MAX_ALLOWED_WIDTH, new_width)), max(0, min(MAX_ALLOWED_HEIGHT, new_width))
    if new_width == width and new_height == height:
        return matrix
    args = (width, height, new_width, new_height)
    scaled = (_resize2d, _resize3d)[rgb](matrix, *args)
    return scaled

@njit(float32[:, :](float32[:, :], int64, int64, int64, int64), parallel=True)
def _resize2d(matrix, width, height, new_width, new_height):
    output = np.zeros((new_height, new_width), dtype=matrix.dtype)
    scale_x, scale_y = new_width / width, new_height / height
    for j in prange(new_height):
        for i in range(new_width):
            x, y = i / scale_x, j / scale_y
            x1, y1 = int(x), int(y)
            x2, y2 = min(x1 + 1, width - 1), min(y1 + 1, height - 1)
            a, b = x - x1, y - y1
            r1 = (1 - a) * matrix[y1, x1] + a * matrix[y1, x2]
            r2 = (1 - a) * matrix[y2, x1] + a * matrix[y2, x2]
            interpolated = (1 - b) * r1 + b * r2
            output[j, i] = interpolated
    return output

@njit(float32[:, :, :](float32[:, :, :], int64, int64, int64, int64), parallel=True)
def _resize3d(matrix, width, height, new_width, new_height):
    output = np.zeros((new_height, new_width, matrix.shape[2]), dtype=matrix.dtype)
    scale_x, scale_y = new_width / width, new_height / height
    has_alpha = matrix.shape[2] == 4
    for j in prange(new_height):
        for i in range(new_width):
            x, y = i / scale_x, j / scale_y
            x1, y1 = int(x), int(y)
            x2, y2 = min(x1 + 1, width - 1), min(y1 + 1, height - 1)
            a, b = x - x1, y - y1
            r1 = (1 - a) * matrix[y1, x1, 0] + a * matrix[y1, x2, 0]
            r2 = (1 - a) * matrix[y2, x1, 0] + a * matrix[y2, x2, 0]
            g1 = (1 - a) * matrix[y1, x1, 1] + a * matrix[y1, x2, 1]
            g2 = (1 - a) * matrix[y2, x1, 1] + a * matrix[y2, x2, 1]
            b1 = (1 - a) * matrix[y1, x1, 2] + a * matrix[y1, x2, 2]
            b2 = (1 - a) * matrix[y2, x1, 2] + a * matrix[y2, x2, 2]
            if has_alpha:
                a1 = (1 - a) * matrix[y1, x1, 3] + a * matrix[y1, x2, 3]
                a2 = (1 - a) * matrix[y2, x1, 3] + a * matrix[y2, x2, 3]
                alpha = (1 - b) * a1 + b * a2
            red = (1 - b) * r1 + b * r2
            green = (1 - b) * g1 + b * g2
            blue = (1 - b) * b1 + b * b2
            output[j, i, 0] = red
            output[j, i, 1] = green
            output[j, i, 2] = blue
            if has_alpha:
                output[j, i, 3] = alpha
    return output

@transform_handler
def shear(matrix: np.ndarray, shear_factor_x: float | int = 0.0, shear_factor_y: float | int = 0.0,
          stretch_x: float | int = 1, stretch_y: float | int = 1):
    """
    Apply affine/shear transformations to image matrix.\n
    ``shear_factor_x`` and ``shear_factor_y`` affect horizontal and vertical shearing, respectively.\n
    Optionally, if specified,``stretch_x`` and ``stretch_y`` affect stretching/squeezing the matrix horizontally or
    vertically.\n
    
    :param matrix: Image matrix
    :param shear_factor_x: Horizontal shear factor
    :param shear_factor_y: Vertical shear factor
    :param stretch_x: Horizontal stretch factor
    :param stretch_y: Vertical stretch factor
    :return: Sheared image
    """
    height, width = matrix.shape[:2]
    shear_factor_x = max(-4.0, min(4.0, shear_factor_x)) if shear_factor_x is not None else 0.0
    shear_factor_y = max(-4.0, min(4.0, shear_factor_y)) if shear_factor_y is not None else 0.0
    stretch_x = max(0.01, min(10.0, stretch_x)) if stretch_x is not None else 1.0
    stretch_y = max(0.01, min(10.0, stretch_y)) if stretch_y is not None else 1.0
    if shear_factor_x == shear_factor_y == 0.0 and stretch_x == stretch_y == 1.0:
        return matrix
    shear_matrix = np.array([[shear_factor_x, stretch_x], [stretch_y, shear_factor_y]], dtype=np.float32)
    top_left_x, top_left_y = shear_matrix[0, 0] * 0 + shear_matrix[0, 1] * 0, \
                             shear_matrix[1, 0] * 0 + shear_matrix[1, 1] * 0
    top_right_x, top_right_y = shear_matrix[0, 0] * 0 + shear_matrix[0, 1] * matrix.shape[1], \
                               shear_matrix[1, 0] * 0 + shear_matrix[1, 1] * matrix.shape[1]
    bottom_left_x, bottom_left_y = shear_matrix[0, 0] * matrix.shape[0] + shear_matrix[0, 1] * 0, \
                                   shear_matrix[1, 0] * matrix.shape[0] + shear_matrix[1, 1] * 0
    bottom_right_x, bottom_right_y = shear_matrix[0, 0] * matrix.shape[0] + shear_matrix[0, 1] * matrix.shape[1], \
                                     shear_matrix[1, 0] * matrix.shape[0] + shear_matrix[1, 1] * matrix.shape[1]
    corners = [(top_left_x, top_left_y), (top_right_x, top_right_y),
               (bottom_left_x, bottom_left_y), (bottom_right_x, bottom_right_y)]
    x_coords, y_coords = [corner[0] for corner in corners], [corner[1] for corner in corners]
    new_width, new_height = ceil(max(x_coords) - min(x_coords)), ceil(max(y_coords) - min(y_coords))
    new_width, new_height = max(0, min(MAX_ALLOWED_WIDTH, new_width)), max(0, min(MAX_ALLOWED_HEIGHT, new_height))
    offset_x, offset_y = int(abs(min(x_coords))), int(abs(min(y_coords)))
    sheared = (_shear2d, _shear3d)[len(matrix.shape) == 3](matrix, shear_matrix, width, height, new_width, new_height, offset_x, offset_y)
    return sheared

@njit(float32[:, :](float32[:, :], float32[:, :], int64, int64, int64, int64, int64, int64))
def _shear2d(matrix, shear_matrix, width, height, new_width, new_height, offset_x, offset_y):
    sheared = np.zeros((new_height, new_width), dtype=matrix.dtype)
    offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for y in range(height):
        for x in range(width):
            new_x, new_y = shear_matrix[0, 0] * y + shear_matrix[0, 1] * x, shear_matrix[1, 0] * y + shear_matrix[1, 1] * x
            new_x, new_y = int(new_x + offset_x), int(new_y + offset_y)
            if 0 < new_x < new_width - 1 and 0 < new_y < new_height - 1:
                sheared[new_y, new_x] = matrix[y, x]
                for i in range(8):
                    if sheared[new_y + offsets[i][0], new_x + offsets[i][1]] == 0:
                        sheared[new_y + offsets[i][0], new_x + offsets[i][1]] = sheared[new_y, new_x]
    return sheared

@njit(float32[:, :, :](float32[:, :, :], float32[:, :], int64, int64, int64, int64, int64, int64))
def _shear3d(matrix, shear_matrix, width, height, new_width, new_height, offset_x, offset_y):
    sheared = np.zeros((new_height, new_width, matrix.shape[2]), dtype=matrix.dtype)
    offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    has_alpha = matrix.shape[2] == 4
    for y in range(height):
        for x in range(width):
            new_x, new_y = shear_matrix[0, 0] * y + shear_matrix[0, 1] * x, shear_matrix[1, 0] * y + shear_matrix[1, 1] * x
            new_x, new_y = int(new_x + offset_x), int(new_y + offset_y)
            if 0 < new_x < new_width - 1 and 0 < new_y < new_height - 1:
                sheared[new_y, new_x, 0] = matrix[y, x, 0]
                sheared[new_y, new_x, 1] = matrix[y, x, 1]
                sheared[new_y, new_x, 2] = matrix[y, x, 2]
                if has_alpha:
                    sheared[new_y, new_x, 3] = matrix[y, x, 3]
                for i in range(8):
                    if sheared[new_y + offsets[i][0], new_x + offsets[i][1], 0] == 0:
                        sheared[new_y + offsets[i][0], new_x + offsets[i][1], 0] = sheared[new_y, new_x, 0]
                        sheared[new_y + offsets[i][0], new_x + offsets[i][1], 1] = sheared[new_y, new_x, 1]
                        sheared[new_y + offsets[i][0], new_x + offsets[i][1], 2] = sheared[new_y, new_x, 2]
                        if has_alpha:
                            sheared[new_y + offsets[i][0], new_x + offsets[i][1], 3] = sheared[new_y, new_x, 3]
    return sheared

@transform_handler
def flip(matrix: np.ndarray, vertical: bool = False):
    """
    Flip and image matrix vertically or horizontally.\n
    
    :param matrix: Image matrix
    :param vertical: If true, flip vertically
    :return: Flipped image
    """
    if vertical:
        return np.flip(matrix, axis=1)
    else:
        return np.flip(matrix, axis=0)

@transform_handler
def perspective_transform(matrix: np.ndarray, src_points: Tuple[Tuple[int, int]] | List[List[int]] | List[Tuple[int, int]],
                          scaling: float = 1.0, width_const: int = 0, height_const: int = 0):
    """
    Applies perspective warp/transform on a section of an image given by four source points, with the result mapped to a
    rectangular matrix of given scaling.\n
    
    :param matrix: Image matrix
    :param src_points: Coordinates of the four corners of a quadrilateral bounding a region within the matrix;
            (points format: [top left, bottom left, top right, bottom right], coordinate format: (width index, height index))
    :param scaling: Scale factor to apply to mapped output (Optional)
    :param width_const: Constant value by which output width may be increased/decreased (Optional)
    :param height_const: Constant value by which output height may be increased/decreased (Optional)
    :return: Transformed image
    """
    # solves homogenous system of equations for the transformation
    def get_transform_matrix(src, dst):  # coords order: [top left, bottom left, top right, bottom right]
        A = []
        for i in range(4):
            x_src, y_src = src[i]
            x_dst, y_dst = dst[i]
            A.extend([
                [x_src, y_src, 1, 0, 0, 0, -x_dst * x_src, -x_dst * y_src],
                [0, 0, 0, x_src, y_src, 1, -y_dst * x_src, -y_dst * y_src]
            ])
        A = np.array(A)
        B = dst.flatten()
        h = np.linalg.solve(A, B)
        h = np.append(h, 1)
        H = h.reshape(3, 3)
        return H
    
    def get_dimensions(points):
        x_coords = [point[0] for point in points]
        y_coords = [point[1] for point in points]
        width = int(max(x_coords) - min(x_coords))
        height = int(max(y_coords) - min(y_coords))
        return width, height
    
    def adjust_dimensions(width, height, max_width, max_height):
        height_factor = max_height / height
        width_factor = max_width / width
        scaling_factor = min(height_factor, width_factor)
        new_height = int(height * scaling_factor)
        new_width = int(width * scaling_factor)
        return new_width, new_height
    
    rgb = len(matrix.shape) == 3
    src_points = [(max(0, min(x, matrix.shape[1])), max(0, min(y, matrix.shape[0]))) for x, y in src_points]
    scaling = max(0.1, min(20.0, scaling)) if scaling is not None else 1.0
    src_w, src_h = get_dimensions(src_points)
    src_w, src_h = max(20, min(MAX_ALLOWED_WIDTH, src_w + width_const)), max(20, min(MAX_ALLOWED_HEIGHT, src_h + height_const))
    if src_w * scaling > MAX_ALLOWED_WIDTH or src_h * scaling > MAX_ALLOWED_HEIGHT:
        src_w, src_h = adjust_dimensions(src_w, src_h, MAX_ALLOWED_WIDTH, MAX_ALLOWED_HEIGHT)  # adjust to screen size later
    else:
        src_w, src_h = src_w * scaling, src_h * scaling
    dst_points = [[0, 0], [0, src_h], [src_w, 0], [src_w, src_h]]
    output_w, output_h = get_dimensions(dst_points)
    trans_matrix = get_transform_matrix(np.array(src_points), np.array(dst_points))
    if rgb:
        output = np.zeros((output_h, output_w, 3), dtype=matrix.dtype)
    else:
        output = np.zeros((output_h, output_w), dtype=matrix.dtype)
    y, x = np.indices((output_h, output_w))
    homogeneous_coords = np.stack([x.ravel(), y.ravel(), np.ones_like(x).ravel()])
    
    # Apply the inverse transformation matrix to get source coordinates
    inv_matrix = np.linalg.inv(trans_matrix)
    transformed_coords = inv_matrix @ homogeneous_coords
    transformed_coords /= transformed_coords[2]     # TODO: fix occasional divide by zero
    x_transformed = transformed_coords[0].reshape(output_h, output_w)
    y_transformed = transformed_coords[1].reshape(output_h, output_w)
    
    # Mapping transformed coordinates to output array
    x_src = np.round(np.nan_to_num(x_transformed, nan=0, posinf=0, neginf=0)).astype(int)
    y_src = np.round(np.nan_to_num(y_transformed, nan=0, posinf=0, neginf=0)).astype(int)
    mask = (x_src >= 0) & (x_src < matrix.shape[1]) & (y_src >= 0) & (y_src < matrix.shape[0])
    x_src_valid = x_src[mask]
    y_src_valid = y_src[mask]
    output_coords = np.nonzero(mask)
    output_i = output_coords[0]
    output_j = output_coords[1]
    if rgb:
        output[output_i, output_j, 0] = matrix[y_src_valid, x_src_valid, 0]
        output[output_i, output_j, 1] = matrix[y_src_valid, x_src_valid, 1]
        output[output_i, output_j, 2] = matrix[y_src_valid, x_src_valid, 2]
    else:
        output[output_i, output_j] = matrix[y_src_valid, x_src_valid]
    return output
