import requests as rq
from bs4 import BeautifulSoup as bs

def get_recipe(ingredients):
    try:
        base_link = "https://www.allrecipes.com/search?q="
        link = "https://www.allrecipes.com/search?q="
        breaker = "%2C"

        for ingredient in ingredients:
            link += ingredient + breaker
        r = rq.get(link)
        c = r.content
        s = bs(c, "html.parser")
        boxes = []
        baseId = "mntl-card-list-items_"
        extra = "1-0"
        for i in range(24):
            boxes.append(s.find("a", {"id" : baseId + extra}))
            extra = str(i + 2) + "-0"
        filteredBoxes = []
        ratings = []
        for box in boxes:
            if box.find("div", {"class" : "mntl-recipe-card-meta__rating-count-number"}) != None:
                fullStars = len(box.find_all("svg", {"class" : "icon-star"}))
                halfStars = (len(box.find_all("svg", {"class" : "icon-star-half"})))
                stars = fullStars + halfStars/2
                rawReviewText = (box.find("div", {"class" : "mntl-recipe-card-meta__rating-count-number"}).text).split("\n")
                numberOfReviews = int(rawReviewText[1].replace(",", ""))
                score = (numberOfReviews/50) + stars
                ratings.append(score)
                filteredBoxes.append(box)
        

        boxes = filteredBoxes

        sorted_indexes = sorted(range(len(ratings)), key=lambda i: ratings[i], reverse=True)

        top3_indexes = sorted_indexes[:3]

        top3 = [boxes[i] for i in top3_indexes]
        

        recipes = []
        for box in top3:
            recipes.append(box.find("span", {"class" : "card__title"}).text)
        links = []
        for recipe in recipes:
            links.append(base_link + recipe.replace(" ", "+"))

        return list(zip(recipes, links))
    except:
        return []

if __name__ == "__main__":
    ingredients = [input("Enter ingredient.")]
    print(get_recipe(ingredients))