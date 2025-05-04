from clearml import Dataset

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