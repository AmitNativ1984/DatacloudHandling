"""
convert class ids from one dataset to another.
bboxes with class ids that are not found in target classes are dropped
"""
import shutil
import argparse
import os

def convert_label_file(label_file_org, cls_converter):
    """ convert convert cls ids in cls_org to cls_new.
        remove labels with no matching class in new.
        remove empty label files

    """

    bboxes = []

    with open(label_file_org, 'r') as f:
        replaced_bboxes = 0
        for line in f.read().splitlines():
            cls_idx_org, x0, y0, w, h = line.split(" ")

            # cls_idx_org = int(cls_idx_org)
            
            if cls_idx_org in cls_converter.keys():
                cls_idx_new = cls_converter[cls_idx_org]
                bbox = " ".join([str(int(cls_idx_new)), str(x0), str(y0), str(w), str(h)])
                bboxes.append(bbox)
                replaced_bboxes += 1

    os.remove(label_file_org)
    if replaced_bboxes > 0:
        with open(label_file_org, 'w+') as f:
            for bbox in bboxes:
                print(bbox, file=f)

    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="converting cls ids based on class names files new and old (*.names0)",
                                     fromfile_prefix_chars="@")

    parser.add_argument('--source-labels', type=str,
                        required=True,
                        help='source label folder')

    parser.add_argument('--cls-org', type=str,
                        required=True,
                        help='source names files (must be *.names)')

    parser.add_argument('--cls-new', type=str,
                        required=True,
                        help='target class names (must be *.names)')

    args = parser.parse_args()

    args.cls_org = args.cls_org.split(",")
    args.cls_new = args.cls_new.split(",")
    cls_converter = dict(zip(args.cls_org, args.cls_new))

    # convert files
    for label_file in os.listdir(args.source_labels):
        convert_label_file(os.path.join(args.source_labels, label_file),
                           cls_converter)
        print("converted: {}".format(label_file))
