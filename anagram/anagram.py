import random
with open("words.txt", "r") as fobj:

    contents = fobj.read()

listofwords = contents.split(",")
while True:
    correct_word = listofwords[random.randint(0, 500)]
    correctwordlist = []
    for letter in correct_word:
        correctwordlist.append(letter)
    random.shuffle(correctwordlist)
    shuffled_word = ""
    for character in correctwordlist:
        shuffled_word += character

    print(f"The jumbled up word is {shuffled_word}. Can you guess what is the original? ")
    while True:
        guess = input("Enter your guess: ")
        if guess == correct_word:
            print("That is correct! ")
            break
        else:
            give_up = input("That is incorrect. Would you like to give up? (Y/N)")
            if give_up == "Y":
                print(f"The correct word is {correct_word}. ")
                break
            else:
                print("Peseverance is key! ")

    more = input("One more game? (Y/N)")
    if more == "N":
        break