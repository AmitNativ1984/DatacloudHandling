import json
import os
import dtlpy as dl
if dl.token_expired():
    dl.login()

from tqdm import tqdm

# Get project and dataset
project = dl.projects.get(project_name='Kzir')
dataset = project.datasets.get(dataset_name='Lab_2020_03_09')

images_folder = r'/home/amit/Data/Kzir/Windows/LabWindows/from_dataloop/items/pics'
annotations_folder = r'/home/amit/Data/Kzir/Windows/LabWindows/from_dataloop/json/pics'

for _, img_filename in enumerate(tqdm(os.listdir(images_folder))):
    # get the matching annotations json
    _, ext = os.path.splitext(img_filename)
    ann_filename = os.path.join(annotations_folder, img_filename.replace(ext, '.json'))
    img_filename = os.path.join(images_folder, img_filename)

    # Upload or get annotations from platform (if already exists)
    item = dataset.items.upload(local_path=img_filename,
                                overwrite=False)
    assert isinstance(item, dl.Item)
    item.annotations.upload(annotations=ann_filename)
    # # read annotations from file
    # with open(ann_filename, 'r') as annotations_file:
    #     # annotations = json.load(f)
    #
