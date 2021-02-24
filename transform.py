"""
Python Image Manipulation Empty Template by Kylie Ying (modified from MIT 6.865)

YouTube Kylie Ying: https://www.youtube.com/ycubed 
Twitch KylieYing: https://www.twitch.tv/kylieying 
Twitter @kylieyying: https://twitter.com/kylieyying 
Instagram @kylieyying: https://www.instagram.com/kylieyying/ 
Website: https://www.kylieying.com
Github: https://www.github.com/kying18 
Programmer Beast Mode Spotify playlist: https://open.spotify.com/playlist/4Akns5EUb3gzmlXIdsJkPs?si=qGc4ubKRRYmPHAJAIrCxVQ 
"""

from image import Image
import numpy as np

def brighten(image, factor):
    # when we brighten, we just want to make each channel higher by some amount 
    # factor is a value > 0, how much you want to brighten the image by (< 1 = darken, > 1 = brighten)
    x_pixels, y_pixels, num_channels = image.array.shape  # get the x, y pixels and channels

    new_image = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)

    """
    This way, we change pixel by pixel, channel by channel
    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                new_image.array[x, y, c] = image.array[x, y, c] * factor"""

    new_image.array = image.array * factor
    # for a numpy array, when we want to add something to every element, we can just do directly

    return new_image

def adjust_contrast(image, factor, mid):
    # adjust the contrast by increasing the difference from the user-defined midpoint by factor amount
    x_pixels, y_pixels, num_channels = image.array.shape  # get the x, y pixels and channels

    new_image = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)

    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                new_image.array[x, y, c] = (image.array[x, y, c] - mid) * factor + mid

    return new_image

def blur(image, kernel_size):
    # kernel size is the number of pixels to take into account when applying the blur
    # (ie kernel_size = 3 would be neighbors to the left/right, top/bottom, and diagonals)
    # kernel size should always be an *odd* number
    x_pixels, y_pixels, num_channels = image.array.shape  # get the x, y pixels and channels

    new_image = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)

    neighbor_range = kernel_size // 2

    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                total = 0
                for x_i in range(max(0, x-neighbor_range), min(x_pixels - 1 , x + neighbor_range) + 1):
                    for y_i in range(max(0, y - neighbor_range), min(y_pixels - 1, y + neighbor_range) + 1):
                        total += image.array[x_i, y_i, c]
                new_image.array[x, y, c] = total / (kernel_size ** 2)

    return  new_image


def apply_kernel(image, kernel):
    # the kernel should be a 2D array that represents the kernel we'll use!
    # for the sake of simiplicity of this implementation, let's assume that the kernel is SQUARE
    # for example the sobel x kernel (detecting horizontal edges) is as follows:
    # [1 0 -1]
    # [2 0 -2]
    # [1 0 -1]
    x_pixels, y_pixels, num_channels = image.array.shape  # get the x, y pixels and channels

    new_image = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)

    kernel_size = kernel.shape[0]
    neighbor_range = kernel_size // 2

    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                total = 0
                for x_i in range(max(0, x - neighbor_range), min(x_pixels - 1, x + neighbor_range) + 1):
                    for y_i in range(max(0, y - neighbor_range), min(y_pixels - 1, y + neighbor_range) + 1):
                        x_k = x_i + neighbor_range - x
                        y_k = y_i + neighbor_range - y
                        kernel_val = kernel[x_k, y_k]
                        total += image.array[x_i, y_i, c] * kernel_val
                new_image.array[x, y, c] = total

    return new_image


def combine_images(image1, image2):
    # let's combine two images using the squared sum of squares: value = sqrt(value_1**2, value_2**2)
    # size of image1 and image2 MUST be the same
    x_pixels, y_pixels, num_channels = image1.array.shape  # get the x, y pixels and channels
    new_image = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)

    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                new_image.array[x, y, c] = (image1.array[x, y, c] ** 2 + image2.array[x, y, c] ** 2) ** 0.5

    return new_image


if __name__ == '__main__':
    lake = Image(filename='lake.png')
    city = Image(filename='city.png')

    # light_lake = brighten(lake, 1.7)
    # light_lake.write_image("brighter-lake.png")

    # dark_lake = brighten(lake, 0.4)
    # dark_lake.write_image("darker-lake.png")

    # contrast_lake = adjust_contrast(lake, 2, 0.5)
    # contrast_lake.write_image("lake-contrast.png")

    # contrast_lake = adjust_contrast(lake, 0.5, 0.5)
    # contrast_lake.write_image("lake-reduce-contrast.png")
    # blur_city = blur(city, 3)
    # blur_city.write_image("blur-image.png")

    # blur_city = blur(city, 15)
    # blur_city.write_image("very-blur-image.png")

    """ sobel edge detection"""
    sobel_x = apply_kernel(city, np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]]))
    # sobel_x.write_image('edge_x.png')
    sobel_y = apply_kernel(city, np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]]))
    # sobel_y.write_image('edge_y.png')

    sobel_xy = combine_images(sobel_x, sobel_y)
    sobel_xy.write_image("edge_xy.png")
