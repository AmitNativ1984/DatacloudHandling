"""
converts all images of type *.jp2 to *.jpg
"""


from PIL import Image
import os
from tqdm import tqdm
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="convert jp2 to jpg", fromfile_prefix_chars="@")

    parser.add_argument('--source', type=str,
                        required=True,
                        help='all files under this folder and its subfolders will be converted')

    args = parser.parse_args()
    source_path = args.source
    for curr_path in os.walk(source_path):
        # check files do exist in current path
        files = curr_path[-1]
        if not files:
            continue

        pbar = tqdm(files)
        pbar.set_description("converting files in {}".format(curr_path[0]))
        for f in pbar:
            if f.endswith(".jp2"):
                img_file = os.path.join(curr_path[0], f)
                img = Image.open(img_file)
                new_img_file = img_file.replace(".jp2", ".jpg")
                img.save(new_img_file)
                os.remove(img_file)