from mfl_request import MFLRequest, MFLLoginRequest, MFLRostersRequest
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
        print(self.user_cookie + " " + str(response.status_code))

    def login_with_credentials(self, username, password):       
        request = MFLLoginRequest(username=username, password=password)
        response = request.make_request()
        return response

    def rosters(self, league_id=None, franchise=None, week=None):
        league_id = league_id if league_id is not None else self.league_id
        request = MFLRostersRequest(league_id, franchise, week)
        #print(request.request_url)
        #print(request.request_params)
        response = request.make_request()
        return response

