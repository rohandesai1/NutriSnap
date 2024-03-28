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
        allLinks = []

        baseId = "mntl-card-list-items_"
        extra = "1-0"
        for i in range(24):
            currBox = s.find("a", {"id" : baseId + extra})
            boxes.append(currBox)
            allLinks.append(currBox["href"])
            extra = str(i + 2) + "-0"
            
        filteredLinks = []
        filteredBoxes = []
        ratings = []
        for i, box in enumerate(boxes):
            if box.find("div", {"class" : "mntl-recipe-card-meta__rating-count-number"}) != None:
                fullStars = len(box.find_all("svg", {"class" : "icon-star"}))
                halfStars = (len(box.find_all("svg", {"class" : "icon-star-half"})))
                stars = fullStars + halfStars/2
                rawReviewText = (box.find("div", {"class" : "mntl-recipe-card-meta__rating-count-number"}).text).split("\n")
                numberOfReviews = int(rawReviewText[1].replace(",", ""))
                score = (numberOfReviews/50) + stars
                ratings.append(score)
                filteredBoxes.append(box)
                filteredLinks.append(allLinks[i])

        

        boxes = filteredBoxes

        sorted_indexes = sorted(range(len(ratings)), key=lambda i: ratings[i], reverse=True)

        top3_indexes = sorted_indexes[:3]

        top3 = [boxes[i] for i in top3_indexes]
        
        recipes = []

        for box in top3:
            recipes.append(box.find("span", {"class" : "card__title"}).text)

        return list(zip(recipes, [filteredLinks[i] for i in top3_indexes]))
    except:
        return []

if __name__ == "__main__":
    ingredients = [input("Enter ingredient.")]
    print(get_recipe(ingredients))