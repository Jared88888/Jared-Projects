import random
import os

suits = ["hearts", "diamonds", "clubs", "spades"]
numbers = [2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King", "Ace"]
deck = []

for i in suits:
    for j in numbers:
        card = f"{j} of {i}"
        deck.append(card)

num_of_players = int(input("How many players? "))
money = {} #store player:total money left     #money no reset every round
for i in range(num_of_players):
    money[f"Player {i+1}"] = 100
money["Banker"] = 200

while True:
    more = input("One more round? ('N' to stop) ").upper()
    if more == "N":
        break
    else:
        hands = {} #store player:their hand     #hands reset every round
        total_value = {} #store player:total value of their cards     #total value resets every round
        bets = {} #store player:bet     #bet resets every round
        for i in range(num_of_players):
            hands[f"Player {i+1}"] = []
            total_value[f"Player {i+1}"] = 0
        hands["Banker"] = []
        total_value["Banker"] = 0

        for i in range(10):
            random.shuffle(deck)

        def value(card1, num_of_cards): #to retrieve value of card
            first = (card1.split())[0]
            if first in ["Jack", "Queen", "King"]:
                return 10
            elif first == "Ace" and num_of_cards ==  2:
                return 11
            elif first == "Ace" and num_of_cards !=  2:
                return 10
            else:
                return int(first)

        for i in money: #giving each player 2 cards first
            if i != "Banker":
                bet = float(input(f"{i}, how much would you like to bet? "))
                bets[i] = bet
            while True:
                reveal = input(f"{i}, press enter to reveal your first card. ")
                if reveal == "":
                    print(deck[0])
                    hands[i].append(deck[0])
                    break
            while True:
                reveal = input(f"{i}, press enter to reveal your second card. ")
                if reveal == "":
                    print(deck[1])
                    hands[i].append(deck[1])
                    break

            total_value[i] = value(deck[0], len(hands[i])) + value(deck[1], len(hands[i]))

            if (deck[0].split())[0] == "Ace" and (deck[1].split())[0] == "Ace":
                print("Double Ace, you win triple: ")
                total_value[i] = "Double Ace"
            elif total_value[i] == 21:
                print("Blackjack, you win double. ")
                total_value[i] = "Blackjack"
            else:
                print(f"Your total is {total_value[i]}")
                

            deck.remove(deck[0])
            deck.remove(deck[0])

        if total_value["Banker"] == "Double Ace":
            for i in money:
                if total_value[i] != "Double Ace": #if player also double ace, tie
                    money["Banker"] += (bets[i] * 3) #else banker gain money
                    money[i] -= (bets[i] * 3) #player loses money
            print("Round ends. ")

        elif total_value["Banker"] == "Blackjack":
            for i in money:
                if total_value[i] == "Double Ace": #Double Ace beats blackjack
                    money["Banker"] -= (bets[i] * 3)
                    money[i] += (bets[i] * 3)
                elif total_value[i] != "Blackjack": #if player also blackjack, tie
                    money["Banker"] += (bets[i] * 2) #else banker gains money
                    money[i] -= (bets[i] * 2) #player loses money
            print("Round ends. ")

        else: #drawing more cards
            for i in money:
                if i != "Banker": #for non banker
            
                    if total_value[i] == "Double Ace" or total_value[i] == "Double Ace":
                        print("You dont have to draw anymore. ")
                    else:
                        while total_value[i] < 16:
                            take = input(f"{i}, your total is less than 16, you have to take 1 more card:(press enter) ")
                            if take == "":
                                print(f"Your card is {deck[0]}. ")
                                hands[i].append(deck[0])

                                total_value[i] = 0 #reset, loop throuh ount again cuz of change in length which affects ace
                                for b in hands[i]:
                                    total_value[i] += value(b, len(hands[i]))
                                deck.remove(deck[0])

                                counter = 0 #triple seven
                                for c in hands[i]:
                                    if "7" in (c.split())[0]:
                                        counter += 1
                                if counter == 3:
                                    print("Triple seven! You win seven times. ")
                                    total_value[i] = "Triple 7"

                                for j in hands[i]: #makin ace 1 if bust
                                    if "Ace" in j and total_value[i] > 21:
                                        total_value[i] = total_value[i] - 9
                                print(f"Your total is {total_value[i]}. ")

                                if len(hands[i]) == 5 and total_value[i] < 21: #win double
                                    print("5 cards and under 21! You win double. ")
                                    total_value[i] = "5 cards"

                        if total_value[i] < 21 and total_value[i] != "5 cards":
                            while True:
                                if total_value[i] > 21:
                                    break
                                take_more = input(f"{i}, would you still like to take more cards? (Y/N) ").upper()
                                if take_more == "N":
                                    break
                                else:
                                    print(f"Your card is {deck[0]}. ")
                                    hands[i].append(deck[0])

                                    total_value[i] = 0
                                    for b in hands[i]:
                                        total_value[i] += value(b, len(hands[i]))
                                    deck.remove(deck[0])

                                    for a in hands[i]:
                                        if "Ace" in a and total_value[i] > 21:
                                            total_value[i] = total_value[i] - 9

                                    print(f"Your total is {total_value[i]}. ")
                                    if len(hands[i]) == 5 and total_value[i] < 21:
                                        print("5 cards and under 21! You win double")
                                        total_value[i] = "5_cards"
                                    break
                                
                        if total_value[i] > 21:
                            print("You bust. ")
                            total_value[i] = "Bust"
                    print("/n" * 50)

                else: ####################################for banker
                    while total_value[i] < 16:
                        take = input(f"{i}, your total is less than 16, you have to take 1 more card:(press enter) ")
                        if take == "":
                            print(f"Your card is {deck[0]}. ")
                            hands[i].append(deck[0])

                            total_value[i] = 0 #reset, loop throuh ount again cuz of change in length which affects ace
                            for b in hands[i]:
                                total_value[i] += value(b, len(hands[i]))
                            deck.remove(deck[0])

                            counter = 0 #triple seven
                            for c in hands[i]:
                                if "7" in (c.split())[0]:
                                    counter += 1
                            if counter == 3:
                                print("Triple seven! You win seven times. ")
                                total_value[i] = "Triple 7"

                            for j in hands[i]: #makin ace 1 if bust
                                if "Ace" in j and total_value[i] > 21:
                                    total_value[i] = total_value[i] - 9
                            print(f"Your total is {total_value[i]}. ")

                            if len(hands[i]) == 5 and total_value[i] < 21: #win double
                                print("5 cards and under 21! You win double. ")
                                total_value[i] = "5 cards"

                    if total_value[i] < 21 and total_value[i] != "5 cards":
                        reveal_everyone = input("Would you like to reveal everyone's card ('N' to skip). ")
                        revealed_everyone = False
                        if reveal_everyone != "N":
                            revealed_everyone = True
                            print("Revealing everyone's cards")

                            for i in total_value:
                                if i != "Banker":
                                    while True:
                                        revealll = input(f"{i}, press enter to reveal if you won: ")
                                        if revealll == "":
                                            if total_value["Banker"] == "Triple 7": #not possible for 2 players to triple 7
                                                money["Banker"] += (bets[i] * 7)
                                                print(f"Banker triple seven. Banker wins. ")
                                                
                                            elif total_value["Banker"] == "5_cards":

                                                if total_value[i]  == "Triple 7":
                                                    money["Banker"] -= (bets[i] * 7)
                                                    money[i] += (bets[i] * 7)
                                                    print("Your triple 7 beats banker. ")
                                                elif total_value[i] != "5_cards" and total_value[i] != "Blackjack":
                                                    money["Banker"] += (bets[i] * 2)
                                                    money[i] -= (bets[i] * 2)
                                                    print("Banker wins, 5 cards and under 21, you pay double")
                                                else:
                                                    print("You tie with banker. ")

                                            else:

                                                if total_value[i] == "Triple 7":
                                                    money["Banker"] -= (bets[i] * 7)
                                                    money[i] += (bets[i] * 7)
                                                    print("Your triple 7 beats banker. ")
                                                elif total_value[i] == "Double Ace":
                                                    money["Banker"] -= (bets[i] * 3)
                                                    money[i] += (bets[i] * 3)
                                                    print("Your double ace beats banker. ")
                                                elif total_value[i] == "Blackjack" or total_value[i] == "5_cards":
                                                    money["Banker"] -= (bets[i] * 7)
                                                    money[i] += (bets[i] * 7)
                                                    print("You beat banker, win double. ")
                                                else:
                                                    if total_value[i] > total_value["Banker"]:
                                                        print(f"{total_value[i]} is more than {total_value["Banker"]}, {i} wins banker. ")
                                                        money["Banker"] -= bets[i]
                                                        money[i] += bets[i]
                                                        
                                                    elif total_value[i] == total_value["Banker"]:
                                                        print(f"{total_value[i]} is same as {total_value["Banker"]}, {i} ties banker. ")

                                                    else:
                                                        print(f"{total_value[i]} is less than {total_value["Banker"]}, {i} loses banker. ")
                                                        money["Banker"] += bets[i]
                                                        money[i] -= bets[i]
                                            break

                        else:
                            while True:
                                if total_value[i] > 21:
                                    break
                                for h in hands:
                                    print(f"{h} has {len(hands[h])} cards. ")

                                while True: #banker open others first / can open multiple players so while loop
                                    reveal = input(f"{i}, which player's hand would you like to open first ('N' to skip): ").upper()
                                    if reveal != "N":
                                        if total_value[f"Player {reveal}"] > total_value[i]:
                                            print(f"{total_value[i]} is more than {total_value[f"Player {reveal}"]}. Banker wins. ")
                                            money[i] += bets[f"Player {reveal}"]
                                            money[f"Player {reveal}"] -= bets[f"Player {reveal}"]

                                        elif total_value[f"Player {reveal}"] == total_value:
                                            print(f"{total_value[i]} is same as {total_value[f"Player {reveal}"]}. Tie. ")

                                        else:
                                            print(f"{total_value[i]} is less than {total_value[f"Player {reveal}"]}. Banker loses. ")
                                            money[i] -= bets[f"Player {reveal}"]
                                            money[f"Player {reveal}"] += bets[f"Player {reveal}"]
                                    else:
                                        break

                                take_more = input(f"{i}, would you still like to take more cards? (Y/N) ").upper()
                                if take_more == "N":
                                    break
                                else:
                                    print(f"Your card is {deck[0]}. ")
                                    hands[i].append(deck[0])

                                    total_value[i] = 0
                                    for b in hands[i]:
                                        total_value[i] += value(b, len(hands[i]))
                                    deck.remove(deck[0])

                                    for a in hands[i]:
                                        if "Ace" in a and total_value[i] > 21:
                                            total_value[i] = total_value[i] - 9

                                    print(f"Your total is {total_value[i]}. ")
                                    if len(hands[i]) == 5 and total_value[i] < 21:
                                        print("5 cards and under 21! You win double")
                                        total_value[i] = "5_cards"
                                    
                            
                    if total_value[i] > 21:
                        print("You bust. ")
                        total_value[i] = "Bust"
                        
                if revealed_everyone == False:
                    print("Revealing everyone's cards")

                    for i in total_value:
                        if i != "Banker":
                            while True:
                                revealll = input(f"{i}, press enter to reveal if you won: ")
                                if revealll == "":
                                    if total_value["Banker"] == "Triple 7": #not possible for 2 players to triple 7
                                        money["Banker"] += (bets[i] * 7)
                                        print(f"Banker triple seven. Banker wins. ")
                                        
                                    elif total_value["Banker"] == "5_cards":

                                        if total_value[i]  == "Triple 7":
                                            money["Banker"] -= (bets[i] * 7)
                                            money[i] += (bets[i] * 7)
                                            print("Your triple 7 beats banker. ")
                                        elif total_value[i] != "5_cards" and total_value[i] != "Blackjack":
                                            money["Banker"] += (bets[i] * 2)
                                            money[i] -= (bets[i] * 2)
                                            print("Banker wins, 5 cards and under 21, you pay double")
                                        else:
                                            print("You tie with banker. ")

                                    else:

                                        if total_value[i] == "Triple 7":
                                            money["Banker"] -= (bets[i] * 7)
                                            money[i] += (bets[i] * 7)
                                            print("Your triple 7 beats banker. ")
                                        elif total_value[i] == "Double Ace":
                                            money["Banker"] -= (bets[i] * 3)
                                            money[i] += (bets[i] * 3)
                                            print("Your double ace beats banker. ")
                                        elif total_value[i] == "Blackjack" or total_value[i] == "5_cards":
                                            money["Banker"] -= (bets[i] * 7)
                                            money[i] += (bets[i] * 7)
                                            print("You beat banker, win double. ")
                                        else:
                                            if total_value[i] > total_value["Banker"]:
                                                print(f"{total_value[i]} is more than {total_value["Banker"]}, {i} wins banker. ")
                                                money["Banker"] -= bets[i]
                                                money[i] += bets[i]
                                                
                                            elif total_value[i] == total_value["Banker"]:
                                                print(f"{total_value[i]} is same as {total_value["Banker"]}, {i} ties banker. ")

                                            else:
                                                print(f"{total_value[i]} is less than {total_value["Banker"]}, {i} loses banker. ")
                                                money["Banker"] += bets[i]
                                                money[i] -= bets[i]
                                    break

        #tests
        for i in money:
            print(f"{i}, has {money[i]}. ")

        print(hands)
        print(total_value)
        print(bets)

