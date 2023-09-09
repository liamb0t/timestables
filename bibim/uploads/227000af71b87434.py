from random import randint 

q = 0
correct = 0
high_score = 0

def problem(limit):
    global q
    global correct
    global high_score
    q += 1
    a = randint(1, limit)
    b = randint(1, limit)
    x = input(f'{a} x {b} = ')
    if int(x) == (a*b):
        correct += 1
        problem(limit)
    else:
        if correct > high_score:
            high_score = correct
            print(f'New high score! {high_score}')
        print(f'The correct answer was {a * b}') 
        print(f'{correct}/{q} correct')
        y = input('Would you like to play again? Y/N')
        if y == 'Y':
            q = 0
            correct = 0
            problem(limit)
        else:
            return

def start():
    x = int(input('Up to what number would you like to practice?'))
    problem(x)

start()
