import io
from game import Result, ChoiceFactory, BigBangGame
from game import Choice, Rock, Paper, Scissors, Lizard, Spock

class TestFactory():
    factory = ChoiceFactory()

    def test_factory(self):
        """ Tests the factory of choices """

        choice = self.factory.create("rock")
        assert choice.is_rock()
        choice = self.factory.create("Rock")
        assert choice.is_rock()

        choice = self.factory.create("paper")
        assert choice.is_paper()
        choice = self.factory.create("Paper")
        assert choice.is_paper()

        choice = self.factory.create("scissors")
        assert choice.is_scissors()
        choice = self.factory.create("Scissors")
        assert choice.is_scissors()

        choice = self.factory.create("lizard")
        assert choice.is_lizard()
        choice = self.factory.create("Lizard")
        assert choice.is_lizard()

        choice = self.factory.create("spock")
        assert choice.is_spock()
        choice = self.factory.create("Spock")
        assert choice.is_spock()

        choice = self.factory.create("invalid")
        assert choice is None

        choice = self.factory.create("")
        assert choice is None


    def create_test(self, choice1_str, choice2_str, expected_result):
        """ Creates a test for 2 choices given an epected result """
        choice1 = self.factory.create(choice1_str)
        choice2 = self.factory.create(choice2_str)
        if not expected_result:
            assert choice1 is None or choice2 is None
            return

        result = choice1.wins(choice2)
        assert result == expected_result

    def test_winning(self):
        """ Tests all the possible combinations for the
            different Choice classes and their wins() method.
        """
        self.create_test("", "", None)
        self.create_test("", "paper", None)
        self.create_test("paper", "", None)
        self.create_test("invalid", "paper", None)
        self.create_test("paper", "invalid", None)

        self.create_test("paper", "paper", Result.Tie)
        self.create_test("paper", "rock", Result.Won)
        self.create_test("paper", "scissors", Result.Lost)
        self.create_test("paper", "lizard", Result.Lost)
        self.create_test("paper", "spock", Result.Won)

        self.create_test("rock", "paper", Result.Lost)
        self.create_test("rock", "rock", Result.Tie)
        self.create_test("rock", "scissors", Result.Won)
        self.create_test("rock", "lizard", Result.Won)
        self.create_test("rock", "spock", Result.Lost)

        self.create_test("scissors", "paper", Result.Won)
        self.create_test("scissors", "rock", Result.Lost)
        self.create_test("scissors", "scissors", Result.Tie)
        self.create_test("scissors", "lizard", Result.Won)
        self.create_test("scissors", "spock", Result.Lost)

        self.create_test("lizard", "paper", Result.Won)
        self.create_test("lizard", "rock", Result.Lost)
        self.create_test("lizard", "scissors", Result.Lost)
        self.create_test("lizard", "lizard", Result.Tie)
        self.create_test("lizard", "spock", Result.Won)

        self.create_test("spock", "paper", Result.Lost)
        self.create_test("spock", "rock", Result.Won)
        self.create_test("spock", "scissors", Result.Won)
        self.create_test("spock", "lizard", Result.Lost)
        self.create_test("spock", "spock", Result.Tie)

class TestGame():
    game = BigBangGame()

    def setUp(self):
        """ Creates a new game at the beginning of every test """
        self.game = BigBangGame()

    def check_read_input(self, monkeypatch, choice_input: str, expected_result: str):
        """ Checks the read_input method given the choice_input in stdin.

            :param monkeypatch: it's used to pass stdin input
            :param choice_input: the choice of a player
            :param expected_result: the expected result of read_input method
        """
        monkeypatch.setattr('sys.stdin', io.StringIO(choice_input))
        assert self.game.read_input("Player") == expected_result

    def test_read_input(self, monkeypatch):
        """ Tests different inputs for read_input method """

        self.check_read_input(monkeypatch, "paper", "paper")
        self.check_read_input(monkeypatch, "Paper", "Paper")

        self.check_read_input(monkeypatch, "rock", "rock")
        self.check_read_input(monkeypatch, "Rock", "Rock")

        self.check_read_input(monkeypatch, "scissors", "scissors")
        self.check_read_input(monkeypatch, "Scissors", "Scissors")

        self.check_read_input(monkeypatch, "lizard", "lizard")
        self.check_read_input(monkeypatch, "Lizard", "Lizard")

        self.check_read_input(monkeypatch, "spock", "spock")
        self.check_read_input(monkeypatch, "Spock", "Spock")

        self.check_read_input(monkeypatch, "invalid", "")

        self.game.score1 = 2
        self.game.score2 = 3
        self.check_read_input(monkeypatch, "restart", "")
        assert self.game.score1 == 0
        assert self.game.score2 == 0

        self.check_read_input(monkeypatch, "score", "")

    def check_calculate_scores(self, choice1, choice2, expected_result,
        expected_score1, expected_score2):
        """ Checks the results of the calculate_scores method.

            :param choice1: the choice of the 1st player
            :param choice2: the choice of the 2nd player
            :param expected_result: the expected result of calculate_scores method
        """
        assert self.game.calculate_scores(choice1, choice2) == expected_result
        assert self.game.score1 == expected_score1
        assert self.game.score2 == expected_score2

    def test_calculate_scores(self):
        """ Tests check_calculate_scores method. Not all the possible
            combinations need to be checked here as they've been checked
            for the wins method, which is called in calculate_scores.
        """
        self.check_calculate_scores(Rock(), Rock(), True, 0, 0)

        self.check_calculate_scores(Rock(), Paper(), True, 0, 1)

        self.check_calculate_scores(Paper(), Scissors(), True, 0, 2)

        self.check_calculate_scores(Choice(), Paper(), False, 0, 2)

