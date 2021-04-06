"""
convert class ids from one dataset to another.
bboxes with class ids that are not found in target classes are dropped
"""
import shutil
import argparse
import os
import numpy as np

def verify_yolo_bbox(label_file_org, label_file_new):
    """ convert convert cls ids in cls_org to cls_new.
        remove labels with no matching class in new.
        remove empty label files

    """

    bboxes = []

    with open(label_file_org, 'r') as f:
        replaced_bboxes = 0
        for line in f.read().splitlines():
            cls_id_org, x0, y0, w, h = line.split(" ")
            x0 = np.clip(float(x0), 0., 1.)
            y0 = np.clip(float(y0), 0., 1.)
            w = np.clip(float(w), 0., 1.)
            h = np.clip(float(h), 0., 1.)
            cls_id_org = int(cls_id_org)

            if x0 - w/2 <= 0:
                w -= 1e-5

            if x0 + w/2 >= 1:
                w -= 1e-5

            if y0 - h / 2 <= 0:
                h -= 1e-5

            if y0 + h / 2 >= 1:
                h -= 1e-5

            bbox = " ".join([str(int(cls_id_org)), str(x0), str(y0), str(w), str(h)])
            bboxes.append(bbox)
            replaced_bboxes += 1

    if replaced_bboxes > 0:
        with open(label_file_new, 'w+') as f:
            for bbox in bboxes:
                print(bbox, file=f)

    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="clipping bbox coordinates to be inside [0,1]",
                                     fromfile_prefix_chars="@")

    parser.add_argument('--source-labels', type=str,
                        required=True,
                        help='source label folder')

    args = parser.parse_args()

    # copy original labels folder
    target_labels = args.source_labels
    args.source_labels = args.source_labels+"_unclipped"
    shutil.copytree(target_labels, args.source_labels)
    shutil.rmtree(target_labels)
    os.makedirs(target_labels, exist_ok=True)

    # convert files
    for label_file in os.listdir(args.source_labels):
        verify_yolo_bbox(os.path.join(args.source_labels, label_file),
                           os.path.join(target_labels, label_file))

        print("verified: {}".format(label_file))
