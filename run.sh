source env/bin/activate

image = "image_0268.jpg"
data = "data/flowers"
num_results = 5
output = "out"

echo -e "[INFO]: Finding ${num_results} similar images to ${image} in ${data}. Output will be saved in ${output}."
python src/image_search.py -i image_0268.jpg  -d data/flowers -n 5 -o out 
deactivate