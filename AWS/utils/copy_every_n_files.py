"""
converts all images of type *.jp2 to *.jpg
"""


from PIL import Image
import os
from tqdm import tqdm
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="copy every X files from folder", fromfile_prefix_chars="@")

    parser.add_argument('--source', type=str,
                        required=True,
                        help='source folder of images')

    parser.add_argument('--dest', type=str,
                        required=True,
                        help='copy files here')

    parser.add_argument('--n', type=int,
                        required=True,
                        help='copy every n files')

    parser.add_argument('--newfiletype', type=str,
                        default='jpg',
                        help='convert image files to this file type')

    parser.add_argument('--filetype', type=str,
                        default='bmp',
                        help='convert image files to this file type')

    args = parser.parse_args()
    source_path = args.source

    os.makedirs(args.dest, exist_ok=True)

    for curr_path in os.walk(source_path):
        # check files do exist in current path
        files = curr_path[-1]
        if not files:
            continue

        pbar = tqdm(files)
        pbar.set_description("copying every {} files".format(args.n))
        for N, f in enumerate(pbar):
            if f.endswith(args.filetype) and N % args.n == 0:
                img_file = os.path.join(curr_path[0], f)
                img = Image.open(img_file)
                new_img_file = os.path.join(args.dest, f.replace(args.filetype, args.newfiletype))
                img.save(new_img_file)