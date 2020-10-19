from mfl_response import MFLLoginResponse, MFLRostersResponse, MFLPlayersResponse, MFLLeagueResponse
import requests

### MFLRequest ###############################################################

class MFLRequestUrl:
    """A non-data descriptor that returns a formatted MFL login request URL string"""
    def __get__(self, obj, type):
        if obj.request_base_type == "login":
            host = "api.myfantasyleague.com"
        else:
            host = obj.host
        return f"{obj.protocol}://{host}/{obj.default_year}/{obj.request_base_type}" 

class MFLRequest:
    """Class to manage MFL requests""" 
    protocol=""
    host=""
    default_year=""
    user_cookie=""
    request_url = MFLRequestUrl()

    def make_request(self):
        print(self.request_url)
        print(self.request_params)
        return requests.post(url=self.request_url, data=self.request_params, cookies={'MFL_USER_ID' : self.user_cookie})

##############################################################################

#### MFLExportRequest ########################################################

class MFLExportRequest(MFLRequest):
    """Class to manage MFL export requests"""
    request_base_type = "export"
    pass

##############################################################################

#### MFLRostersRequest #######################################################

class MFLRostersRequestParams:
    """A non-data descriptor that returns MFL rosters request params as a dictionary"""
    def __get__(self, obj, type):
        params = {'TYPE' : obj.request_type, 'L' : obj.league_id}
        if obj.franchise is not None:
            params['FRANCHISE'] = obj.franchise
        if obj.week is not None:
            params['W'] = obj.week
        params['JSON'] = obj.json
        return params

class MFLRostersRequest(MFLExportRequest):
    """Class to manage MFL rosters request"""
    request_type = "rosters"
    request_params = MFLRostersRequestParams()

    def __init__(self, league_id, franchise=None, week=None):
        self.league_id = league_id
        self.franchise = franchise
        self.week = week
        self.json = 1

    def make_request(self):
        response = super().make_request()
        return MFLRostersResponse(response)

##############################################################################

#### MFLPlayersRequest #######################################################

class MFLPlayersRequestParams:
    """A non-data descriptor that returns MFL players request params as a dictionary"""
    def __get__(self, obj, type):
        params = {'TYPE' : obj.request_type}
        if obj.league_id is not None:
            params['L'] = obj.league_id
        if obj.details is not None:
            params['DETAILS'] = obj.details
        if obj.since is not None:
            params['SINCE'] = obj.since
        if obj.players is not None:
            params['PLAYERS'] = obj.players
        params['JSON'] = obj.json
        return params

class MFLPlayersRequest(MFLExportRequest):
    """Class to manage MFL players request"""
    request_type = "players"
    request_params = MFLPlayersRequestParams()

    def __init__(self, league_id=None, details=None, since=None, players=None):
        self.league_id = league_id
        self.details = details
        self.since = since
        self.players = players
        self.json = 1

    def make_request(self):
        response = super().make_request()
        return MFLPlayersResponse(response)

##############################################################################

#### MFLLeagueRequest ########################################################

class MFLLeagueRequestParams:
    """A non-data descriptor that returns MFL league request params as a dictionary"""
    def __get__(self, obj, type):
        params = {'TYPE' : obj.request_type, 'L' : obj.league_id, 'JSON' : obj.json}
        return params

class MFLLeagueRequest(MFLExportRequest):
    """Class to manage MFL league request"""
    request_type = "league"
    request_params = MFLLeagueRequestParams()

    def __init__(self, league_id):
        self.league_id = league_id
        self.json = 1

    def make_request(self):
        response = super().make_request()
        return MFLLeagueResponse(response)

##############################################################################

### MFLLoginRequest ##########################################################

class MFLLoginRequestParams:
    """A non-data descriptor that returns MFL login request params as a dictionary"""
    def __get__(self, obj, type):
        return {'USERNAME' : obj.username, 'PASSWORD' : obj.password, 'XML' : 1}

class MFLLoginRequest(MFLRequest):
    """Class to manage MFL login requests"""
    request_base_type = "login"
    request_params = MFLLoginRequestParams()

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def make_request(self):
        response = super().make_request()
        return MFLLoginResponse(response)

##############################################################################

