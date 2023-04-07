from fastapi import FastAPI, UploadFile, File
import keras_ocr
from text_category_function import categorize_texts
from fastapi.responses import FileResponse
import matplotlib.pyplot as plt

app = FastAPI()
pipeline = keras_ocr.pipeline.Pipeline()


@app.post("/process_image")
def process_image(image: UploadFile = File(...)):
    
    img = keras_ocr.tools.read(image.file)

    images: list = [img]

    prediction_groups = pipeline.recognize(images)
    prediction_object = [(text, boxes.tolist())
                         for text, boxes in prediction_groups[0]]
    only_text = [text[0] for text in prediction_object]

    categorized_text: list = categorize_texts(only_text)

    _, axs = plt.subplots(figsize=(10, 8))
    keras_ocr.tools.drawAnnotations(image=img,predictions=prediction_groups[0],ax=axs)
    axs.set_title('text detection output')
    plt.savefig('image.png')

    return {
        'categorized_text': categorized_text
    }


@app.get('/get_image/{image_key}')
def get_image(image_key: str):

    return FileResponse(path='assets/img.png')
