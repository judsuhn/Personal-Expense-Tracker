import random


def play_game():
    lucky_number = random.randint(1, 20)
    attempts = 0
    storage = []

    print("Welcome to the Lucky Game Show!")
    print("Select a number 1 - 20")

    while True:
        guess = int(input("What's your guess?"))
        attempts += 1
        storage.append(guess)

        if guess != lucky_number:
            print("Oh no try again!")
            print(f"Previously used, {sorted(storage)}")
        elif guess == lucky_number:
            print(
                f"Congrats! This took {attempts} Attempts! Previously Used: {sorted(storage)}")
            break


play_game()
