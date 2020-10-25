import re
import dict_digger

### MFLResponse ###############################################################

class ResponseDescriptor():
    """Non-data descriptor to retrieve nested values in instance's json_response"""
    def __init__(self, *path):
        self.path = path

    def __get__(self, obj, type):
        try:
            return dict_digger.dig(obj.json_response, *self.path, fail=True)
        except(IndexError, KeyError):
            raise AttributeError("Item not present in instance attribute 'json_response'")

class ResponseJsonDescriptor():
    """Non-data descriptor to retrieve JSON object from the instance's raw_response 
        (if the raw_response was written in JSON format, if not it returns an empty dict)
    """
    def __get__(self, obj, type):
        try:
            return obj.raw_response.json()
        except:
            return {}

class ResponseStatusCodeDescriptor():
    """Non-data descriptor to retrieve status code from the instance's raw_response 
        that indicates the status of the response (200 is OK, 404 is Not Found)
    """
    def __get__(self, obj, type):
        return obj.raw_response.status_code

class MFLResponse:
    """Class to manage MFL responses"""

    json_response = ResponseJsonDescriptor()
    status_code = ResponseStatusCodeDescriptor()

    def __init__(self, response):
        """Init MFLResponse class
        
        Args:
            raw_response: requests.Response() Object contains the server's response to the HTTP request.

        """
        self.raw_response = response

##############################################################################

### MFLExportResponse ########################################################

class MFLExportResponse(MFLResponse):
    """Class to manage MFL Export responses"""
    def __init__(self, response):
        try:
            response.json()
        except(AttributeError):
            raise ValueError("response is not valid JSON")

        super().__init__(response)

##############################################################################

#### MFLRostersResponse ######################################################

class RostersResponseDescriptor():
    
    def __get__(self, obj, type):
        
        rosters_json_raw = dict_digger.dig(obj.json_response, 'rosters', 'franchise')

        franchise_dict = {}
        for franchise in rosters_json_raw:
            
            player_dict = {}
            for player in franchise['player']:
                player_dict[ player['id'] ] = { 'status' : player['status'], 'salary' : player['salary'] }

            franchise_dict[ franchise['id'] ] = { 'week' :  franchise['week'], 'players' : player_dict }

        return franchise_dict


class MFLRostersResponse(MFLExportResponse):
    
    rosters = RostersResponseDescriptor() 
    week = ResponseDescriptor('rosters', 'franchise', 0, 'week')
    
    def __init__(self, response):
        super().__init__(response)

##############################################################################

#### MFLPlayersResponse ######################################################

class PlayersResponseDescriptor():
    
    def __get__(self, obj, type):
        
        players_json_raw = dict_digger.dig(obj.json_response, 'players', 'player')

        # TO DO handle this better
        if players_json_raw is None:
            return {}

        player_dict = {}
        for player in players_json_raw:

            player_dict[ player['id'] ] = { 'name' :  player['name'], 
                                            'position' : player['position'], 
                                            'team' : player['team'],
                                            'status' : player.get('status', '') }

        return player_dict


class MFLPlayersResponse(MFLExportResponse):
    
    players = PlayersResponseDescriptor() 
    timestamp = ResponseDescriptor('players', 'timestamp')

    def __init__(self, response):
        super().__init__(response)

##############################################################################

#### MFLLeagueResponse #######################################################

class FranchisesResponseDescriptor():
    
    def __get__(self, obj, type):
        
        franchises_json_raw = dict_digger.dig(obj.json_response, 'league', 'franchises', 'franchise')

        franchise_dict = {}
        for franchise in franchises_json_raw:
            
            franchise_id = franchise['id']
            franchise_dict[franchise_id] = {}
            for key in franchise:
                if(key is not 'id'):
                    franchise_dict[franchise_id][key] = franchise[key]

        return franchise_dict


class MFLLeagueResponse(MFLExportResponse):
    
    franchises = FranchisesResponseDescriptor() 
    
    def __init__(self, response):
        super().__init__(response)

##############################################################################

#### MFLLiveScoringResponse ##################################################

class FranchiseLiveScoringResponseDescriptor():
    
    def __get__(self, obj, type):
        
        matchups_raw_json = dict_digger.dig(obj.json_response, 'liveScoring', 'matchup')

        franchise_dict = {}
        for matchup in matchups_raw_json:

            franchise_pair_json = dict_digger.dig(matchup, 'franchise')
            #print(franchise_pair_json)
            for franchise in franchise_pair_json:
                players = dict_digger.dig(franchise, 'players', 'player')
                player_dict = {}
                for player in players:

                    player_id = player['id']
                    player_dict[player_id] = {}
                    for key in player:
                        if(key is not 'id'):
                            player_dict[player_id][key] = player[key]

                franchise_dict[ franchise['id'] ] = { 'playersCurrentlyPlaying' : franchise['playersCurrentlyPlaying'], 
                                                        'isHome' : franchise['isHome'],
                                                        'gameSecondsRemaining' : franchise['gameSecondsRemaining'], 
                                                        'playersYetToPlay' : franchise['playersYetToPlay'], 
                                                        'score' : franchise['score'], 
                                                        'players' : player_dict }

        return franchise_dict


class MFLLiveScoringResponse(MFLExportResponse):
    
    franchise_live_scoring = FranchiseLiveScoringResponseDescriptor() 
    week = ResponseDescriptor('liveScoring', 'week')
    
    def __init__(self, response):
        super().__init__(response)

##############################################################################

#### MFLPlayerScoresResponse #################################################

class PlayerScoresResponseDescriptor():
    
    def __get__(self, obj, type):
        
        player_scores_json_raw = dict_digger.dig(obj.json_response, 'playerScores', 'playerScore')

        player_dict = {}
        for player in player_scores_json_raw:

            player_id = player['id']
            player_dict[player_id] = { 'isAvailable' : player['isAvailable'], 'score' : player['score'] }

        return player_dict

class MFLPlayerScoresResponse(MFLExportResponse):
    
    player_scores = PlayerScoresResponseDescriptor() 
    week = ResponseDescriptor('playerScores', 'week')

    def __init__(self, response):
        super().__init__(response)

##############################################################################

#### MFLLoginResponse ########################################################

class MFLLoginResponseCookie:
    """A non-data descriptor that returns a formatted MFL login request URL string"""
    
    # regex pattern to find cookie in response text
    regex_pattern = 'MFL_USER_ID="([^"]*)">OK'

    def __get__(self, obj, type):
        cookie =  re.search(self.regex_pattern, obj.text).group(1)
        
        if cookie is not None:
            return cookie
        else:
            print("Failed to retrieve cookie")
            return None

class MFLLoginResponse(MFLResponse):
    """Class to manage MFL login response"""

    cookie = MFLLoginResponseCookie()

    def __init__(self, response):
        super().__init__(response)

##############################################################################