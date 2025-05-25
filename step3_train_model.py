import os
if 'MPLBACKEND' in os.environ:
    del os.environ['MPLBACKEND']

import matplotlib
matplotlib.use('Agg')

from clearml import Task, Dataset
import pandas as pd
from ultralytics import YOLO

# === 初始化任务 ===
task = Task.init(project_name="UZI_project", task_name="Pipeline Step 3: Train Model")

task.execute_remotely()

# === 设置可供 HPO 调整的超参数 ===
args = Task.current_task().get_parameters_as_dict()
lr = args.get("General/lr0", 0.001)  # 提供默认值供 HPO 修改
task.connect({"General/lr0": lr})    # ✅ 告诉 ClearML 这是一个可以调优的超参数

dataset_task_id = args.get("General", {}).get("dataset_task_id", "9fee97e4b92644e8ae71209d44e4ad04")
task.connect({"dataset_task_id": dataset_task_id})
dataset = Dataset.get(dataset_project="UZI_project", dataset_name="UZI_database")
local_path = dataset.get_local_copy()
yaml_path = os.path.join(local_path, "data.yaml")

model = YOLO('yolov8n.pt')
model.train(
    data=yaml_path,
    epochs=100,
    imgsz=416,
    batch=16,
    lr0=lr,                           # ✅ 传入可调超参数
    name='yolov8n_asl',
    project='yolo_results'
)

logger = task.get_logger()
results_path = os.path.join("yolo_results", "yolov8n_asl", "results.csv")
if os.path.exists(results_path):
    df = pd.read_csv(results_path)
    last_row = df.iloc[-1]
    print("✅ Reporting metrics:", last_row.to_dict())

    def safe_report(series_name, column_name):
        try:
            value = float(last_row[column_name])
            iteration = int(last_row['epoch'])
            logger.report_scalar("metrics", series_name, value=value, iteration=iteration)
            print(f"✅ Reported {series_name}: {value}")
        except Exception as e:
            print(f"❌ Failed to report {series_name}: {e}")

    safe_report("mAP50(B)", 'metrics/mAP_0.5')
    safe_report("mAP50-95(B)", 'metrics/mAP_0.5:0.95')
    safe_report("precision(B)", 'metrics/precision')
    safe_report("recall(B)", 'metrics/recall')
else:
    print("❌ results.csv not found. No metrics reported.")


model_path = "yolo_results/yolov8n_asl/weights/best.pt"
if os.path.exists(model_path):
    task.upload_artifact('model', artifact_object=model_path)
    print("✅ Model uploaded.")
else:
    print("❌ Model file not found.")

print("✅ Step 3 done.")


