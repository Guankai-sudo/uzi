from clearml import Task, Dataset

# Init ClearML Task
task = Task.init(project_name="UZI_project", task_name="Pipeline Step 1: Upload Dataset")

task.execute_remotely()



print("Dataset uploaded successfully")

print("Step 1 done.")