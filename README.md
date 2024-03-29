# **NutriSnap**
Welcome to the Food Nutrition Detector! This project offers an effective way for users to capture photos of their food and retrieve nutritional data about it. Powered by custom Convolutional Neural Networks, along with various other Python libraries, the goal is to make tracking your food intake as effortless as taking a snapshot.

## **Demo**


https://github.com/rohandesai1/NutriSnap/assets/126644574/904557a6-31f1-4a77-93f3-0220cc6269b9

## **Usage**
  
  To run the core app, you must do the following:
  
  1. Enter this command to clone the repository
  <br></br>
  ```git clone https://github.com/rohandesai1/NutriSnap```
  <br></br>
  2. Insall the required dependencies
  <br></br>
  ```pip install -r requirements.txt```
  <br></br>
  3. Run the Program.
  <br></br>
  ```python3 app.py``` and open ```localhost:8000```
  

The Training_Model folder contains all files (except the datasets) used to train the models. The dependencies used to train the model are not listed in the requirements.txt file. 
Assets and Assets2 are the 2 models that were trained.
Dataset #1 can be found [HERE](https://www.kaggle.com/datasets/bjoernjostein/food-classification)
Dataset #2 can be found [HERE](https://www.kaggle.com/datasets/kmader/food41)


## Features
 
- Image Capture: Use your device's camera to take a picture of your food.
- Deep Learning Analysis: The TensorFlow model identifies the food items in the picture.
- Nutrition Data Retrieval: Get a detailed breakdown of calories, macronutrients, and more for the identified food.
