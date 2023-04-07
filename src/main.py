from fastapi import FastAPI, UploadFile, File, HTTPException, status, BackgroundTasks
import keras_ocr
from text_category_function import categorize_texts
from fastapi.responses import FileResponse
import matplotlib.pyplot as plt
from string import ascii_letters
from random import sample
from files_manager import files_manager
from os import remove
from time import sleep

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
    keras_ocr.tools.drawAnnotations(
        image=img, predictions=prediction_groups[0], ax=axs)

    file_name: str = ''.join(sample(ascii_letters, k=8))
    file_path: str = f'assets/tempfiles/{file_name}.png'

    files_manager.add_path(file_name=file_name, file_path=file_path)

    plt.savefig(file_path)

    return {
        'categorized_texts': categorized_text,
        'file_key': file_name
    }


@app.get('/get_image/{image_key}')
async def get_image(image_key: str, background_task: BackgroundTasks):
    background_task.add_task(lambda: (
        sleep(2),
        remove(path)
    ))
    path: str = files_manager.get_path(file_name=image_key)

    if path is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            'error': 'invalid image_key'})

    response = FileResponse(path, media_type='image/png')

    return response
