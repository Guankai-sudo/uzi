import os
if 'MPLBACKEND' in os.environ:
    del os.environ['MPLBACKEND']

import matplotlib
matplotlib.use('Agg')

from clearml import Task
from clearml.automation import PipelineController


pipe = PipelineController(
    name="UZI_Pipeline",
    project="UZI_project",
    version="1.0",
    add_pipeline_tags=True
)

pipe.set_default_execution_queue("pipeline")

# Step 1：upload dataset
pipe.add_step(
    name="step1_upload_dataset",
    base_task_project="UZI_project",
    base_task_name="Pipeline Step 1: Upload Dataset"
)

# Step 2：preprocess data
pipe.add_step(
    name="step2_preprocessing",
    parents=["step1_upload_dataset"],
    base_task_project="UZI_project",
    base_task_name="Pipeline Step 2: Preprocess Data",
    parameter_override={
        "General/dataset_task_id": "${step1_upload_dataset.id}"
    }
)

# Step 3：model training
pipe.add_step(
    name="step3_train_model",
    parents=["step2_preprocessing"],
    base_task_project="UZI_project",
    base_task_name="Pipeline Step 3: Train Model",
    parameter_override={
        "General/dataset_task_id": "${step2_preprocessing.id}"
    }
)

# Step 4：HPO
pipe.add_step(
    name="task_hpo",
    parents=["step3_train_model"], 
    base_task_project="UZI_project",
    base_task_name="Pipeline Step 4: HPO",
    parameter_override={
        "General/dataset_task_id": "${step3_train_model.id}" 
    }
)

pipe.start_locally()
#pipe.start(queue="pipeline")

print(" done.")