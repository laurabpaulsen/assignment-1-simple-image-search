import cv2
import pandas as pd
from tqdm import tqdm
from pathlib import Path

def image_hist_normalize(image_path: Path):
    """
    Loads an image, calculates its histogram across all three color channels and min-max normalizes it.
    
    Parameters
    -----------
    image_path : Path
        path to the image
    
    Returns
    -------
    hist_norm : np.array
        normalized histogram of the image
    """
    
    image = cv2.imread(str(image_path))
    hist = cv2.calcHist([image], [0,1,2], None, [256,256,256], [0,256, 0,256, 0,256])
    hist_norm = cv2.normalize(hist, hist, 0, 1.0, cv2.NORM_MINMAX)
    
    return hist_norm


def image_search_dist(chosen_image: Path, image_paths:list, n:int = 5):
    """
    Finds the n most similar images to the chosen image by comparing their normalised histograms using the chi squared distance metric.
    
    Parameters
    -----------
    chosen_image : Path 
        path to the chosen image
    image_paths : list: 
        list of paths to the images
    n : int
        number of most similar images to return (default = 5)

    Returns
    -------
    df : pd.DataFrame 
        dataframe with the n most similar images to the chosen image
    """
    # get the histogram of the chosen image
    chosen = image_hist_normalize(chosen_image)

    # remove the chosen image from the list
    image_paths.remove(chosen_image)
    

    distances = []
    for image in tqdm(image_paths, desc = 'Analysing images'): # tqdm is used to show a progress bar
        hist = image_hist_normalize(image)
        distances.append((image, cv2.compareHist(chosen, hist, cv2.HISTCMP_CHISQR)))

    # sort distances
    distances.sort(key = lambda x: x[1])

    # get the n most similar images and chosen image 
    dist = [(chosen_image, 0)] + distances[:n]
    
    # creating a dataframe with the n most similar images including the filename and the distance
    df = pd.DataFrame(dist, columns = ["image", "distance"])
    
    return df