from fastapi import FastAPI, UploadFile, File
import keras_ocr
from text_category_function import categorize_texts
# from skimage.io import imsave
from fastapi.responses import FileResponse

app = FastAPI()
pipeline = keras_ocr.pipeline.Pipeline()


@app.post("/process_image")
def get_image(image: UploadFile = File(...)):

    img = keras_ocr.tools.read(image.file)

    prediction_groups = pipeline.recognize([img])
    prediction_object = [(text, boxes.tolist())
                         for text, boxes in prediction_groups[0]]
    only_text = [text[0] for text in prediction_object]

    categorized_text: list = categorize_texts(only_text)

#     output_image = keras_ocr.tools.drawBoxes(
#         image=img, boxes=prediction_groups[0])

#     if output_image is not None:
#         imsave('assets/output.jpg', output_image)

    return {
        'categorized_text': categorized_text
    }


@app.get('/get_image/{image_key}')
def get_image(image_key: str):

    return FileResponse(path='assets/img.png')
