import glob
import os
import xmltodict
import json
import pprint

from PIL import Image


# Printing results
pp = pprint.PrettyPrinter(indent=4)


# Look for XML files and parses then as if they were Pascal VOC Files
def process():
    # Finds all XML files on data/ and append to list
    pascal_voc_contents = []
    os.chdir("data")

    print("Found {} files in data directory!".format(
        str(len(glob.glob("*.xml")))))
    for file in glob.glob("*.xml"):
        f_handle = open(file, 'r')
        print("Parsing file '{}'...".format(file))
        pascal_voc_contents.append(xmltodict.parse(f_handle.read()))

    # Process each file individually
    for index in pascal_voc_contents:
        image_file = index['annotation']['filename']
        # If there's a corresponding file in the folder,
        # process the images and save to output folder
        if os.path.isfile(image_file):
            extractDataset(index['annotation'])
        else:
            print("Image file '{}' not found, skipping file...".format(image_file))


# Extract image samples and save to output dir
def extractDataset(dataset):
    objects = dataset['object']
    if not isinstance(objects, list):
        objects = [objects]

    print("Found {} objects on image '{}'...".format(
        len(objects), dataset['filename']))

    # Open image and get ready to process
    img = Image.open(dataset['filename'])

    save_dir = dataset['filename'].split('.')[0]
   # Create output directory

    # Image name preamble
    sample_preamble = dataset['filename'].split('.')[0] + "_"
    # Image counter
    i = 0

    # Run through each item and save cut image to output folder
    for item in objects:
        # Convert str to integers
        save_dir = item['name']
        try:
            os.mkdir(save_dir)
        except:
            pass

        bndbox = dict([(a, int(b)) for (a, b) in item['bndbox'].items()])
        # Crop image
        im = img.crop((bndbox['xmin'], bndbox['ymin'],
                       bndbox['xmax'], bndbox['ymax']))
        # Save
        im.save(save_dir + "/" + sample_preamble + str(i) + '.png')
        i = i + 1


if __name__ == '__main__':
    print("\n------------------------------------")
    print("----- PascalVOC-to-Images v0.1 -----")
    print("Created by Giovanni Cimolin da Silva")
    print("------------------------------------\n")
    process()
