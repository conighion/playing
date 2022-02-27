import random
from timeit import default_timer as timer

_GAME_LIST_DIC = {
    1: 'Find the vega [bps] per tenor',
    2: 'Calculate Break Evens',
    3: 'Convert Vegas to Notionals',
    4: 'Convert Notionals to Vegas'
}

_TENOR_CHOICES = ["O/N", "1-week", "1-month", "3-months", "6-months", "1-year"]
_VEGAS_BPS_PER_TENOR = [2, 5, 10, 20, 28, 40]


def vega_bps_game() -> str:
    random_index = random.randint(0, len(_TENOR_CHOICES) - 1)
    tenor_vega = _TENOR_CHOICES[random_index]
    correct_vega = _VEGAS_BPS_PER_TENOR[random_index]

    while True:
        try:
            user_reply_vega = input("What is the vega in bps for {}?".format(tenor_vega))

            # Check if input is to stop the game. Otherwise try to parse the input.
            if user_reply_vega.lower() == "stop":
                return "stop"

            user_reply_vega = int(user_reply_vega)
        except ValueError:
            print("Invalid reply. Please try again.")
            continue
        break

    correct_or_wrong = "Correct" if correct_vega == user_reply_vega else "Wrong"
    computer_reply_vega = "{}! The vega for {} is {} bps.".format(
        correct_or_wrong,
        tenor_vega,
        correct_vega
    )
    print(computer_reply_vega)
    print("\n")

    return "continue"


def calc_break_even() -> str:
    random_index = random.randint(0, len(_TENOR_CHOICES) - 1)
    tenor_vega = _TENOR_CHOICES[random_index]
    correct_vega = _VEGAS_BPS_PER_TENOR[random_index]
    vol = random.randint(30, 200)/10

    start = timer()
    while True:
        try:
            msg = "The {tenor} vol is {vol}. What is the break-even?".format(tenor=tenor_vega, vol=vol)
            user_reply_be = input(msg)

            # Check if input is to stop the game. Otherwise try to parse the input.
            if user_reply_be.lower() == "stop":
                return "stop"

            user_reply_be = float(user_reply_be)
        except ValueError:
            print("Invalid reply. Please try again.")
            continue
        break

    end = timer()
    time_lapsed = end - start
    correct_be = correct_vega*vol/100*2
    diff_pct = (user_reply_be - correct_be)/correct_be*100

    # Percentage threshold for a correct answer is 5%.
    msg_timer = "It took you {:.2f}s.".format(time_lapsed)
    if abs(diff_pct) < 2:
        print("Correct! The break-even is {:.2f}%. ".format(correct_be) + msg_timer)
    else:
        if diff_pct > 0:
            diff_act = user_reply_be - correct_be
            print("Yours! You were higher by {:.2f}%; the b/e is {:.2f}%. ".format(diff_act, correct_be) + msg_timer)
        else:
            diff_act = correct_be - user_reply_be
            print("Mine! You were lower by {:.2f}%; the b/e is {:.2f}%. ".format(diff_act, correct_be) + msg_timer)

    # Add new line
    print("\n")
    return "continue"


def convert_vega_to_notional() -> str:
    return "continue"


def convert_notional_to_vega() -> str:
    return "continue"


def game_chooser_menu() -> int:
    print("Games available: ")
    for item, amount in _GAME_LIST_DIC.items():
        print("  {}: {}.".format(item, amount))

    while True:
        try:
            game_input = int(input())

            # Check if input is to stop the game. Otherwise try to parse the input.
            if game_input in _GAME_LIST_DIC:
                print("\nYou are playing '{}'.".format(_GAME_LIST_DIC[game_input]))
                print("To return to the game selection mode type 'stop'.")
                print("\n\n")
                return game_input
            else:
                print("Invalid game entry. Please try again.")
                continue

        except ValueError:
            print("Invalid reply. Please the number of one of the games above.")
            continue


_GAME_LIST_FNS = {
    1: vega_bps_game,
    2: calc_break_even,
    3: convert_vega_to_notional,
    4: convert_notional_to_vega
}


def game_chooser(game_input: int) -> str:
    # Get the§ function from switcher dictionary
    func = _GAME_LIST_FNS.get(game_input, lambda: "Invalid game function.")
    return func()


def play() -> None:
    game_input = game_chooser_menu()

    while True:

        game_output = game_chooser(game_input)

        if game_output == "stop":
            game_input = game_chooser_menu()
