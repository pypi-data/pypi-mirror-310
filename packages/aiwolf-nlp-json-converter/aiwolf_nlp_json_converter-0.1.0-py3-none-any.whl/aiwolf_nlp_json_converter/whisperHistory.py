from __future__ import annotations

from aiwolf_nlp_common.protocol import CommunicationProtocol
from .talkHistory import talkHistoryConverter


class whisperHistoryConverter(talkHistoryConverter):
    @classmethod
    def get_whisper_history_list(cls, protocol: CommunicationProtocol) -> list:
        if protocol.is_whisper_hisotry_empty():
            return None

        return cls.get_communication_history(
            communication_history=protocol.talk_history
        )
