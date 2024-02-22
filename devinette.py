import random

def game():
    number_to_guess = random.randint(1, 100)
    guess = None
    attempts = 0

    while guess != number_to_guess:
        guess = int(input("Devinez le nombre entre 1 et 100: "))
        attempts += 1
        if guess < number_to_guess:
            print("Trop bas!")
        elif guess > number_to_guess:
            print("Trop haut!")
    
    print(f"Félicitations! Vous avez deviné le nombre en {attempts} tentatives.")

if __name__ == "__main__":
    game()