import os

def generate_negative_description_file():
    # open the input file for writing. Will overwrite all existing data in there.
    with open('Else/Cascade_train/neg.txt', 'w') as f:
        # loop over all the filenames
        for filename in os.listdir('Else/Cascade_train/negative'):
            f.write('Else/Cascade_train/negative/' + filename + '\n')