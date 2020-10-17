from mfl_response import MFLLoginResponse
import requests

class MFLRequest:
    """Class to manage MFL requests""" 
    protocol=""
    host=""
    default_year=""

    def make_request(self):
        return requests.post(self.request_url, self.request_params)

class MFLLoginRequestUrl:
    """A non-data descriptor that returns a formatted MFL login request URL string"""
    def __get__(self, obj, type):
        return f"{obj.protocol}://{obj.host}/{obj.year}/{obj.request_type}" 

class MFLLoginRequestParams:
    """A non-data descriptor that returns MFL login request params as a dictionary"""
    def __get__(self, obj, type):
        return {'USERNAME' : obj.username, 'PASSWORD' : obj.password, 'XML' : 1}

class MFLLoginRequest(MFLRequest):
    """Class to manage MFL login requests"""
    request_type = "login"
    request_url = MFLLoginRequestUrl()
    request_params = MFLLoginRequestParams()

    def __init__(self, username, password, year = None):
        self.username = username
        self.password = password
        self.year = year if year is not None else MFLRequest.default_year

    def make_request(self):
        response = super().make_request()
        return MFLLoginResponse(response)
