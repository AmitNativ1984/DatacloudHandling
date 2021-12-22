"""
convert class ids from one dataset to another.
bboxes with class ids that are not found in target classes are dropped
"""
import argparse
import os

def create_cls_labels_dict(labels_file):
    cls2label = {}
    with open(labels_file, "r") as f:
        for i, line in enumerate(f):
            label = line.split("\n")[0]
            cls2label[label] = i
    
    return cls2label

def list_all_files_from_subdirs(parentPath, filext=".txt"):
    """
        list all file in current directory and subdirectories, with specific file extension:
    """

    filelist = []
    for root, dir, files in os.walk(parentPath):
        for file in files:
            if os.path.splitext(file)[-1] == filext:
                filelist.append(os.path.join(root, file))

    return filelist

def convert_label_file(label_file_org, idx2label_source, label2idx_target):
    """ convert convert cls ids in cls_org to cls_new.
        remove labels with no matching class in new.
        remove empty label files
    """

    bboxes = []

    with open(label_file_org, 'r') as f:
        replaced_bboxes = 0
        for line in f.read().splitlines():
            cls_idx_source, x0, y0, w, h = line.split(" ")

            cls_idx_source = int(cls_idx_source)
            cls_label_source = idx2label_source[cls_idx_source]
            if cls_idx_source in idx2label_source.keys():
                cls_idx_target = label2idx_target[cls_label_source]
                bbox = " ".join([str(int(cls_idx_target)), str(x0), str(y0), str(w), str(h)])
                bboxes.append(bbox)
                replaced_bboxes += 1

    if replaced_bboxes > 0:
        os.remove(label_file_org)
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

    label2idx_source = create_cls_labels_dict(args.cls_org)
    idx2label_source = dict(zip(label2idx_source.values(), label2idx_source.keys()))
    label2idx_target = create_cls_labels_dict(args.cls_new)
   
    
   # get all txt files in source labels:
    labels_list = list_all_files_from_subdirs(args.source_labels, filext=".txt")
     
    
    # # convert files
    for label_file in labels_list:
        convert_label_file(os.path.join(args.source_labels, label_file),
                           idx2label_source, 
                           label2idx_target)
        print("converted: {}".format(label_file))
