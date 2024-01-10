from enum import Enum


class ClientProtocol(Enum):
    DATA = "0"
    PLAYERS_INFOS = "1"
    ERROR = "2"
    SUCCESS = "3"
    ACTION = "4"

    @staticmethod
    def is_valid(protocol):
        return protocol in [protocol.value for protocol in ClientProtocol]