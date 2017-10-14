import os

import pandas as pd
import scipy.misc
from celery import shared_task, current_task
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from hog import hog


@shared_task
def create_hog(original_file_name):
    current_task.update_state(meta={'process_percent': 25})
    print('Enter create_hog')

    fs = FileSystemStorage()
    original_image = fs.open(original_file_name)
    current_task.update_state(meta={'process_percent': 50})

    image = scipy.misc.imread(original_image)
    histogram_descriptor, hog_image = hog(image)  # , pixels_per_cell=(16, 16), cells_per_block=(4, 4))
    current_task.update_state(meta={'process_percent': 80})

    hog_file_name = 'hog_' + original_file_name
    hog_file_path = os.path.join(settings.MEDIA_ROOT, hog_file_name)
    scipy.misc.imsave(hog_file_path, hog_image)
    current_task.update_state(meta={'process_percent': 90})

    hog_image_url = fs.url(hog_file_name)
    original_photo_url = fs.url(original_file_name)

    histogram_descriptor = pd.Series(histogram_descriptor).to_json(orient='values')
    # pd.read_json('?', orient='values')
    current_task.update_state(meta={'process_percent': 99})
    print('Exit create_hog')
    return histogram_descriptor, original_photo_url, hog_image_url
