print("Jai Shree Ram")
score=350
team="India"
exam_score=23.76
print((team) + " scored " + str(score))
print(type(team))
print(str(score).isdigit())
print(str(score).isalpha())
print(len(str(score)))
print(team.count("i"))
print(int(exam_score))
score+=1
print(score)
place=input("where do you want to go?")
if place=="Vrindavan":
    print("Lets go to " + (place) + " Radhe Radhe!")
if place=="Ladhak":
    print("Lets visit ice stupa")
if place=="America":
    print("Lets go to America. Hurray!")
else: print("where is that?")