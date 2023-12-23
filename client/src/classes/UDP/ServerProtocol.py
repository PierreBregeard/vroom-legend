from enum import Enum


class ServerProtocol(Enum):
    REGISTER = "0"
    GET_PLAYERS_IDs = "1"
    START_GAME = "2"
    SET_PLAYER_DATA = "3"

    @staticmethod
    def is_valid(protocol):
        return protocol in [protocol.value for protocol in ServerProtocol]
