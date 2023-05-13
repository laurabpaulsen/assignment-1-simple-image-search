"""
Assigment 1 for visual analytics (S2023)

This script finds the n most similar images in a directory to a chosen image by comparing their histograms using the chi squared distance metric.

It saves a csv file with the n most similar images and a plot of the n most similar images to a desired output directory.

The script takes the following arguments:
    -i: filename of the chosen image
    -d: path to the directory containing the images
    -n: number of most similar images to return (defaults to 5)
    -o: path to the output directory
    -a: the search algorithm to use (defaults to "hist")

Usage: python src/image_search.py -i <image> -d <image directory> -n <number of similar images> -o <output directory> -a <searc_algorithm>

Author: Laura Bock Paulsen (202005791)
"""

import argparse as ap

# local module import
import sys 
from pathlib import Path
sys.path.append(str(Path(__file__).parents[1])) # add the parent directory to the path (to be able to import utils no matter where the script is run from )

from utils import plot_similar, image_search_dist, image_search_knn

def parse_args():
    """
    Parses the arguments passed to the script

    Parameters
    -----------
    None
    
    Returns
    --------
    args : dict
        dictionary with the arguments
    """
    parser = ap.ArgumentParser()
    parser.add_argument("-i", "--image", help = "Filename of the chosen image", type = str)
    parser.add_argument("-d", "--directory", help = "Path to the directory containing the images", default = "data/flowers", type = str)
    parser.add_argument("-n", "--number", help = "Number of most similar images to return", default = 5, type = int)
    parser.add_argument("-o", "--output", help = "Path to the output directory", default = "out", type=str)
    parser.add_argument("-a", "--search_algorithm", help = "The search algorithm to use. Can be 'knn' or 'hist'", default = "hist", type=str)
    
    return vars(parser.parse_args())


def list_images_dir(directory:Path):
    """
    Lists all the files in the data directory with .jpg or .png extensions.
    
    
    Parameters
    ----------
    directory : Path
        path to the directory

    Returns
    --------
    images : list 
        list of all the images paths in the directory
    """
    files = list(directory.iterdir())
    
    images = [f for f in files if f.suffix == ".jpg" or f.suffix == ".png"]
    
    return images

def main():
    # parse arguments
    args = parse_args()
    
    # create output directory if it does not exist
    if not Path(args["output"]).exists():
        Path(args["output"]).mkdir(parents=True)
    
    # list images in the data directory
    images = list_images_dir(Path(args['directory']))

    # chosen image path
    chosen_image = Path(f"{args['directory']}/{args['image']}")

    # get the n most similar images
    if args["search_algorithm"].lower() == "hist":
        similar = image_search_dist(chosen_image, images, n = args['number'])
    
    elif args["search_algorithm"].lower() == "knn":
        from tensorflow.keras.applications.vgg16 import VGG16
        
        # initialize model without the classification layers
        model = VGG16(weights='imagenet', include_top=False, pooling='avg',input_shape=(224, 224, 3))        
        image_search_knn(chosen_image, images, model, n = args['number'])
    
    else:
        raise ValueError("The search algorithms implemented are 'knn' and 'hist'. Please input one of the two.")

    # save the dataframe
    similar.to_csv(Path(f"{args['output']}/{args['number']}_most_similar_{args['image'].split('.')[0]}_{args['search_algorithm']}.csv"), index = False)

    # plot the n most similar images
    plot = plot_similar(similar, chosen_image)

    # save the plot
    plot.savefig(Path(f"{args['output']}/{args['number']}_most_similar_{args['image'].split('.')[0]}_{args['search_algorithm']}.png"))



if __name__ == "__main__": 
    main()

    
