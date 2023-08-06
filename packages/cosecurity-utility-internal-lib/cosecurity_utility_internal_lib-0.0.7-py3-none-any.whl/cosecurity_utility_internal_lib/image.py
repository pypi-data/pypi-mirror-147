import numpy as np


def to_image(image:np.ndarray) -> np.ndarray:
    """
    Method to convert an array to an array with type uint8

    Parameters:
        image (np.ndarray): image array

    Returns:
        np.ndarray: converted matrix from image
    """
    return np.asarray(image).astype(np.uint8)

def crop(image:np.ndarray, x:int, y:int, w:int, h:int) -> np.ndarray:
    """
    Method to crop the image

    Parameters:
        image (np.ndarray): converted matrix from image
        x (int): starting x position within the image
        y (int): starting y position within the image
        w (int): width to be cut
        h (int): height to be cut

    Returns:
        np.ndarray: image cropped from the dimensions passed via parameter
    """
    return image[y:y+h, x:x+w]
