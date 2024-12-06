from PIL import Image
import numpy as np
from math import floor
from numba import njit, float32, float64, prange

from filterkit.tools.common import preserve_transparency

def _load_cube_lut(file_path: str):
	with open(file_path, 'r') as f:
		lines = f.readlines()
	lut_size = None
	lut_data = []
	for line in lines:
		if line.startswith('LUT_3D_SIZE'):
			lut_size = int(line.split()[1])
		elif line.startswith('#') or line[0].isalpha():
			continue
		elif not line.strip():
			continue
		else:
			try:
				values = [float(x) for x in line.strip().split()]
				if len(values) == 3:  # Ensure this is an RGB triplet
					lut_data.append(values)
			except ValueError:
				continue
	return np.array(lut_data, dtype=np.float32).reshape((lut_size, lut_size, lut_size, 3))

@njit
def _trilinear_interpolate_pixel_with_lut(c, lut: np.ndarray):
	"""
	Perform trilinear interpolation to find the interpolated color value from the 3D LUT given a pixel value.
	:param c: RGB pixel
	:param lut: Lookup table of shape NxNxNx3 (ndarray)
	:return:
	"""
	# Get the LUT size
	lut_size = lut.shape[0]
	# Normalize the input color to [0, lut_size-1]
	r, g, b = c[2], c[1], c[0]
	r = r * (lut_size - 1)
	g = g * (lut_size - 1)
	b = b * (lut_size - 1)
	# Find the integer part (lower bound indices)
	r0, g0, b0 = floor(r), floor(g), floor(b)
	r1, g1, b1 = min(r0 + 1, lut_size - 1), min(g0 + 1, lut_size - 1), min(b0 + 1, lut_size - 1)
	# Calculate the fractional distance between the input and the nearest neighbors
	fr, fg, fb = r - r0, g - g0, b - b0
	# Trilinear interpolation
	# Get cube points
	c000_r, c000_g, c000_b = lut[r0, g0, b0, 0], lut[r0, g0, b0, 1], lut[r0, g0, b0, 2]
	c100_r, c100_g, c100_b = lut[r1, g0, b0, 0], lut[r1, g0, b0, 1], lut[r1, g0, b0, 2]
	c010_r, c010_g, c010_b = lut[r0, g1, b0, 0], lut[r0, g1, b0, 1], lut[r0, g1, b0, 2]
	c110_r, c110_g, c110_b = lut[r1, g1, b0, 0], lut[r1, g1, b0, 1], lut[r1, g1, b0, 2]
	c001_r, c001_g, c001_b = lut[r0, g0, b1, 0], lut[r0, g0, b1, 1], lut[r0, g0, b1, 2]
	c101_r, c101_g, c101_b = lut[r1, g0, b1, 0], lut[r1, g0, b1, 1], lut[r1, g0, b1, 2]
	c011_r, c011_g, c011_b = lut[r0, g1, b1, 0], lut[r0, g1, b1, 1], lut[r0, g1, b1, 2]
	c111_r, c111_g, c111_b = lut[r1, g1, b1, 0], lut[r1, g1, b1, 1], lut[r1, g1, b1, 2]
	# Interpolate along the R axis
	c00_r, c00_g, c00_b = (1 - fr) * c000_r + fr * c100_r, (1 - fr) * c000_g + fr * c100_g, (1 - fr) * c000_b + fr * c100_b
	c01_r, c01_g, c01_b = (1 - fr) * c001_r + fr * c101_r, (1 - fr) * c001_g + fr * c101_g, (1 - fr) * c001_b + fr * c101_b
	c10_r, c10_g, c10_b = (1 - fr) * c010_r + fr * c110_r, (1 - fr) * c010_g + fr * c110_g, (1 - fr) * c010_b + fr * c110_b
	c11_r, c11_g, c11_b = (1 - fr) * c011_r + fr * c111_r, (1 - fr) * c011_g + fr * c111_g, (1 - fr) * c011_b + fr * c111_b
	# Interpolate along the G axis
	c0_r, c0_g, c0_b = (1 - fg) * c00_r + fg * c10_r, (1 - fg) * c00_g + fg * c10_g, (1 - fg) * c00_b + fg * c10_b
	c1_r, c1_g, c1_b = (1 - fg) * c01_r + fg * c11_r, (1 - fg) * c01_g + fg * c11_g, (1 - fg) * c01_b + fg * c11_b
	# Interpolate along the B axis
	interpolated_color = (1 - fb) * c0_r + fb * c1_r, (1 - fb) * c0_g + fb * c1_g, (1 - fb) * c0_b + fb * c1_b
	return interpolated_color

@njit(float32[:, :, :](float32[:, :, :], float32[:, :, :, :], float64), parallel=True)
def _interpolate_with_lut(matrix: np.ndarray, lut: np.ndarray, strength: float):
	x, y, _ = matrix.shape
	matrix_norm = np.divide(matrix, 255)  # Normalize matrix
	interpolated = np.zeros_like(matrix)
	for i in prange(x):
		for j in range(y):
			lut_result = _trilinear_interpolate_pixel_with_lut(matrix_norm[i, j], lut)
			# Interpolate between the original matrix value and the LUT result based on strength
			interpolated[i, j, 0] = matrix[i, j, 0] + (lut_result[0] * 255 - matrix[i, j, 0]) * strength
			interpolated[i, j, 1] = matrix[i, j, 1] + (lut_result[1] * 255 - matrix[i, j, 1]) * strength
			interpolated[i, j, 2] = matrix[i, j, 2] + (lut_result[2] * 255 - matrix[i, j, 2]) * strength
	return interpolated

@preserve_transparency
def apply_lut(image: Image.Image, cube_file: str, strength: float = 1.0):
	"""
	Applies a lookup table mapping (LUT) from a .cube file to an image.\n
	The ``strength`` of the applied LUT must be within 0.0 and 1.0.
	
	:param image: PIL Image
	:param cube_file: .cube file path
	:param strength: LUT factor [0.0 - 1.0]
	:return: Filtered image
	"""
	if image.mode == 'L':
		image = image.convert('RGB')
	lut = _load_cube_lut(cube_file)
	strength = max(0.0, min(1.0, strength)) if strength is not None else 1.0
	matrix = np.array(image).astype(np.float32)
	interpolated = _interpolate_with_lut(matrix, lut, strength)
	return Image.fromarray(interpolated.astype(np.uint8))
