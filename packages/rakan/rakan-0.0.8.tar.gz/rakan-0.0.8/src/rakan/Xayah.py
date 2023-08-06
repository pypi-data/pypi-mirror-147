import platform
import requests
from . import LowLevelErrors


class RiotAPI:
    """Class intended to handle the Riot Games Devloper API"""
    api_token: str
    """API token given by Riot Games."""

    def __init__(self, api_token: str) -> None:
        self.api_token = api_token

    def make_request(self, url: str):
        header_data = {
            'X-Riot-Token': self.api_token
        }
        response = requests.get(url=url, headers=header_data)
        match(int(response.status_code)):
            case 400:
                raise LowLevelErrors.BadRequest
            case 401:
                raise LowLevelErrors.Unauthorized
            case 403:
                raise LowLevelErrors.Forbidden
            case 404:
                raise LowLevelErrors.NotFound
            case 415:
                raise LowLevelErrors.UnsupportedMediaType
            case 429:
                raise LowLevelErrors.RateLimiExceeded
            case 500:
                raise LowLevelErrors.InternalServerError
            case 503:
                raise LowLevelErrors.ServiceUnavailable
            case 200:
                return response.json()
            case _:
                raise LowLevelErrors.UnknowError

    def get_matches_by_puuid(self, region: str, puuid: str, start_time: int, end_time: int, queque: int, type: str, start: int, count: int):
        url = f'https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?startTime={start_time}&endTime={end_time}&queue={queque}&type={type}&start={start}&count={count}'
        return self.make_request(url=url)

    def get_matches_by_match_id(self, region: str, match_id: str):
        url = f'https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}'
        return self.make_request(url=url)

    def get_match_timeline_by_match_id(self, region: str, match_id: str):
        url = f'https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}/timeline'
        return self.make_request(url=url)

    def get_champion_mastery_by_summoner_id(self, summoner_id: str, region: str):
        url = f'https://{region}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summoner_id}'
        return self.make_request(url=url)

    def get_champion_mastery_by_summoner_id_and_champion_id(self, summoner_id: str, champion_id: int, region: str):
        url = f'https://{region}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summoner_id}/by-champion/{champion_id}'
        return self.make_request(url=url)

    def get_summoner_mastery_score(self, summoner_id: str, region: str):
        url = f'https://{region}.api.riotgames.com/lol/champion-mastery/v4/scores/by-summoner/{summoner_id}'
        return self.make_request(url=url)

    def get_champion_rotation(self, region: str):
        url = f'https://{region}.api.riotgames.com/lol/platform/v3/champion-rotations'
        return self.make_request(url=url)

    def get_challenger_league(self, queque: str, region: str):
        url = f'https://{region}.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/{queque}'
        return self.make_request(url=url)

    def get_grandmaster_league(self, queque: str, region: str):
        url = f'https://{region}.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/{queque}'
        return self.make_request(url=url)

    def get_master_league(self, queque: str, region: str):
        url = f'https://{region}.api.riotgames.com/lol/league/v4/masterleagues/by-queue/{queque}'
        return self.make_request(url=url)

    def get_all_ranked_stats_by_summoner_id(self, summoner_id: str, region: str):
        url = f'https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}'
        return self.make_request(url=url)

    def get_all_summoners_by_division_tier_queque(self, region: str, division: str, tier: str, queque: str, page: int = 1):
        url = f'https://{region}.api.riotgames.com/lol/league/v4/entries/{queque}/{tier}/{division}?page={page}'
        return self.make_request(url=url)

    def get_server_status(self, region: str):
        url = f'https://{region}.api.riotgames.com/lol/status/v4/platform-data'
        return self.make_request(url=url)

    def get_in_game_info_by_summoner_id(self, summoner_id: str, region: str):
        url = f'https://{region}.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{summoner_id}'
        return self.make_request(url=url)

    def get_summoner_by_summoner_id(self, summoner_id: str, region: str):
        """
            A function that returns a JSON obj from [Riot Games API](https://developer.riotgames.com/apis#summoner-v4/GET_getBySummonerId) containing basic summoner information.\\
            It can raise every error in the Errors module.
            ### Arguments
                - The summoner's ID. [ string ]
                - The summoner's region. [ string ]
            ### Output
                Assuming no errors occured the function will return a json obj containing:
                - The account ID. [ string ] { accountId }
                - The profile icon ID. [ int ] { profileIconId }
                - The date of the last time the account was modified in epoch milliseconds. [ int ] { revisionDate }
                - The name of the summoner. [ sring ] { name }
                - The summoner's ID. [ string ] { id }
                - The summoner's PUUID. [ string ] { puuid }
                - The summoner's level. [ int ] { summonerLevel }
        """
        url = f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/{summoner_id}'
        return self.make_request(url=url)

    def get_summoner_by_name(self, name: str, region: str):
        """
            A function that returns a JSON obj from [Riot Games API](https://developer.riotgames.com/apis#summoner-v4/GET_getBySummonerName) containing basic summoner information.\\
            It can raise every error in the Errors module.
            ### Arguments
                - The summoner's name. [ string ]
                - The summoner's region. [ string ]
            ### Output
                Assuming no errors occured the function will return a json obj containing:
                - The account ID. [ string ] { accountId }
                - The profile icon ID. [ int ] { profileIconId }
                - The date of the last time the account was modified in epoch milliseconds. [ int ] { revisionDate }
                - The name of the summoner. [ sring ] { name }
                - The summoner's ID. [ string ] { id }
                - The summoner's PUUID. [ string ] { puuid }
                - The summoner's level. [ int ] { summonerLevel }
        """
        url = f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}'
        return self.make_request(url=url)

    def get_summoner_by_puuid(self, puuid: str, region: str):
        """
            A function that returns a JSON obj from [Riot Games API](https://developer.riotgames.com/apis#summoner-v4/GET_getByPUUID) containing basic summoner information.\\
            It can raise every error in the Errors module.
            ### Arguments
                - The summoner's PUUID. [ string ]
                - The summoner's region. [ string ]
            ### Output
                Assuming no errors occured the function will return a json obj containing:
                - The account ID. [ string ] { accountId }
                - The profile icon ID. [ int ] { profileIconId }
                - The date of the last time the account was modified in epoch milliseconds. [ int ] { revisionDate }
                - The name of the summoner. [ sring ] { name }
                - The summoner's ID. [ string ] { id }
                - The summoner's PUUID. [ string ] { puuid }
                - The summoner's level. [ int ] { summonerLevel }
        """
        url = f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}'
        return self.make_request(url=url)

    def get_summoner_by_account_id(self, account_id: str, region: str):
        """
            A function that returns a JSON obj from [Riot Games API](https://developer.riotgames.com/apis#summoner-v4/GET_getByAccountId) containing basic summoner information.\\
            It can raise every error in the Errors module.
            ### Arguments
                - The summoner's account ID. [ string ]
                - The summoner's region. [ string ]
            ### Output
                Assuming no errors occured the function will return a json obj containing:
                - The account ID. [ string ] { accountId }
                - The profile icon ID. [ int ] { profileIconId }
                - The date of the last time the account was modified in epoch milliseconds. [ int ] { revisionDate }
                - The name of the summoner. [ sring ] { name }
                - The summoner's ID. [ string ] { id }
                - The summoner's PUUID. [ string ] { puuid }
                - The summoner's level. [ int ] { summonerLevel }
        """
        url = f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-account/{account_id}'
        return self.make_request(url=url)


class MMR_API:
    user_agent_string = f'{platform.system()}:rakan_python_package:0.0.8'

    def __init__(self) -> None:
        pass

    def get_summoner_mmr_info(self, region: str, summoner_name: str):
        url = f'https://{region}.whatismymmr.com/api/v1/summoner?name={summoner_name}'
        response = requests.get(url)
        return response
