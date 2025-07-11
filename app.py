from flask import Flask, render_template, request, redirect, url_for
import cv2
import os
import shutil

app = Flask(__name__)

IMAGE_PATH = 'static/capture.jpg'
GREYSCALE_PATH = 'static/greyscale.jpg'

@app.route('/', methods=['GET', 'POST'])
def index():

    print('hi')
    image_exists = os.path.exists(IMAGE_PATH)
    greyscale_exists = os.path.exists(GREYSCALE_PATH)


    # Default values for form fields
    model_number = ''
    selected_part = ''
    measurement_type = ''
    shift_name = ''

    if request.method == 'POST':
        print('hi2')
        model_number = request.form.get('model_number', '')
        selected_part = request.form.get('part_number', '')
        measurement_type = request.form.get('measurement_type', '')
        shift_name = request.form.get('shift_name', '')

        if 'capture' in request.form:
            print('inside capture block')
            # Capture image from webcam
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            cap.release()
            if ret:
                cv2.imwrite(IMAGE_PATH, frame)
                image_exists =True
            # Pass form values back to template
            return render_template(
                'index.html',
                measurement_exists=greyscale_exists,
                image_exists=image_exists,
                part_numbers=['6609220CD', '650658200'],
                model_number=model_number,
                selected_part=selected_part,
                measurement_type=measurement_type,
                shift_name=shift_name
            )

        elif 'measurement' in request.form and image_exists:
            # Convert to greyscale
            img = cv2.imread(IMAGE_PATH)
            grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(GREYSCALE_PATH, grey)
            greyscale_exists = True 
            return render_template(
                'index.html',
                measurement_exists=greyscale_exists,
                image_exists=image_exists,
                part_numbers=['6609220CD', '650658200'],
                model_number=model_number,
                selected_part=selected_part,
                measurement_type=measurement_type,
                shift_name=shift_name
            )
        elif 'submit' in request.form and image_exists and greyscale_exists:
            print("Saving images...")
            # Save images to a new folder
            folder_name = model_number or 'default_folder'
            folder_path = os.path.join('data', folder_name)
            os.makedirs(folder_path, exist_ok=True)
            shutil.copy(IMAGE_PATH, os.path.join(folder_path, f"{folder_name}_original.jpg"))
            shutil.copy(GREYSCALE_PATH, os.path.join(folder_path, f"{folder_name}_greyscale.jpg"))
            # Delete images from static path
            if os.path.exists(IMAGE_PATH):
                os.remove(IMAGE_PATH)
            if os.path.exists(GREYSCALE_PATH):
                os.remove(GREYSCALE_PATH)
            
            # Clear form fields
            model_number = ''
            selected_part = ''
            measurement_type = ''
            shift_name = ''
            image_exists = False
            greyscale_exists = False
            return render_template(
                    'index.html',
                    measurement_exists=greyscale_exists,
                    image_exists=image_exists,
                    part_numbers=['6609220CD', '650658200'],
                    model_number='',
                    selected_part='',
                    measurement_type='',
                    shift_name=''
                )
    print('hi before last render')
    return render_template(
        'index.html',
        measurement_exists=greyscale_exists,
        image_exists=image_exists,
        part_numbers=['6609220CD', '650658200'],
        model_number=model_number,
        selected_part=selected_part,
        measurement_type=measurement_type,
        shift_name=shift_name
    )

if __name__ == '__main__':
    app.run(debug=True)