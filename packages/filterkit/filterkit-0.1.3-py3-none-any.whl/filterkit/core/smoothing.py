import numpy as np
from PIL import Image
from numba import njit, int16, int64, prange

from filterkit.tools.common import access_element_safe, channel_handler, preserve_transparency, allow_mask

@allow_mask
def sliding_histogram_filter(matrix: np.ndarray, window_size: int, method: int, **kwargs):
	axes = len(matrix.shape)
	if axes == 3:
		return _sliding_histogram_operation_3d(matrix, window_size, method)
	elif axes == 2:
		return _sliding_histogram_operation_2d(matrix, window_size, method)

@allow_mask
def median_filter_constant_time(matrix: np.ndarray, window_size: int, **kwargs):
	axes = len(matrix.shape)
	if axes == 3:
		return _median_filter_const(matrix, window_size)
	elif axes == 2:
		return _median_filter_const_2d(matrix, window_size)

@channel_handler
@preserve_transparency
def apply_smoothing(image: Image.Image, style: int = 0, window_size: int = 7, **kwargs) -> Image.Image:
	"""
	Apply smoothing/rank-based filters to an image with the method specified by ``style``.\n
	This method primarily is used to apply smoothing filters like the Median filter (style:0), Mode filter (style:1),
	Max filter (style:2) or Min filter (style:3), but supports other rank/histogram based filters as well.\n
	The strength of the applied filter can be adjusted by specifying a kernel size. Currently, kernel sizes (k) upto
	k=99 can be processed efficiently; if k>99, there will be noticeable processing delay. The median filter can be
	applied for all k>1.\n
	Note: Transparent images will not have their alpha channels modified.

	:param image: PIL Image
	:param style: Smoothing style [0-5]
	:param window_size: Kernel radius (k) for smoothing filter [1-150]
	:return: Smoothed image
	"""
	# TODO: rank filter
	image_np = np.array(image).astype(np.int16)
	window_size = max(2, min(150, 2 * window_size + 1)) if window_size is not None else 7
	style = style if style is not None else 0
	if style == 0 and window_size > 99:
		smoothed = median_filter_constant_time(image_np, window_size, **kwargs)
	else:
		smoothed = sliding_histogram_filter(image_np, window_size, style, **kwargs)
	smoothed_image = Image.fromarray(smoothed.astype(np.uint8))
	return smoothed_image

@njit(int16[:, :](int16[:, :], int64))
def _median_filter_const_2d(matrix, window_size):              # constant time median filter for k > 99
	rows, cols = matrix.shape
	dst = np.zeros((rows, cols), dtype=np.int16)
	histograms = np.zeros((cols, 256), dtype=int16)
	crt_histogram = np.zeros(256, dtype=np.int16)
	offset = int(window_size // 2)
	threshold = window_size * window_size // 2
	for j in range(cols):
		for i in range(-offset, offset):
			histograms[j, access_element_safe(matrix, i, j)] += 1
	for i in range(rows):
		for j in range(cols):
			histograms[j, access_element_safe(matrix, i + offset, j)] += 1
		for j in range(-offset, offset):
			for k in range(256):
				crt_histogram[k] += histograms[max(0, j), k]
		for j in range(cols):
			for k in range(256):
				crt_histogram[k] += histograms[min(cols - 1, j + offset), k]
			cnt, k = 0, 0
			while cnt < threshold and k < 256:
				cnt += crt_histogram[k]
				k += 1
			dst[i, j] = k
			for k in range(256):
				crt_histogram[k] -= histograms[max(0, j - offset), k]
		for j in range(cols):
			histograms[j, access_element_safe(matrix, i - offset, j)] -= 1
		crt_histogram[:] = 0
	return dst

def _median_filter_const(matrix, window_size):
	smoothed = np.zeros_like(matrix)
	smoothed[:, :, 0] = _median_filter_const_2d(matrix[:, :, 0], window_size)
	smoothed[:, :, 1] = _median_filter_const_2d(matrix[:, :, 1], window_size)
	smoothed[:, :, 2] = _median_filter_const_2d(matrix[:, :, 2], window_size)
	return smoothed

@njit(int16[:, :](int16[:, :], int64, int64), parallel=True)
def _sliding_histogram_operation_2d(matrix, window_size, method):      # method=0: median, method=1: mode, method2: max, method=3: min
	# TODO: bilateral mean filter (sliding histogram based)
	rows, cols = matrix.shape
	offset = int(window_size // 2)
	output = np.zeros((rows, cols), dtype=np.int16)
	histogram = [[0] * 256 for _ in range(rows)]
	for i in prange(rows):
		for j in range(cols):
			start_row = max(0, i - offset)
			end_row = min(rows, i + offset + 1)
			start_col = max(0, j - offset)
			end_col = min(cols, j + offset + 1)
			window = matrix[start_row:end_row, start_col:end_col]
			if j == 0:
				for row in window:
					for num in row:
						histogram[i][num] += 1
			elif j < cols//2 and end_col-start_col < window_size:
				right = window[:, -1]
				for num in right:
					histogram[i][num] += 1
			elif j > cols//2 and end_col-start_col < window_size:
				left = window[:, 0]
				for num in left:
					histogram[i][num] -= 1
			else:
				left = window[:, 0]
				right = window[:, -1]
				for num in left:
					histogram[i][num] -= 1
				for num in right:
					histogram[i][num] += 1
			if method == 1:                     # local mode
				output[i, j] = histogram[i].index(max(histogram[i]))
			elif method == 2:
				k = -1                          # local maximum
				while histogram[i][k] == 0:
					k -= 1
				output[i, j] = 256 + k
			elif method == 3:                   # local minimum
				k = 0
				while histogram[i][k] == 0:
					k += 1
				output[i, j] = k
			elif method == 4:                   # local gradient
				kmin, kmax = 0, -1
				while histogram[i][kmin] == 0:
					kmin += 1
				while histogram[i][kmax] == 0:
					kmax -= 1
				output[i, j] = kmax - kmin
			elif method == 5:                   # local entropy
				k = 0
				summed = sum(histogram[i])
				for count in histogram[i]:
					if count > 0:
						p = count / summed
						k += p * np.log2(p)
				output[i, j] = -k * 60
			else:
				k, tot = 0, 0                         # local median; use for k < 99
				summed = sum(histogram[i])
				threshold = summed//2 if summed % 2 == 0 else (summed+1)//2
				while tot < threshold:
					tot += histogram[i][k]
					k += 1
				output[i, j] = k
	return output

def _sliding_histogram_operation_3d(matrix, window_size, method):
	smoothed = np.zeros_like(matrix)
	smoothed[:, :, 0] = _sliding_histogram_operation_2d(matrix[:, :, 0], window_size, method)
	smoothed[:, :, 1] = _sliding_histogram_operation_2d(matrix[:, :, 1], window_size, method)
	smoothed[:, :, 2] = _sliding_histogram_operation_2d(matrix[:, :, 2], window_size, method)
	return smoothed
