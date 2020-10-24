from mfl_request import MFLRequest, MFLLoginRequest, MFLRostersRequest, MFLPlayersRequest, MFLLeagueRequest, MFLLiveScoringRequest
from mfl_response import MFLResponse

class MyFantasyLeagueAPISession():

    host = "www67.myfantasyleague.com"
    protocol = "https"

    def __init__(self, year, league_id="", username="", password=""):
        """"Initializes a new MyFantasyLeague API session"""
        self.year = year
        self.league_id = league_id
        self.username = username
        self.password = password
        self.user_cookie = ""

        '''Initialize MFLRequest class variables'''
        MFLRequest.host = self.host
        MFLRequest.protocol = self.protocol
        MFLRequest.default_year = self.year

    @classmethod
    def initalize_generic_session(cls, year):
        return cls(year)
        
    @classmethod
    def initialize_league_session(cls, year, league_id):
        return cls(year, league_id)

    @classmethod
    def initialize_authenticated_league_session(cls, year, league_id, username, password):
        new_instance = cls(year, league_id, username, password)
        new_instance.login()
        return new_instance

    def login(self):
        response = self.login_with_credentials(self.username, self.password)
        self.user_cookie = response.cookie
        MFLRequest.user_cookie = self.user_cookie
        print(self.user_cookie + " " + str(response.status_code))

    def login_with_credentials(self, username: str, password: str):       
        request = MFLLoginRequest(username=username, password=password)
        response = request.make_request()
        return response

    def rosters(self, league_id: str=None, franchise: int=None, week: int=None) -> dict:
        '''
        The current rosters for all franchises in a league, including player status (active roster, IR, TS), 
        as well as all salary/contract information for that player.

        :param league_id: League Id
        :param franchise: When set, the response will include the current roster of just the specified franchise.
        :param week: If the week is specified, it returns the roster for that week. The week must be less than or 
                equal to the upcoming week. Changes to salary and contract info is not tracked so those fields (if used) 
                always show the current values.
        :returns: rosters dict, where key is franchise ID
        '''
        league_id = league_id if league_id is not None else self.league_id
        request = MFLRostersRequest(league_id, franchise, week)
        response = request.make_request()
        return response.rosters

    def players(self, league_id: str=None, details: bool=False, since: int=None, players: str=None) -> dict:
        '''
        All player IDs, names and positions that MyFantasyLeague.com has in database for the current year. 

        :param league_id: League Id
        :param details: Set this value to True to return complete player details, including player IDs from other sources.
        :param since: Pass a unix timestamp via this parameter to receive only changes to the player database since that time.
        :param players: Pass a list of player ids separated by commas (or just a single player id) to receive back just the info on those players.
        :returns: players dict, where key is player ID
        '''
        league_id = league_id if league_id is not None else self.league_id
        request = MFLPlayersRequest(league_id, details, since, players)
        response = request.make_request()
        return response.players

    def franchises(self, league_id: str=None) -> dict:
        '''
        All franchise IDs, names and miscellaneous info.

        :param league_id: League Id
        :returns: franchise dict, where key is franchise ID
        '''
        league_id = league_id if league_id is not None else self.league_id
        request = MFLLeagueRequest(league_id)
        response = request.make_request()
        return response.franchises        

    def live_scoring(self, league_id: str=None, week: int=None, details: bool=False) -> dict:
        '''
            Live scoring for a given league and week, including each franchise's current score, 
            how many game seconds remaining that franchise has, players who have yet to play, 
            and players who are currently playing.

        :param league_id: League Id
        :param week: If the week is specified, it returns the data for that week, 
                otherwise the most current data is returned.
        :param details: Setting this argument to True will return data for non-starters as well.
        :returns: franchises dict, where key is franchise ID
        '''
        league_id = league_id if league_id is not None else self.league_id
        request = MFLLiveScoringRequest(league_id, week, details)
        response = request.make_request()
        return response.franchise_live_scoring

#TO DO debug raw response option