from flask import Flask, render_template, url_for, request
import numpy as np, random
import cv2
from PIL import Image
from model import CalorieCounter
from recipe import get_recipe
app = Flask(__name__)
@app.route("/", methods = ["POST", "GET"])

def index():
    if request.method == "GET":
        info = ""
        headers = [":",":"]
        nutrition = [[""],[""]]
        serving = ""
        recipes = ""
        prediction = ""
    if request.method == "POST":
        counter = CalorieCounter()
        try:
            image = Image.open(request.files["image"].stream)
        except:
            return render_template("index.html", heading1="File type not supported", prediction="")
        image = np.array(image)[:, :, :3]
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        #cv2.imwrite("img" + "".join([random.choice("abcdefghijklmnopqrstuvwxyz123456789") for i in range(10)]) + ".png", image)

        """
        prediction = counter.food_prediction(image, 2)
        info = counter.food_to_nutrition(prediction)
        info = counter.interpret_nutrition_info(info)
        """

        prediction = counter.food_prediction(image, 1)
        recipes = get_recipe(prediction)
        info2 = counter.food_to_nutrition(prediction)
        info2 = counter.interpret_nutrition_info(info2)
        info = info2

        if info == "Not Found":

            return render_template("index.html", heading2 = (f"Detected: {' '.join(prediction)}. Not found in USDA database of food nutrition."), prediction="")
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
                    nutrition[z].append(f"{tag}: {val}")
                except UnboundLocalError:
                    nutrition = [[f"{tag}: {val}"], [], [], []]
            z += 1

        serving = "Serving Size: 100 grams, Nutrition Source: USDA"

        

    return render_template('index.html', prediction=" ".join(prediction) , heading1 = headers[0].split(":")[1], heading2 = headers[1].split(":")[1],  nutritionInfo1 = " ".join(nutrition[0]), nutritionInfo2 = " ".join(nutrition[1]), servingSize = serving, recipe = recipes)



if __name__ == "__main__":
    app.run(host = "0.0.0.0", debug = True, port = "8000")