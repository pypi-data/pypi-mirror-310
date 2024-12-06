from aiwolf_nlp_common.protocol import CommunicationProtocol
from aiwolf_nlp_json_converter.gameSetting import gameSettingConverter

def test_get_game_setting_dict(initialize_str, initialize_json) -> None:
    protocol = CommunicationProtocol.initialize_from_json(received_str=initialize_str)
    test_result = gameSettingConverter.get_game_setting_dict(protocol=protocol)

    assert test_result["responseTimeout"] * 1000 == initialize_json["setting"]["responseTimeout"]
    assert test_result["actionTimeout"] * 1000 == initialize_json["setting"]["actionTimeout"]
    assert test_result["maxTalk"] == initialize_json["setting"]["maxTalk"]