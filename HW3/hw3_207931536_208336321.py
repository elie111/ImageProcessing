import numpy as np
import cv2
import random
import matplotlib.pyplot as plt
import scipy.ndimage
from scipy.signal import convolve2d


def add_SP_noise(im, p):
    sp_noise_im = im.copy()
    noised_pixels_num = p * (sp_noise_im.shape[0] * sp_noise_im.shape[1])
    noised_pixels_pos = random.sample(range(im.shape[0] * im.shape[1]), int(noised_pixels_num))
    sp_noise_im = np.ravel(sp_noise_im)
    sp_noise_im[noised_pixels_pos[0: int(noised_pixels_num) // 2]] = 0
    sp_noise_im[noised_pixels_pos[int(noised_pixels_num) // 2:]] = 255
    sp_noise_im = np.reshape(sp_noise_im, (im.shape[0], im.shape[1]))
    return sp_noise_im


def clean_SP_noise_single(im, radius):
    clean_im = im.copy()

    for i in range(radius, im.shape[0] - radius):
        for j in range(radius, im.shape[1] - radius):
            clean_im[i][j] = np.median(im[i - radius: i + radius + 1, j - radius: j + radius + 1])

    # return value
    return clean_im


def clean_SP_noise_multiple(images):
    # TODO: add implementation
    clean_image = np.median(images, axis=0)
    return clean_image


def add_Gaussian_Noise(im, s):
    gaussian_noise_im = im.copy()
    # TODO: add implementation

    # Generate the noise
    noise = np.random.normal(0, s, im.shape)

    # Add the noise to the image
    gaussian_noise_im = gaussian_noise_im + noise.astype(float)
    gaussian_noise_im = np.clip(gaussian_noise_im, 0, 255)
    return gaussian_noise_im.astype(np.uint8)


def clean_Gaussian_noise(im, radius, maskSTD):
    # TODO: add implementation
    # Create a 2D Gaussian kernel with the given std and radius
    cleaned_im = im.copy()
    X, Y = np.meshgrid(np.arange(-radius, radius + 1), np.arange(-radius, radius + 1))
    kernel = np.exp(-(X ** 2 + Y ** 2) / (2 * (maskSTD ** 2)))
    kernel /= np.sum(kernel)
    # Convolve the image with the kernel using scipy.signal.convolve2d
    cleaned_im = convolve2d(cleaned_im.astype(np.float), kernel, mode='same')

    return cleaned_im.astype(np.uint8)


def clean_Gaussian_noise_bilateral(im, radius, stdSpatial, stdIntensity):
    # Create the x and y grids for the neighborhood
    x, y = np.meshgrid(np.arange(-radius, radius + 1), np.arange(-radius, radius + 1))

    # Calculate the spatial weighting mask
    gs = np.exp(-(x ** 2 + y ** 2) / (2 * stdSpatial ** 2))
    gs = gs / gs.sum()
    # Initialize the filtered image
    bilateral_im = im.copy()

    # Iterate over the rows and columns of the image
    for i in range(radius, im.shape[0] - radius):
        for j in range(radius, im.shape[1] - radius):
            # Extract the neighborhood window
            window = im[i - radius:i + radius + 1, j - radius:j + radius + 1].astype(np.float)

            # Calculate the intensity weighting mask
            gi = np.exp(- (np.power((window - im[i, j]), 2) / (2 * stdIntensity ** 2)))

            # Normalize the masks so that the sum of their elements is 1
            gi = gi / gi.sum()

            # Calculate the filtered value for the pixel
            bilateral_im[i, j] = np.divide(np.sum(gi * gs * window), np.sum(gi * gs))

    return bilateral_im.astype(np.uint8)
