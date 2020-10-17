from mfl_request import MFLRequest, MFLLoginRequest
from mfl_response import MFLResponse

class MyFantasyLeagueAPISession():

    host = "api.myfantasyleague.com"
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
        response = self.login_with_credentials(self.username, self.password, self.year)
        self.user_cookie = response.cookie
        #print(self.user_cookie)

    def login_with_credentials(self, username, password, year=None):       
        request = MFLLoginRequest(username=username, password=password, year=year)
        response = request.make_request()
        return response

