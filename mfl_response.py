import re

class MFLResponse:
    """Class to manage MFL responses"""
    def __init__(self, mfl_response):
        self.mfl_response = mfl_response
        self.mfl_response_text = mfl_response.text

# TO DO what additional info a generic response has

class MFLLoginResponseCookie:
    """A non-data descriptor that returns a formatted MFL login request URL string"""
    
    # regex pattern to find cookie in response text
    regex_pattern = 'MFL_USER_ID="([^"]*)">OK'

    def __get__(self, obj, type):
        cookie =  re.search(self.regex_pattern, obj.mfl_response_text).group(1)
        
        if cookie is not None:
            return cookie
        else:
            print("Failed to retrieve cookie")
            return None

class MFLLoginResponse(MFLResponse):
    """Class to manage MFL login response"""

    cookie = MFLLoginResponseCookie()

    def __init__(self, mfl_response):
        super().__init__(mfl_response)
