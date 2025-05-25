from clearml import Task, Dataset

# Init ClearML Task
task = Task.init(project_name="UZI_project", task_name="Pipeline Step 1: Upload Dataset")

task.execute_remotely()


# change to your local_path
dataset_path = '/content/drive/MyDrive/ais/Database'

dataset = Dataset.create(
    dataset_name="UZI_database",
    dataset_project="UZI_project"
)

dataset.add_files(path=dataset_path)
dataset.upload()
dataset.finalize()

print("Dataset uploaded successfully")

print("Step 1 done.")