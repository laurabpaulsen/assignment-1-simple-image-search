import cv2
import matplotlib.pyplot as plt
import pandas as pd
from math import ceil
from pathlib import Path


def load_image_rgb(image_path: Path):
    """
    Loads an image in in BGR format and converts it to RGB
    
    Parameters
    -----------
    image_path : Path 
        path to the image
    
    Returns
    --------
    image : numpy.ndarray
        image in RGB format
    """
    image = cv2.imread(str(image_path))
    
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)



def nrows_ncols(n:int):
    """
    A function which calculates the number of rows and columns for a plot of n images.

    Parameters
    -----------
    n : int
        number of images to plot

    
    Returns
    --------
    nrows : int
        number of rows
    ncols : int 
        number of columns
    """
    if ceil(n**0.5)**2 == n:
        return (int(n**0.5), int(n**0.5))
    
    else: 
        # optimal number of columns
        ncols = int(n**0.5)
        # optimal number of rows
        nrows = int(n/ncols)

        # is the number of columns optimal?
        if nrows * ncols < n:
            nrows += 1
        
        return (nrows, ncols)

def plot_similar(df:pd.DataFrame, chosen_image:str):
    """
    Plots the n most similar images to the chosen image
    
    Parameters
    -----------
    df : pd.DataFrame
        dataframe with the n most similar images to the chosen image
    
    chosen_image : str 
        path to the chosen image

    Returns
    --------
    plt : matplotlib.pyplot
        plot of the n most similar images
    """

    nrows, ncols = nrows_ncols(len(df))

    fig, axs = plt.subplots(nrows, ncols, figsize = (nrows * 10, ncols * 10))
    
    for i, ax in enumerate(axs.flatten()):
        
        try:
            image = load_image_rgb(df.iloc[i, 0])
            ax.imshow(image)
            ax.set_title(f"Distance: {round(df.iloc[i, 1], 3)}", fontsize = 15*ncols)
        except IndexError: # if the index is out of range(i.e., no more rows in similar), just leave the axis empty
            pass

        if i == 0:
            ax.set_title(f"Chosen image:\n{chosen_image}", color = "red", fontsize = 15 * ncols)
            # put a frame in red around the chosen image
            ax.plot([0, 0, image.shape[1], image.shape[1], 0], [0, image.shape[0], image.shape[0], 0, 0], color = "red", linewidth = 7)
            
        ax.axis("off")

    plt.tight_layout()

    return plt
