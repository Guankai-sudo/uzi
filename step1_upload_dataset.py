from clearml import Task, Dataset
import pandas as pd
import os

# Init ClearML Task
task = Task.init(project_name="UZI_project", task_name="Pipeline Step 1: Upload Dataset")

task.execute_remotely()

# get dataset by name
dataset = Dataset.get(dataset_project="UZI_project", dataset_name="UZI_database")

# download and extract dataset
local_path = dataset.get_local_copy()
csv_path = os.path.join(local_path, "english.csv")
df = pd.read_csv(csv_path)


# upload dataframe for artifact
task.upload_artifact(name='UZI_df', artifact_object=df)

print("Step 1 done.")