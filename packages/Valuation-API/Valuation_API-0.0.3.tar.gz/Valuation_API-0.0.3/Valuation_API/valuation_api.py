import requests

BASE_URL = 'https://api-valorizacion.lvaindices.com/graphql'

class ConnectionAPILVA:

    access_token = None
    refresh_token = None

    def __init__(self):
        pass
    
    def api_connection(self, user, password):
        "Return an authenticate code"
        query = f"""mutation {{
            auth(password: "{password}", user: "{user}") {{
                accessToken
                refreshToken
                }}
            }}
        """
        response = requests.post(url = BASE_URL, json = {'query': query})

        if "errors" in response.json():
            print(response.json())
            raise Exception("Incorrect credentials")
        self.access_token = response.json().get('data',{}).get('auth',{}).get('accessToken',None)
        self.refresh_token = response.json().get('data',{}).get('auth',{}).get('refreshToken',None)

    def refresh_ID_token(self):
        "Refresh an authenticate code"
        query = f"""mutation {{
            refresh(refreshToken: "{self.refresh_token}") {{
                accessToken
                refreshToken
                }}
            }}
        """
        response = requests.post(url = BASE_URL, json = {'query': query})

        self.access_token = response.json().get('data',{}).get('refresh',{}).get('accessToken',None)
        self.refresh_token = response.json().get('data',{}).get('refresh',{}).get('refreshToken',None)

    def request_data(self, query):

        headers = {'Authorization': f'Bearer {self.access_token}'}
        r = requests.post(url = BASE_URL, json = {'query': query}, headers=headers)
        #If the token expired, we get a new token and run the query again
        if "errors" in r.json():
                if "INVALID_ID_TOKEN" in r.json()["errors"][0]["message"]:
                    self.refresh_ID_token()
                    headers = {'Authorization': f'Bearer {self.access_token}'}
                    r = requests.post(url = BASE_URL, json = {'query': query}, headers=headers)

        return r.json()
