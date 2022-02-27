import random
from timeit import default_timer as timer

_GAME_LIST_DIC = {
    1: 'Find the vega [bps] per tenor',
    2: 'Calculate Break Evens',
    3: 'Practic basis points',
    4: 'Practice basis points (advanced)',
    5: 'Convert Notionals to Vegas'
}

_TENOR_CHOICES = ["O/N", "1-week", "1-month", "3-months", "6-months", "1-year"]
_VEGAS_BPS_PER_TENOR = [2, 5, 10, 20, 28, 40]


def vega_bps_game() -> str:
    random_index = random.randint(0, len(_TENOR_CHOICES) - 1)
    tenor_vega = _TENOR_CHOICES[random_index]
    correct_vega = _VEGAS_BPS_PER_TENOR[random_index]

    while True:
        try:
            user_reply_vega = input("What is the vega in bps for {}? ".format(tenor_vega))

            # Check if input is to stop the game. Otherwise try to parse the input.
            if user_reply_vega.lower() == "stop":
                return "stop"

            if user_reply_vega.lower() == "exit":
                return "exit"

            user_reply_vega = int(user_reply_vega)

            correct_or_wrong = "Correct" if correct_vega == user_reply_vega else "Wrong"
            computer_reply_vega = "{}! The vega for {} is {} bps.\n".format(
                correct_or_wrong,
                tenor_vega,
                correct_vega
            )
            print(computer_reply_vega)
        except ValueError:
            print("Invalid reply. Please try again.")
            continue
        break

    return "continue"


def calc_break_even() -> str:
    random_index = random.randint(0, len(_TENOR_CHOICES) - 1)
    tenor_vega = _TENOR_CHOICES[random_index]
    correct_vega = _VEGAS_BPS_PER_TENOR[random_index]
    vol = random.randint(30, 200)/10

    while True:
        try:
            msg = "The {tenor} vol is {vol}. What is the break-even? ".format(tenor=tenor_vega, vol=vol)
            start = timer()
            user_reply_be = input(msg)
            end = timer()

            # Check if input is to stop the game. Otherwise try to parse the input.
            if user_reply_be.lower() == "stop":
                return "stop"

            if user_reply_be.lower() == "exit":
                return "exit"

            # If not check the answer and print the reply
            user_reply_be = float(user_reply_be)
            time_lapsed = end - start
            correct_be = correct_vega * vol / 100 * 2
            diff_pct = (user_reply_be - correct_be) / correct_be * 100

            # Percentage threshold for a correct answer is 5%.
            msg_timer = "It took you {:.2f}s. \n".format(time_lapsed)
            if abs(diff_pct) < 2:
                print("Correct! The break-even is {:.2f}%. ".format(correct_be) + msg_timer)
            else:
                if diff_pct > 0:
                    diff_act = user_reply_be - correct_be
                    print("Yours! You were higher by {:.2f}%; the b/e is {:.2f}%. ".format(diff_act,
                                                                                           correct_be) + msg_timer)
                else:
                    diff_act = correct_be - user_reply_be
                    print("Mine! You were lower by {:.2f}%; the b/e is {:.2f}%. ".format(diff_act,
                                                                                         correct_be) + msg_timer)
        except ValueError:
            print("Invalid reply. Please try again.")
            continue
        break

    return "continue"


def get_random_notional() -> tuple:
    mill_mapping = {
        'K': 1000,
        'Mio': 1000000,
        'Bn': 1000000000
    }
    leading_number = random.randint(2, 19)/2
    mill_name = random.sample(mill_mapping.keys(), 1)[0]
    notional = leading_number*mill_mapping[mill_name]
    notional_print = "{} {}".format(leading_number, mill_name)

    return notional, notional_print


def practice_basis_points(basic=False) -> str:
    notional, notional_print = get_random_notional()
    bps = random.sample([1, 10, 100], k=1)[0] if basic else random.randint(1, 100)
    correct_number = bps/10000*notional

    while True:
        try:
            msg = "What is {bps} bps of {notional}? ".\
                format(bps=bps, notional=notional_print)
            start = timer()
            user_reply = input(msg)
            end = timer()

            # Check if input is to stop the game. Otherwise try to parse the input.
            if user_reply.lower() == "stop":
                return "stop"

            if user_reply.lower() == "exit":
                return "exit"

            # If not check the answer and print the reply
            user_reply = float(user_reply)
            time_lapsed = end - start

            # Percentage threshold for a correct answer is 5%.
            off_pct = abs(user_reply - correct_number)/correct_number*100
            correct_or_wrong = "Correct" if off_pct <= 10 else "Wrong"
            computer_reply = "{}! It's {:,.2f}. You were {:.1f}% off and it took you {:.2f}s. \n".format(
                correct_or_wrong,
                correct_number,
                off_pct,
                time_lapsed
            )
            print(computer_reply)
        except ValueError:
            print("Invalid reply. Please try again.")
            continue
        break

    return "continue"


def practice_basis_points_basic() -> str:
    return practice_basis_points(True)


def convert_notional_to_vega() -> str:
    notional, notional_print = get_random_notional()
    random_index = random.randint(0, len(_TENOR_CHOICES) - 1)
    tenor = _TENOR_CHOICES[random_index]
    correct_vega = _VEGAS_BPS_PER_TENOR[random_index]*notional/10000

    while True:
        try:
            msg = "What is the vega of a {tenor} vanilla option with notional {notional}? ".\
                format(tenor=tenor, notional=notional_print)
            start = timer()
            user_reply = input(msg)
            end = timer()

            # Check if input is to stop the game. Otherwise try to parse the input.
            if user_reply.lower() == "stop":
                return "stop"

            if user_reply.lower() == "exit":
                return "exit"

            # If not check the answer and print the reply
            user_reply = float(user_reply)
            time_lapsed = end - start

            # Percentage threshold for a correct answer is 5%.
            correct_or_wrong = "Correct" if correct_vega == user_reply else "Wrong"
            computer_reply = "{}! The vega is {:.2f}. It took you {:.2f}s. \n".format(
                correct_or_wrong,
                correct_vega,
                time_lapsed
            )
            print(computer_reply)
        except ValueError:
            print("Invalid reply. Please try again.")
            continue
        break

    return "continue"


def game_chooser_menu() -> int:
    while True:
        try:
            print("\nGames available: ")
            for item, amount in _GAME_LIST_DIC.items():
                print("  {}: {}.".format(item, amount))
            user_reply_be = input()

            game_input = int(user_reply_be)
            if game_input in _GAME_LIST_DIC:
                print("You are playing '{}'.".format(_GAME_LIST_DIC[game_input]))
                print("To return to the game selection mode type 'stop'.\n")
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
    3: practice_basis_points_basic,
    4: practice_basis_points,
    5: convert_notional_to_vega
}


def game_chooser(game_input: int) -> str:
    # Get the function from the switcher dictionary
    func = _GAME_LIST_FNS.get(game_input, lambda: "Invalid game function.")
    return func()


def play() -> None:
    game_input = game_chooser_menu()

    while True:
        game_output = game_chooser(game_input)

        if game_output == "stop":
            game_input = game_chooser_menu()
        elif game_output == "exit":
            return None


def main():
    play()


if __name__ == "__main__":
    main()
