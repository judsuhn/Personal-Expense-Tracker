def collatz(number):
    collatz_number = [number]
    while number != 1:
        if number % 2 == 0:
            number = number // 2
        elif number % 2 == 1:
            number = 3 * number + 1
        collatz_number.append(number)
    for x in collatz_number:
        print(x)


number = int(input('What is your number?: '))
collatz(number)
