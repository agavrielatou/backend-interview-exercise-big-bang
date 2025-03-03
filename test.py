import io
from game import Result, ChoiceFactory, BigBangGame

class Testing():
    factory = ChoiceFactory()

    def test_factory(self):
        choice = self.factory.create("rock")
        assert choice.is_rock()

        choice = self.factory.create("paper")
        assert choice.is_paper()

        choice = self.factory.create("scissors")
        assert choice.is_scissors()

        choice = self.factory.create("lizard")
        assert choice.is_lizard()

        choice = self.factory.create("spock")
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

    def test_game(self, monkeypatch):
        """ Tests different inputs for read_input method """

        monkeypatch.setattr('sys.stdin', io.StringIO('paper'))
        game = BigBangGame()
        assert game.read_input("Player") == "paper"

        monkeypatch.setattr('sys.stdin', io.StringIO('rock'))
        game = BigBangGame()
        assert game.read_input("Player") == "rock"

        monkeypatch.setattr('sys.stdin', io.StringIO('scissors'))
        game = BigBangGame()
        assert game.read_input("Player") == "scissors"

        monkeypatch.setattr('sys.stdin', io.StringIO('lizard'))
        game = BigBangGame()
        assert game.read_input("Player") == "lizard"

        monkeypatch.setattr('sys.stdin', io.StringIO('spock'))
        game = BigBangGame()
        assert game.read_input("Player") == "spock"

        monkeypatch.setattr('sys.stdin', io.StringIO('invalid'))
        game = BigBangGame()
        assert game.read_input("Player") == ""

        monkeypatch.setattr('sys.stdin', io.StringIO('restart'))
        game = BigBangGame()
        assert game.read_input("Player") == ""

        monkeypatch.setattr('sys.stdin', io.StringIO('score'))
        game = BigBangGame()
        assert game.read_input("Player") == ""

