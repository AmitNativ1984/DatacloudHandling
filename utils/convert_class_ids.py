"""
convert class ids from one dataset to another.
bboxes with class ids that are not found in target classes are dropped
"""
import shutil
import argparse
import os

def convert_label_file(label_file_org, label_file_new, cls_org, cls_new):
    """ convert convert cls ids in cls_org to cls_new.
        remove labels with no matching class in new.
        remove empty label files

    """

    bboxes = []

    with open(label_file_org, 'r') as f:
        replaced_bboxes = 0
        for line in f.read().splitlines():
            cls_id_org, x0, y0, w, h = line.split(" ")

            cls_id_org = int(cls_id_org)
            cls_name_org = [key for key, val in cls_org.items() if val == cls_id_org][0]

            if cls_name_org in cls_new.keys():
                cls_id_new = cls_new[cls_name_org]
                bbox = " ".join([str(int(cls_id_new)), str(x0), str(y0), str(w), str(h)])
                bboxes.append(bbox)
                replaced_bboxes += 1

    if replaced_bboxes > 0:
        with open(label_file_new, 'w+') as f:
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

    # copy original labels folder
    target_labels = args.source_labels
    args.source_labels = args.source_labels+"_copy"
    shutil.copytree(target_labels, args.source_labels)
    shutil.rmtree(target_labels)
    os.makedirs(target_labels, exist_ok=True)

    # create dicts for class names:
    with open(args.cls_org) as f:
        cls_names = f.read().splitlines()
    cls_id = list(range(len(cls_names)))
    cls_org_dict = dict(zip(cls_names, cls_id))

    with open(args.cls_new) as f:
        cls_names = f.read().splitlines()
    cls_id = list(range(len(cls_names)))
    cls_new_dict = dict(zip(cls_names, cls_id))

    # convert files
    for label_file in os.listdir(args.source_labels):
        convert_label_file(os.path.join(args.source_labels, label_file),
                           os.path.join(target_labels, label_file),
                           cls_org_dict,
                           cls_new_dict)
        print("converted: {}".format(label_file))
