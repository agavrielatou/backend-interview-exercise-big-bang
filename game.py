import os
import signal
import sys
from enum import Enum

class Result(Enum):
    """ Enum for the results of each game """
    Won = 1
    Lost = 2
    Tie = 3

class Choice:
    """ The base class for all the different
        types of user choices """

    def wins(self, opponent) -> Result:
        """ Decides if this player wins or not.

            :param Choice opponent: the choice of the other player.
            :return: the result for this player (Won, Lost, Tie).
        """
        pass

    def is_rock(self):
        """ Returns True if this choice is Rock. False otherwise """
        return False

    def is_paper(self):
        """ Returns True if this choice is Paper. False otherwise """
        return False

    def is_scissors(self):
        """ Returns True if this choice is Scissors. False otherwise """
        return False

    def is_lizard(self):
        """ Returns True if this choice is Lizard. False otherwise """
        return False

    def is_spock(self):
        """ Returns True if this choice is Spock. False otherwise """
        return False

class Rock(Choice):
    """ It's the Rock type of Choice """

    def is_rock(self):
        """ Returns True as the object is Rock type """
        return True

    def wins(self, opponent) -> Result:
        """ See base class """
        if opponent.is_rock():
            return Result.Tie
        if opponent.is_scissors() or \
            opponent.is_lizard():
            return Result.Won
        return Result.Lost

class Paper(Choice):
    """ It's the Paper type of Choice """

    def is_paper(self):
        """ Returns True as the object is Paper type """
        return True

    def wins(self, opponent) -> Result:
        """ See base class """
        if opponent.is_paper():
            return Result.Tie
        if opponent.is_rock() or \
            opponent.is_spock():
            return Result.Won
        return Result.Lost

class Scissors(Choice):
    """ It's the Scissors type of Choice """

    def is_scissors(self):
        """ Returns True as the object is Scissors type """
        return True

    def wins(self, opponent) -> Result:
        """ See base class """
        if opponent.is_scissors():
            return Result.Tie
        if opponent.is_paper() or \
            opponent.is_lizard():
            return Result.Won
        return Result.Lost

class Lizard(Choice):
    """ It's the Lizard type of Choice """

    def is_lizard(self):
        """ Returns True as the object is Lizard type """
        return True

    def wins(self, opponent) -> Result:
        """ See base class """
        if opponent.is_lizard():
            return Result.Tie
        if opponent.is_paper() or \
            opponent.is_spock():
            return Result.Won
        return Result.Lost

class Spock(Choice):
    """ It's the Spock type of Choice """

    def is_spock(self):
        """ Returns True as the object is Spock type """
        return True

    def wins(self, opponent) -> Result:
        """ See base class """
        if opponent.is_spock():
            return Result.Tie
        if opponent.is_scissors() or \
            opponent.is_rock():
            return Result.Won
        return Result.Lost

class ChoiceFactory:
    """ Factory that creates the right object
        based on the user's choice """

    def create(self, choice: str) -> Choice:
        """ Creates the right Choice object based
            on the given choice_str.

            :param choice: The user's choice.
            :return: the right Choice object based on
                    the given choice_str.
        """
        match choice:
            case "Rock" | "rock":
                return Rock()
            case "Paper" | "paper":
                return Paper()
            case "Scissors" | "scissors":
                return Scissors()
            case "Lizard" | "lizard":
                return Lizard()
            case "Spock" | "spock":
                return Spock()
            case _:
                return None

class BigBangGame:
    """ The big bang game class """

    # Score for player1
    score1 = 0
    # Score for player2
    score2 = 0

    def read_input(self, player_num: str) -> str:
        """ Reads the stdin input.

            :return: The given choice string if input was
                     valid. Empty string otherwise.
        """
        prompt = player_num + " choice (paper, rock, scissors, lizard, spock, restart, score): "
        choice = input(prompt)

        if "restart" == choice:
            self.score1 = 0
            self.score2 = 0
            print("\nRestarting game\n")
            return ""

        if "score" == choice:
            self.print_score()
            return ""

        print("CHOICE: ", choice)
        if choice != "paper" and \
            choice != "rock" and \
            choice != "scissors" and \
            choice != "lizard" and \
            choice != "spock":
            print("Invalid choice. Try again.\n")
            return ""

        return choice

    def play(self):
        """ Plays the game """

        # Handle SIGINT, so the program can exit gracefull
        # when Ctrl-C is given.
        signal.signal(signal.SIGINT, signal_handler)

        factory = ChoiceFactory()
        while True:
            choice1_str = self.read_input("Player1")
            if not choice1_str:
                continue
            choice2_str = self.read_input("Player2")
            if not choice2_str:
                continue

            choice1 = factory.create(choice1_str)
            choice2 = factory.create(choice2_str)
            if choice1 is None or choice2 is None:
                continue

            result = choice1.wins(choice2)
            match result:
                case Result.Tie:
                    print("It's a tie")
                    self.score1 += 1
                    self.score2 += 1
                case Result.Won:
                    print("Player1 won")
                    self.score1 += 1
                case Result.Lost:
                    print("Player2 won")
                    self.score2 += 1
                case _:
                    print("Invalid result. Shouldn't get here")
                    break
            self.print_score()

    def print_score(self):
        print("\nScore: [Player1:", self.score1, "- Player2:",self.score2,"]\n")

def signal_handler(sig, frame):
    """ Handles a signal, so it can exit gracefully """
    print("")
    sys.exit(0)

def main():
    game = BigBangGame()
    game.play()

if __name__ == '__main__':
    main()
