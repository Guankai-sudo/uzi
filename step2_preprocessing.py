from clearml import Task, Dataset
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
import cv2
import os
import joblib   # 新增，用于保存label_map
import yaml

task = Task.init(project_name="UZI_project", task_name="Pipeline Step 2: Preprocess Data")

task.execute_remotely()

# get parameters
args = Task.current_task().get_parameters_as_dict()
dataset_task_id = args.get("General", {}).get("dataset_task_id", None)
if not dataset_task_id:
    dataset_task_id = 'd4427d25445448e68c972f632c1f80ec'  

task.connect({"dataset_task_id": dataset_task_id})

# get the last step of metadata artifact
meta_task = Task.get_task(task_id=dataset_task_id)

# get dataset by name
dataset = Dataset.get(dataset_project="UZI_project", dataset_name="UZI_database")

# download and extract dataset
local_path = dataset.get_local_copy()
# 指定 YAML 文件路径
yaml_path = os.path.join(local_path, "data.yaml")

# 读取 YAML 文件为 Python dict
with open(yaml_path, 'r') as f:
    config_dict = yaml.safe_load(f)

# 上传 dict 为 artifact
task.upload_artifact(name="data", artifact_object=config_dict)


print("Step 2 done. ")
