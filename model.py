import food
import tensorflow as tf, numpy as np, pandas as pd, cv2
class CalorieCounter():
    def __init__(self):
        pass
        
        

    def calories_from_image(self, image):
        prediction = self.food_prediction(image)
        info = self.food_to_nutrition(prediction)
        cleaned = self.interpret_nutrition_info(info)
        return cleaned


    def food_prediction(self, image, model):
        if type(image) == str:
            image = cv2.imread(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        if model == 1:
            w, h = 256, 256
            self.model = tf.keras.models.load_model("assets")
            df_train = pd.read_csv("Training_Model/Model1/train_img.csv")
            df_train.drop_duplicates(subset = ["ClassName"])["ImageId"]
            self.label_names = np.asarray(sorted(df_train["ClassName"].unique()))
            

        else:
            w, h = 100, 100
            self.model = tf.keras.models.load_model("assets2")
            with open("labels.txt", "r") as file:
                self.label_names = file.read().split("\n")

        
        
        
        image = cv2.resize(image, (w,h))
        predictions = self.model.predict(image.reshape(1, w, h, 3, 1))[0]
        chosen = predictions.argmax()
        print(self.label_names[chosen])
        if model == 1:
            return self.label_names[chosen].split("-")
        else:
            return self.label_names[chosen].split(" ")
    
    def food_to_nutrition(self, prediction):
        prediction = [value for value in prediction if value != "with" and value != "without"] # filter filler words
        print(prediction)
        finalPred = None
        maxMatches = 0
        secondaryPred = None
        secondMaxMatches = 0
        for fd in food.get_report():
            matches = 0
            for item in prediction:
                if item.lower() == fd["Category"].lower():
                    matches += 2
                if item.lower() in fd["Description"].lower():
                    matches += 1
                        
            if matches > maxMatches:
                maxMatches = int(matches)
                finalPred = fd
            elif matches > secondMaxMatches:
                secondMaxMatches = matches
                secondaryPred = fd

        return finalPred, secondaryPred
    
    def interpret_nutrition_info(self, predictions):
        allInfo = []
     
        for prediction in predictions:
            
            description = prediction["Description"]
            prediction = prediction["Data"]
            fats = prediction["Fat"]
            carbs = prediction["Carbohydrate"]
            cholestrol = prediction["Cholesterol"]
            fiber = prediction["Fiber"]
            protein = prediction["Protein"]
            sodium = prediction["Major Minerals"]["Sodium"]
            sugar = prediction["Sugar Total"]
            mono = fats["Monosaturated Fat"]
            poly = fats["Polysaturated Fat"]
            sat = fats["Saturated Fat"]
            calories = 4 * (carbs + protein) + 9 * (mono + poly + sat)

            nutrition = [description, calories, carbs, cholestrol, fiber, protein, sodium, sugar, mono, poly, sat]
            nutrition = [description] + [round((val), 1) for val in nutrition[1:]]
            tags = ["Description", "Calories", "Carbs", "Cholestrol", "Fiber", "Protein", "Sodium", "Sugar", "Monosaturated Fat", "Polysaturated Fat", "Saturated Fat"]
            #tags = [(list(prediction.keys()))[(list(prediction.values())).index(val)] for val in nutrition]
            info = [f"{tag}: {val}" for tag,val in list(zip(tags, nutrition))]
            info = list(zip(tags, nutrition))

            allInfo.append(info)

        return allInfo


def main():
    counter = CalorieCounter()
    info = counter.calories_from_image("test_images/test_images/0a3c32bc94.jpg")
    print(info)
    #print(nutrition_info)

    


if __name__ == "__main__":
    main()