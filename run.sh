#!/bin/bash

source ./env/bin/activate

image="image_0268.jpg"
data="data/flowers"
num_results=5
output="out"

algorithms="knn hist"

echo -e "[INFO]: Finding ${num_results} similar images to ${image} in ${data}. Output will be saved in ${output}."

# Loop over the search algorithms
for algorithm in $algorithms; do
    echo "Running search algorithm: $algorithm"
    python3 src/image_search.py -i "$image" -d "$data" -n "$num_results" -o "$output" -a "$algorithm"
done

deactivate