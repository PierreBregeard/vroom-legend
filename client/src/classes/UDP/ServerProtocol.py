from enum import Enum


class ServerProtocol(Enum):
    REGISTER = "0"
    START_GAME = "1"
    SET_PLAYER_DATA = "2"
    ERROR = "3"

    @staticmethod
    def is_valid(protocol):
        return protocol in [protocol.value for protocol in ServerProtocol]
