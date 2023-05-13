import cv2
import pandas as pd
from tqdm import tqdm
from pathlib import Path
import numpy as np

# tensorflow VGG16 for extracting features
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.applications.vgg16 import preprocess_input

from numpy.linalg import norm

from sklearn.neighbors import NearestNeighbors

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

def extract_features(image_path: Path, model):
    """
    Extracts features for image search from image using a pretrained model. 
    
    Parameters
    -----------
    image_path : Path 
        The path to the image to extract features from
    model : Model
        Pretrained model (e.g., VGG16)

    Returns
    -------
    features : np.array
        The features extracted from the image
    """
    # load image from file path
    img = load_img(image_path, target_size=(224, 224))
    
    # prepare image to be input to the model
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)

    # generate feature representation
    features = model.predict(img, verbose=0) 

    # flatten features
    features = features.flatten()

    # normalise features
    features = features / norm(features)

    return features

def image_search_knn(chosen_image, image_paths: list, model, n:int = 5):
    """
    Parameters
    -----------
    chosen_image : Path 
        The path to the chosen image
    image_paths : list 
        list of paths to the images
    model : Model
        Pretrained model (e.g., VGG16)
    n : int
        number of most similar images to return (default = 5)

    Returns
    -------
    df : pd.Dataframe
        dataframe with the n most similar images to the chosen image
    """
    # ind of chosen image in list
    index = image_paths.index(chosen_image)

    # extract features for all images
    features = [extract_features(img, model) for img in image_paths]
    
    # fit KNN 
    neighbours = NearestNeighbors(
        n_neighbors=n+1, 
        algorithm='brute',
        metric='cosine'
        ).fit(features)

    # extract features for the target image
    target_features = features[index]

    # find the nearest neighbours for target
    distances, indices = neighbours.kneighbors([target_features])
    indices = np.array(indices[0]).astype(int)

    # sort distances (and include image paths)
    dist = sorted(zip([image_paths[i] for i in indices], distances[0]), key=lambda x: x[1])
    
    # creating a dataframe with the n most similar images including the filename and the distance
    df = pd.DataFrame(dist, columns = ["image", "distance"])

    return df
