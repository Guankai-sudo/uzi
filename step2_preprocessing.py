from clearml import Task, Dataset
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
import cv2
import os


task = Task.init(project_name="UZI_project", task_name="Pipeline Step 2: Preprocess Data")

task.execute_remotely()

# get parameters
args = Task.current_task().get_parameters_as_dict()
dataset_task_id = args.get("General/dataset_task_id", None)
if not dataset_task_id:
    dataset_task_id = 'd4427d25445448e68c972f632c1f80ec'  

task.connect({"General/dataset_task_id": dataset_task_id})

# get the last step of metadata artifact
meta_task = Task.get_task(task_id=dataset_task_id)
df = meta_task.artifacts['UZI_df'].get()

# get the dataset path
dataset = Dataset.get(dataset_project="UZI_project", dataset_name="UZI_database")
img_path = dataset.get_local_copy()
csv_path = os.path.join(img_path, "english.csv")
os.remove(csv_path)


# get the part of the data
df_sample = df.sample(frac=0.1, random_state=42)
train_df = df_sample.sample(frac=0.8, random_state=42)
test_df = df_sample.drop(train_df.index)

# adjust image size
IMG_SIZE = (32, 32)

def load_images_labels(df, img_path):
    X = []
    y = []
    label_map = {label: idx for idx, label in enumerate(sorted(df['label'].unique()))}
    for _, row in df.iterrows():
        img_path = os.path.join(img_path, row['image'])
        image = cv2.imread(img_path)
        if image is not None:
            image = cv2.resize(image, IMG_SIZE)
            X.append(image)
            y.append(label_map[row['label']])
    return np.array(X), np.array(y)

X_train, y_train = load_images_labels(train_df, img_path)
X_test, y_test = load_images_labels(test_df, img_path)

# upload data and dataframe
task.upload_artifact('train_df', train_df)
task.upload_artifact('test_df', test_df)
task.upload_artifact('X_train', X_train)
task.upload_artifact('y_train', y_train)
task.upload_artifact('X_test', X_test)
task.upload_artifact('y_test', y_test)

print("Step 2 done. ")