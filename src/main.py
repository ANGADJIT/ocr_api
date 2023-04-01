from fastapi import FastAPI,UploadFile,File

import keras_ocr
import json

app=FastAPI()
pipeline = keras_ocr.pipeline.Pipeline()

@app.post("/get_image")
def get_image(image: UploadFile = File(...)):
     
     img = keras_ocr.tools.read(image.file) 
     prediction_groups = pipeline.recognize([img])
     prediction_object=[(text,boxes.tolist()) for text, boxes in prediction_groups[0]]
     only_text=[text[0] for text in prediction_object ]
     only_boxes=[box[1] for box in prediction_object[0] ]
     return {
          'text':only_text,
          'boxes':only_boxes
     }
    		

     