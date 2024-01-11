from enum import Enum


class ClientProtocol(Enum):
    DATA = "0"
    PLAYERS_INFOS = "1"
    ERROR = "2"
    ACTION = "3"
    PING = "4"
    INFO = "5"
    START_GAME = "6"

    @staticmethod
    def is_valid(protocol):
        return protocol in [protocol.value for protocol in ClientProtocol]
