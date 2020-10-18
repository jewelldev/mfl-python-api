import re
import dict_digger

### MFLResponse ###############################################################

class MFLResponse:
    """Class to manage MFL responses"""
    def __init__(self, response):
        self.raw_response = response
        self.text = response.text
        self.status_code = response.status_code
        # TO DO this should be a descriptor 

# TO DO what additional info a generic response has

##############################################################################

### MFLExportResponse ########################################################

class MFLExportResponse(MFLResponse):
    """Class to manage MFL Export responses"""
    def __init__(self, response):
        self.json_response = response.json()
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