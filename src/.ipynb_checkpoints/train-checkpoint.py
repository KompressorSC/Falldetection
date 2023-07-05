from ultralytics import YOLO
from multiprocessing import freeze_support
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
           
if __name__ =="__main__":
    freeze_support()
# Load a model
    model_file = r'/root/autodl-tmp/falldetection/src/runs/detect/train20/weights/best.pt'
    model_file_cfg = r'/root/autodl-tmp/falldetection/model_file/isFall.yaml'
    #data_path = r'C:\code\walking_distraction\persons'
    model = YOLO(model_file)  # load a pretrained model (recommended for training)


    # Train the model
      
    model.train(data=model_file_cfg,device='cuda:0', epochs=500)
    metrics = model.val()  # evaluate model performance on the validation set
