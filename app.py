from flask import Flask, render_template, url_for, request
import numpy as np
import cv2
from PIL import Image
from model import CalorieCounter

app = Flask(__name__)
@app.route("/", methods = ["POST", "GET"])

def index():
    if request.method == "GET":
        info = ""
        headers = ["",""]
        nutrition = [[""],[""]]
    if request.method == "POST":
        counter = CalorieCounter()
        image = Image.open(request.files["image"].stream)
        image = np.array(image)[:, :, :3]
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cv2.imwrite("img.png", image)
        """
        prediction = counter.food_prediction(image, 2)
        info = counter.food_to_nutrition(prediction)
        info = counter.interpret_nutrition_info(info)
        """
        prediction2 = counter.food_prediction(image, 1)
        info2 = counter.food_to_nutrition(prediction2)
        info2 = counter.interpret_nutrition_info(info2)
        info = info2
        #info = info + info2
        print(info)
        
        z = 0
        for item in info:
            tag1, val1 = item[0]
            try:
                headers.append(f"{tag1}: {val1}")
            except UnboundLocalError:
                headers = [f"{tag1}: {val1}"]
            for tag, val in item[1:]:
                try:
                    print(z)
                    nutrition[z].append(f"{tag}: {val}")
                except UnboundLocalError:
                    nutrition = [[f"{tag}: {val}"], [], [], []]
            z += 1

        

    return render_template('index.html', heading1 = headers[0], heading2 = headers[1],  nutritionInfo1 = " ".join(nutrition[0]), nutritionInfo2 = " ".join(nutrition[1]))


if __name__ == "__main__":
    app.run(host = "0.0.0.0", debug = True, port = "8000")