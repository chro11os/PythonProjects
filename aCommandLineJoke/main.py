import os
import time

funny = "you"
name = "Neil"

def joke():

    choice = input(f"Do you wanna hear a joke? yes or no: ")

    if (choice == "yes"):
        print(f"okay here's a joke for you")
        time.sleep(3)
        print(funny + " " +  name + " your'e a fucking joke.")
    else:
        print("Aw shucks too bad maybe next time")

def unjoke():

    choice2 = input(f"what's that? You want to hear a song now? (yes or no): ")

    if (choice2 == "yes"):
        print(f"Okay here goes nothing")
        time.sleep(4)
        print(f"Never Gonna give you up")
        time.sleep(1.5)
        print(f"Never gonna let you down")
        time.sleep(1.5)
        print(f"Never gonna turn around and desert you!")
        time.sleep(3)
        print(f"Finally im done, how was it??")



# implement a switch case in down here the two choices are
# joke() and unjoke()

choice3 = input(f"What do you wanna hear a joke or something much more verbose!! (joke or unjoke): ")
if choice3 == "joke":
    joke()
else:
    unjoke()


