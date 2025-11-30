import unittest
import pygame
from buttons import Button, ButtonFactory, PlayAction, ExitAction

class FakeGame:
    def __init__(self):
        self.run = True

class TestButtons(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pygame.init()
        cls.font = pygame.font.SysFont(None, 30)
        cls.screen_size = (800, 600)
        cls.button_size = (200, 80)

    def test_button_creation(self):
        action = PlayAction()
        button = Button("Test", (100, 100), self.button_size, action, self.font)

        self.assertEqual(button.name, "Test")
        self.assertEqual(button.pos, (100, 100))
        self.assertEqual(button.size, self.button_size)
        self.assertFalse(button.active)

    def test_button_activate(self):
        game = FakeGame()
        action = ExitAction(game)
        button = Button("Exit", (100, 100), self.button_size, action, self.font)

        button.activate()
        self.assertFalse(game.run)   # deve aver cambiato lo stato del gioco

    def test_button_factory(self):
        factory = ButtonFactory(self.screen_size, self.button_size, self.font)
        action = PlayAction()

        button = factory.create_button("Play", 250, action)

        # deve essere centrato orizzontalmente
        expected_x = (self.screen_size[0] - self.button_size[0]) / 2
        self.assertEqual(button.pos[0], expected_x)
        self.assertEqual(button.pos[1], 250)

if __name__ == "__main__":
    unittest.main()
