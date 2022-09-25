import unittest


from iot import Terminal


class TerminalTest(unittest.TestCase):

    def setUp(self) -> None:
        Terminal.load_models('iot')

    def test_before(self):
        Terminal.run()

