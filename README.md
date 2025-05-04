# uzi

# Handwritten Character Recognition AI System
This project aims to develop an AI-powered system that recognizes handwritten text from images using deep learning models. It supports both baseline (CNN-LSTM) and advanced (Transformer-based TrOCR) models, integrated into a modular end-to-end (E2E) pipeline for scalable deployment and experimentation.

## Objective
The handwritten character recognition system is designed to improve efficiency in scenarios where manual data entry or text digitization is time-consuming or error-prone. It can be used in educational institutions for automatically grading handwritten assignments, in financial and legal sectors to digitize handwritten documents, and in government or healthcare systems to extract critical information from handwritten forms. By leveraging state-of-the-art computer vision and deep learning techniques, our system interprets and converts handwritten text into digital format with high accuracy. This solution supports our expansion into the education, finance, and public service sectors by enabling faster, more reliable, and intelligent data processing workflows.

## Project structure
<pre>
ASL/
├── step1_upload_dataset.py      # Upload image dataset and generate metadata
├── step2_preprocessing.py       # Load and preprocess images, upload training/test sets
├── step3_train_model.py         # Train the CNN model and save the weights
├── main.py                      # ClearML Pipeline controller
├── upload_dataset.py            # Upload local data
└── README.md
</pre>
# Getting Started
## 1. Install Dependencies
<pre>
  pip install clearml
  pip install clearml-agent
</pre>
## 2. Configure ClearML
Create a credential from the clearml workspace and paste it above
<pre>
  clearml-init
</pre>
## 3. Upload local datasets to clearML datasets
<pre>
  python upload_dataset.py
</pre>
# Run three steps and store it in the project
Before starting the following steps, you need to create a new queue called pipeline in the works & queues of clearml, so that subsequent agents can listen to the queue and run the project steps according to their pipeline order.
## 1 Upload image dataset and generate metadata
 <pre> python step1_dataset_upload.py</pre>
## 2 Load and preprocess images, upload training/test sets
  <pre> python step2_preprocessing.py</pre>
## 3 Train the CNN model and save the weights
   <pre>  python step3_train_model.py  </pre> 
## 4 start ClearML Agent
  <pre> clearml-agent daemon --queue pipeline --detached  </pre> 
## 5 Run the pipeline controller to register its three steps into ASL_Pipeline
   <pre>  python main.py  </pre> 
# The following is the pipeline operation diagram

<img width="293" alt="readme" src="https://github.com/user-attachments/assets/a003b172-2e23-4041-95c2-804cfe1ee946" />


