from common import WebSocketEventResponse

event = WebSocketEventResponse(
    type="UPDATE",
    uri="/lol-champ-select/v1/session",
    data={
        "actions": [
            [
                {
                    "actorCellId": 0,
                    "championId": 0,
                    "completed": False,
                    "id": 0,
                    "isAllyAction": True,
                    "isInProgress": True,
                    "type": "ban",
                },
                {
                    "actorCellId": 1,
                    "championId": 0,
                    "completed": False,
                    "id": 1,
                    "isAllyAction": True,
                    "isInProgress": True,
                    "type": "ban",
                },
                {
                    "actorCellId": 2,
                    "championId": 0,
                    "completed": False,
                    "id": 2,
                    "isAllyAction": True,
                    "isInProgress": True,
                    "type": "ban",
                },
                {
                    "actorCellId": 3,
                    "championId": 0,
                    "completed": False,
                    "id": 3,
                    "isAllyAction": True,
                    "isInProgress": True,
                    "type": "ban",
                },
                {
                    "actorCellId": 4,
                    "championId": 0,
                    "completed": False,
                    "id": 4,
                    "isAllyAction": True,
                    "isInProgress": True,
                    "type": "ban",
                },
                {
                    "actorCellId": 5,
                    "championId": 0,
                    "completed": False,
                    "id": 5,
                    "isAllyAction": False,
                    "isInProgress": True,
                    "type": "ban",
                },
                {
                    "actorCellId": 6,
                    "championId": 0,
                    "completed": False,
                    "id": 6,
                    "isAllyAction": False,
                    "isInProgress": True,
                    "type": "ban",
                },
                {
                    "actorCellId": 7,
                    "championId": 0,
                    "completed": False,
                    "id": 7,
                    "isAllyAction": False,
                    "isInProgress": True,
                    "type": "ban",
                },
                {
                    "actorCellId": 8,
                    "championId": 0,
                    "completed": False,
                    "id": 8,
                    "isAllyAction": False,
                    "isInProgress": True,
                    "type": "ban",
                },
                {
                    "actorCellId": 9,
                    "championId": 0,
                    "completed": False,
                    "id": 9,
                    "isAllyAction": False,
                    "isInProgress": True,
                    "type": "ban",
                },
            ],
            [
                {
                    "actorCellId": -1,
                    "championId": 0,
                    "completed": False,
                    "id": 100,
                    "isAllyAction": False,
                    "isInProgress": False,
                    "type": "ten_bans_reveal",
                }
            ],
            [
                {
                    "actorCellId": 0,
                    "championId": 0,
                    "completed": False,
                    "id": 10,
                    "isAllyAction": True,
                    "isInProgress": False,
                    "type": "pick",
                }
            ],
            [
                {
                    "actorCellId": 5,
                    "championId": 0,
                    "completed": False,
                    "id": 11,
                    "isAllyAction": False,
                    "isInProgress": False,
                    "type": "pick",
                },
                {
                    "actorCellId": 6,
                    "championId": 0,
                    "completed": False,
                    "id": 12,
                    "isAllyAction": False,
                    "isInProgress": False,
                    "type": "pick",
                },
            ],
            [
                {
                    "actorCellId": 1,
                    "championId": 0,
                    "completed": False,
                    "id": 13,
                    "isAllyAction": True,
                    "isInProgress": False,
                    "type": "pick",
                },
                {
                    "actorCellId": 2,
                    "championId": 0,
                    "completed": False,
                    "id": 14,
                    "isAllyAction": True,
                    "isInProgress": False,
                    "type": "pick",
                },
            ],
            [
                {
                    "actorCellId": 7,
                    "championId": 0,
                    "completed": False,
                    "id": 15,
                    "isAllyAction": False,
                    "isInProgress": False,
                    "type": "pick",
                },
                {
                    "actorCellId": 8,
                    "championId": 0,
                    "completed": False,
                    "id": 16,
                    "isAllyAction": False,
                    "isInProgress": False,
                    "type": "pick",
                },
            ],
            [
                {
                    "actorCellId": 3,
                    "championId": 0,
                    "completed": False,
                    "id": 17,
                    "isAllyAction": True,
                    "isInProgress": True,
                    "type": "pick",
                },
                {
                    "actorCellId": 4,
                    "championId": 517,
                    "completed": False,
                    "id": 18,
                    "isAllyAction": True,
                    "isInProgress": False,
                    "type": "pick",
                },
            ],
            [
                {
                    "actorCellId": 9,
                    "championId": 0,
                    "completed": False,
                    "id": 19,
                    "isAllyAction": False,
                    "isInProgress": False,
                    "type": "pick",
                }
            ],
        ],
        "allowBattleBoost": False,
        "allowDuplicatePicks": False,
        "allowLockedEvents": False,
        "allowRerolling": False,
        "allowSkinSelection": True,
        "bans": {"myTeamBans": [], "numBans": 0, "theirTeamBans": []},
        "benchChampionIds": [],
        "benchEnabled": False,
        "boostableSkinCount": 0,
        "chatDetails": {
            "chatRoomName": "f4bd4d54-7843-4e59-954b-fb6752bde040@champ-select.pvp.net",
            "chatRoomPassword": None,
        },
        "counter": 5,
        "entitledFeatureState": {"additionalRerolls": 0, "unlockedSkinIds": []},
        "gameId": 309443568,
        "hasSimultaneousBans": True,
        "hasSimultaneousPicks": False,
        "isCustomGame": False,
        "isSpectating": False,
        "localPlayerCellId": 3,
        "lockedEventIndex": -1,
        "myTeam": [
            {
                "assignedPosition": "jungle",
                "cellId": 0,
                "championId": 0,
                "championPickIntent": 0,
                "entitledFeatureType": "NONE",
                "selectedSkinId": 0,
                "spell1Id": 4,
                "spell2Id": 11,
                "summonerId": 6311092,
                "team": 1,
                "wardSkinId": -1,
            },
            {
                "assignedPosition": "utility",
                "cellId": 1,
                "championId": 0,
                "championPickIntent": 0,
                "entitledFeatureType": "NONE",
                "selectedSkinId": 0,
                "spell1Id": 14,
                "spell2Id": 4,
                "summonerId": 2577624311440800,
                "team": 1,
                "wardSkinId": -1,
            },
            {
                "assignedPosition": "bottom",
                "cellId": 2,
                "championId": 0,
                "championPickIntent": 0,
                "entitledFeatureType": "NONE",
                "selectedSkinId": 0,
                "spell1Id": 7,
                "spell2Id": 4,
                "summonerId": 23601342,
                "team": 1,
                "wardSkinId": -1,
            },
            {
                "assignedPosition": "top",
                "cellId": 3,
                "championId": 0,
                "championPickIntent": 0,
                "entitledFeatureType": "NONE",
                "selectedSkinId": 0,
                "spell1Id": 12,
                "spell2Id": 4,
                "summonerId": 2592564405913376,
                "team": 1,
                "wardSkinId": 1,
            },
            {
                "assignedPosition": "middle",
                "cellId": 4,
                "championId": 0,
                "championPickIntent": 517,
                "entitledFeatureType": "NONE",
                "selectedSkinId": 0,
                "spell1Id": 4,
                "spell2Id": 14,
                "summonerId": 24481617,
                "team": 1,
                "wardSkinId": -1,
            },
        ],
        "rerollsRemaining": 0,
        "skipChampionSelect": False,
        "theirTeam": [
            {
                "assignedPosition": "",
                "cellId": 5,
                "championId": 0,
                "championPickIntent": 0,
                "entitledFeatureType": "",
                "selectedSkinId": 0,
                "spell1Id": 0,
                "spell2Id": 0,
                "summonerId": 0,
                "team": 2,
                "wardSkinId": -1,
            },
            {
                "assignedPosition": "",
                "cellId": 6,
                "championId": 0,
                "championPickIntent": 0,
                "entitledFeatureType": "",
                "selectedSkinId": 0,
                "spell1Id": 0,
                "spell2Id": 0,
                "summonerId": 0,
                "team": 2,
                "wardSkinId": -1,
            },
            {
                "assignedPosition": "",
                "cellId": 7,
                "championId": 0,
                "championPickIntent": 0,
                "entitledFeatureType": "",
                "selectedSkinId": 0,
                "spell1Id": 0,
                "spell2Id": 0,
                "summonerId": 0,
                "team": 2,
                "wardSkinId": -1,
            },
            {
                "assignedPosition": "",
                "cellId": 8,
                "championId": 0,
                "championPickIntent": 0,
                "entitledFeatureType": "",
                "selectedSkinId": 0,
                "spell1Id": 0,
                "spell2Id": 0,
                "summonerId": 0,
                "team": 2,
                "wardSkinId": -1,
            },
            {
                "assignedPosition": "",
                "cellId": 9,
                "championId": 0,
                "championPickIntent": 0,
                "entitledFeatureType": "",
                "selectedSkinId": 0,
                "spell1Id": 0,
                "spell2Id": 0,
                "summonerId": 0,
                "team": 2,
                "wardSkinId": -1,
            },
        ],
        "timer": {
            "adjustedTimeLeftInPhase": 13754,
            "internalNowInEpochMs": 1623513734596,
            "isInfinite": False,
            "phase": "BAN_PICK",
            "totalTimeInPhase": 24000,
        },
        "trades": [],
    },
)
