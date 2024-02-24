import random
import time
import pickle

attempt_limit = 30
record_file = 'records.pkl'

def load_records():
    try:
        with open(record_file, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return []

def save_records(records):
    with open(record_file, 'wb') as f:
        pickle.dump(records, f)

def give_hint(guess, number_to_guess):
    difference = abs(guess - number_to_guess)
    if difference < 10:
        return "Très proche!"
    elif difference < 50:
        return "Proche!"
    else:
        return "Loin!"

def game():
    records = load_records()
    player_names = input("Entrez les noms des joueurs, séparés par des virgules: ").split(',')
    difficulty = input("Choisissez un niveau de difficulté (facile, moyen, difficile): ")

    if difficulty.lower() == 'facile':
        number_to_guess = random.randint(1, 50)
    elif difficulty.lower() == 'moyen':
        number_to_guess = random.randint(1, 100)
    elif difficulty.lower() == 'difficile':
        number_to_guess = random.randint(1, 1000)
    else:
        print("Niveau de difficulté non reconnu. Utilisation du niveau moyen par défaut.")
        number_to_guess = random.randint(1, 100)

    attempts = {player_name: 0 for player_name in player_names}

    while True:
        for player_name in player_names:
            start_time = time.time()
            user_input = input(f"{player_name}, devinez le nombre ou tapez 'quitter' pour arrêter: ")

            if user_input.lower() == 'quitter':
                end_time = time.time()
                elapsed_time = end_time - start_time
                minutes, seconds = divmod(elapsed_time, 60)
                print("Merci d'avoir joué, {}! Temps écoulé: {} minutes {} secondes".format(player_name, int(minutes), int(seconds)))
                return

            try:
                guess = int(user_input)
            except ValueError:
                print("Ce n'est pas un nombre valide. Essayez encore.")
                continue

            if guess < 1 or guess > 1000:
                print("Le nombre doit être entre 1 et 1000. Essayez encore.")
                continue

            attempts[player_name] += 1

            if attempts[player_name] > attempt_limit:
                print("Vous avez dépassé la limite de tentatives. Merci d'avoir joué!")
                return

            if guess < number_to_guess:
                print("Trop bas! " + give_hint(guess, number_to_guess))
            elif guess > number_to_guess:
                print("Trop haut! " + give_hint(guess, number_to_guess))
            else:
                end_time = time.time()
                elapsed_time = end_time - start_time
                minutes, seconds = divmod(elapsed_time, 60)
                print(f"Félicitations, {player_name}! Vous avez deviné le nombre en {attempts[player_name]} tentatives. Temps écoulé: {int(minutes)} minutes {int(seconds)} secondes")
                records.append({"name": player_name, "attempts": attempts[player_name], "time": elapsed_time, "difficulty": difficulty})
                records.sort(key=lambda x: (x['attempts'], x['time']))
                print("Nouveau record!")
                save_records(records)
                play_again = input("Voulez-vous jouer à nouveau? (oui/non): ")
                if play_again.lower() != 'oui':
                    print("Tableau de records:")
                    for record in records:
                        minutes, seconds = divmod(record['time'], 60)
                        print(f"{record['name']}: {record['attempts']} tentatives, {int(minutes)} minutes {int(seconds)} secondes, difficulté: {record['difficulty']}")
                    print("Merci d'avoir joué!")
                    return
                else:
                    if difficulty.lower() == 'facile':
                        number_to_guess = random.randint(1, 50)
                    elif difficulty.lower() == 'moyen':
                        number_to_guess = random.randint(1, 100)
                    elif difficulty.lower() == 'difficile':
                        number_to_guess = random.randint(1, 1000)
                    attempts = {player_name: 0 for player_name in player_names}

if __name__ == "__main__":
    game()
