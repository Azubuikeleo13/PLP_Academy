"""Assignment 1: Design Your Own Class! 🏗️

Create a class representing anything you like (a Smartphone, Book, or even a Superhero!).
Add attributes and methods to bring the class to life!
Use constructors to initialize each object with unique values.
Add an inheritance layer to explore polymorphism or encapsulation.
"""

class Smartphone:
    def __init__(self, name, model, color):
        self.__name = name
        self.__model = model
        self.__color = color

class Apple(Smartphone):
    
    def ring(self):
        print("Ding ding ding")

class Samsung(Smartphone):
    def ring(self):
        print("Dong dong dong")

class Xiaomi(Smartphone):
    pass

class Redmi(Xiaomi):
    def ring(self):
        print("Dang dang dang")


iphone_X = Apple("Iphone X", "AIXXYFYTY655", "Gold Silver")
galaxy_fold = Samsung("Galaxy Fold", "SFDNIKHFFD6165", "Sky Blue")
redmi_note13 = Redmi("Redmi Note 13", "25GDDTHBVCF", "Ocean Sunset")

redmi_note13.ring()


"""Activity 2: Polymorphism Challenge! 🎭

Create a program that includes animals or vehicles with the same action (like move()). However, make each class define move() differently (for example, Car.move() prints "Driving" 🚗, while Plane.move() prints "Flying" ✈️).
"""

class Vehicle:
    def __init__(self, name, model, color, track):
        self.name = name
        self.model = model
        self.color = color
        self.track = track

class Car(Vehicle):
    def move_by(self):
        print(f"I move by {self.track}")

class Aeroplane(Vehicle):
    def move_by(self):
        print(f"I move by {self.track}")

class Train(Vehicle):
    def move_by(self):
        print(f"I move by {self.track}")

class Ship(Vehicle):
    def move_by(self):
        print(f"I move by {self.track}")

lexus = Car("Lexus", "Toyota", "Blue", "Road")
air_ways = Aeroplane("Air_ways", "Air Peace", "Gradient White", "Air")
train = Train("Railway AirWays", "Bullet Train", "Ash", "Railway")
boat = Ship("Boat Ways", "Marine Blue", "Off White", "Water")

air_ways.move_by()
