from iot.factories import PlayerFactory
from iot.integration.audio import AudioClient
from iot.models import Player


@PlayerFactory.set
class BuiltinPlayer(Player):

    def play(self, path: str) -> None:
        AudioClient.play(path)