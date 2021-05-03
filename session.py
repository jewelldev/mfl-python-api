'''
session.py

MyFantasyLeagueAPISession object

'''

from mfl_request import MFLRequest, MFLLoginRequest, MFLRostersRequest, MFLPlayersRequest, MFLLeagueRequest, MFLLiveScoringRequest, MFLPlayerScoresRequest
from mfl_response import MFLResponse
import json

class MyFantasyLeagueAPISession():
    """The summary line for a class docstring should fit on one line.

    If the class has public attributes, they may be documented here
    in an ``Attributes`` section and follow the same formatting as a
    function's ``Args`` section. Alternatively, attributes may be documented
    inline with the attribute's declaration (see __init__ method below).

    Properties created with the ``@property`` decorator should be documented
    in the property's getter method.

    Attributes:
        attr1 (str): Description of `attr1`.
        attr2 (:obj:`int`, optional): Description of `attr2`.

    """
    host = "www67.myfantasyleague.com"
    protocol = "https"

    def __init__(self, year, league_id="", username="", password=""):
        """Example of docstring on the __init__ method.

        The __init__ method may be documented in either the class level
        docstring, or as a docstring on the __init__ method itself.

        Either form is acceptable, but the two should not be mixed. Choose one
        convention to document the __init__ method and be consistent with it.

        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            param1 (str): Description of `param1`.
            param2 (:obj:`int`, optional): Description of `param2`. Multiple
                lines are supported.
            param3 (:obj:`list` of :obj:`str`): Description of `param3`.

        """
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

    def rosters(self, league_id: str=None, franchise: int=None, week: int=None) -> MFLResponse:
        """The current rosters for all franchises in a league, including player status (active roster, IR, TS), 
        as well as all salary/contract information for that player.
    
        Args:
            league_id: League Id
            franchise: When set, the response will include the current roster of just the specified franchise.
            week: If the week is specified, it returns the roster for that week. The week must be less than or 
                    equal to the upcoming week. Changes to salary and contract info is not tracked so those fields (if used) 
                    always show the current values.

        Returns:
            MFLRostersResponse
        """
        league_id = league_id if league_id is not None else self.league_id
        
        request = MFLRostersRequest(league_id, franchise, week)
        response = request.make_request()
        return response

    def players(self, league_id: str=None, details: bool=False, since: int=None, players: str=None) -> MFLResponse:
        """All player IDs, names and positions that MyFantasyLeague.com has in database for the current year. 
        
        Args:
            league_id: League Id
            details: Set this value to True to return complete player details, including player IDs from other sources.
            since: Pass a unix timestamp via this parameter to receive only changes to the player database since that time.
            players: Pass a list of player ids separated by commas (or just a single player id) to receive back just the info on those players.
        
        Returns: 
            MFLPlayersResponse
        """
        league_id = league_id if league_id is not None else self.league_id
        
        request = MFLPlayersRequest(league_id, details, since, players)
        response = request.make_request()
        return response

    def league(self, league_id: str=None) -> MFLResponse:
        """General league setup parameters for a given league, including: league name, roster size, IR/TS size, starting and ending week, 
        starting lineup requirements, franchise names, division names, and more. If you pass the cookie of a user with commissioner access, 
        it will return otherwise private owner information, like owner names, email addresses, etc.
        Private league access restricted to league owners.
        Personal user information, like name and email addresses only returned to league owners.

        Args:
            league_id: League Id
        
        Returns:
            MFLLeagueResponse
        
        """
        league_id = league_id if league_id is not None else self.league_id
        
        request = MFLLeagueRequest(league_id)
        response = request.make_request()
        return response     

    def live_scoring(self, league_id: str=None, week: int=None, details: bool=False) -> MFLResponse:
        """Live scoring for a given league and week, including each franchise's current score, 
        how many game seconds remaining that franchise has, players who have yet to play, 
        and players who are currently playing.
        
        Args:
            league_id: League Id
            week: If the week is specified, it returns the data for that week, 
                    otherwise the most current data is returned.
            details: Setting this argument to True will return data for non-starters as well.

        Returns:
            MFLLiveScoringResponse

        """
        league_id = league_id if league_id is not None else self.league_id
        
        request = MFLLiveScoringRequest(league_id, week, details)
        response = request.make_request()
        return response

    def player_scores(self, league_id: str=None, week: int=None, year: int=None, players: str=None, status: str=None, rules: bool=False, count: int=None) -> MFLResponse:
        """All player scores for a given league/week, including all rostered players as well as all free agents

        Args:
            league_id: League Id
            week: If the week is specified, it returns the data for that week, otherwise the 
                    current week data is returned. If the value is 'YTD', then it returns year-to-date 
                    data. If the value is 'AVG', then it returns a weekly average.
            year: The year for the data to be returned. Default is year set in instance of MyFantasyLeagueAPISession
            players: Pass a list of player ids separated by commas (or just a single player id) 
                    to receive back just the info on those players.
            position: Return only players from this position.
            status: If set to 'freeagent', returns only players that are fantasy league free agents.
            rules: If set, and a league id passed, it re-calculates the fantasy score for each player according to 
                    that league's rules. This is only valid when specifying the current year and current week.
            count: Limit the result to this many players.
        
        Returns:
            MFLPlayerScoresResponse

        """

        league_id = league_id if league_id is not None else self.league_id
        year = year if year is not None else self.year

        # TO DO when specifying players this breaks
        request = MFLPlayerScoresRequest(league_id, week, year, players, status, rules, count)
        response = request.make_request()
        return response

#TO DO debug raw response option
#TO DO error checking and exception handling