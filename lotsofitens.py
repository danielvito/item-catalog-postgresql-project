#!/usr/bin/env python

from app import db
from app.models import User, Category, CategoryItem, Brand

db.create_all()

# Brands
brand1 = Brand(name="Nike")
brand2 = Brand(name="Adidas")
brand3 = Brand(name="Wilson")
db.session.add(brand1)
db.session.add(brand2)
db.session.add(brand3)
db.session.commit()

# Categories
category1 = Category(name="Soccer")
category2 = Category(name="Basketball")
category3 = Category(name="Baseball")
category4 = Category(name="Frisbee")
category5 = Category(name="Snowboarding")
category6 = Category(name="Rock Climbing")
category7 = Category(name="Foosball")
category8 = Category(name="Skating")
category9 = Category(name="Hockey")
db.session.add(category1)
db.session.add(category2)
db.session.add(category3)
db.session.add(category4)
db.session.add(category5)
db.session.add(category6)
db.session.add(category7)
db.session.add(category8)
db.session.add(category9)
db.session.commit()


# Soccer
categoryItem1 = CategoryItem(name="Two shinguards",
                             description="Two shinguards description ...",
                             price="$7.50", category=category1, brand=brand1)
categoryItem2 = CategoryItem(name="Shinguards",
                             description="Shinguards description ...",
                             price="$8.50", category=category1, brand=brand2)
categoryItem3 = CategoryItem(name="Jersey",
                             description="Jersey description ...",
                             price="$2.50", category=category1, brand=brand3)
categoryItem4 = CategoryItem(name="Soccer Cleats",
                             description="Soccer Cleats description ...",
                             price="$1.00", category=category1, brand=brand3)
# Baseball
categoryItem5 = CategoryItem(name="Bat",
                             description="Bat description ...",
                             price="$0.50", category=category3, brand=brand2)
# Frisbee
categoryItem6 = CategoryItem(name="Frisbee",
                             description="Frisbee description ...",
                             price="$17.50", category=category4, brand=brand1)
# Snowboarding
categoryItem7 = CategoryItem(name="Googles",
                             description="Googles description ...",
                             price="$24.20", category=category5, brand=brand1)
categoryItem8 = CategoryItem(name="Snowboard",
                             description="Snowboard description ...",
                             price="$6.29", category=category5, brand=brand2)
# Hockey
categoryItem9 = CategoryItem(name="Stick",
                             description="Stick description ...",
                             price="$71.59", category=category9, brand=brand3)

db.session.add(categoryItem1)
db.session.add(categoryItem2)
db.session.add(categoryItem3)
db.session.add(categoryItem4)
db.session.add(categoryItem5)
db.session.add(categoryItem6)
db.session.add(categoryItem7)
db.session.add(categoryItem8)
db.session.add(categoryItem9)
db.session.commit()

print("Added records!")
