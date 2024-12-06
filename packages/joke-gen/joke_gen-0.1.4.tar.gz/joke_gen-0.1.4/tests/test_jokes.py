import unittest
from joke_gen.jokes import JokeGenerator

class TestJokeGenerator(unittest.TestCase):
    def test_random_joke(self):
        joke_gen = JokeGenerator()
        self.assertIn(joke_gen.get_random_joke(), joke_gen.get_all_jokes())

    def test_add_joke(self):
        joke_gen = JokeGenerator()
        joke = "TEST JOKE!"
        joke_gen.add_joke(joke)
        self.assertIn(joke, joke_gen.get_all_jokes())

if __name__ == "__main__":
    unittest.main()
