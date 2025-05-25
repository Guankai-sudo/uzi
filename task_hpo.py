from clearml import Task
from clearml.automation import UniformParameterRange
from clearml.automation import HyperParameterOptimizer


task = Task.init(project_name="UZI_project", task_name="Pipeline Step 4: HPO", task_type=Task.TaskTypes.optimizer)

task.execute_remotely()

# get parameters
args = Task.current_task().get_parameters_as_dict()


dataset_task_id = args.get("General", {}).get("dataset_task_id", None)
if not dataset_task_id:
    dataset_task_id = "d4427d25445448e68c972f632c1f80ec"  
task.connect({"dataset_task_id": dataset_task_id})
# get the last step of metadata artifact
meta_task = Task.get_task(task_id=dataset_task_id)

optimizer = HyperParameterOptimizer(
    base_task_id=dataset_task_id,
    hyper_parameters = [
      UniformParameterRange(
        name='General/lr0',
        min_value=1e-5,
        max_value=1e-2,
        step_size=1e-5  
      )
    ],
    objective_metric_title='metrics',   
    objective_metric_series='mAP50(B)', 
    objective_metric_sign='max',            
    max_number_of_concurrent_tasks=2,           
    max_iteration_per_job=1,           
    total_max_jobs=10,                  
    execution_queue='pipeline',
    project_name="UZI_project",
    task_name="YOLOv8 HPO with Default Optimizer"
)


optimizer.set_time_limit(in_minutes=60)

optimizer.start()
print("🏁 HPO started successfully")