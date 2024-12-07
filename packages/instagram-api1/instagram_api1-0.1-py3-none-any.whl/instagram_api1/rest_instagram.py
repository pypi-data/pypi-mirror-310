import requests

class InstagramAPI:
    def __init__(self):
        self.url = 'https://i.instagram.com/api/v1/accounts/send_password_reset/'
        self.headers = {
            'authority': 'www.instagram.com',
            'accept': '*/*',
            'accept-language': 'ar',
            'content-type': 'application/x-www-form-urlencoded',
            'cookie': 'csrftoken=vEG96oJnlEsyUWNS53bHLkVTMFYQKCBV; ig_did=5D80D38A-797B-482D-A407-4B51217E09E7; ig_nrcb=1; mid=ZEqtPgALAAE-IVt6zG-ZazKzI4qN; datr=jrJKZGOaV4gHwa-Znj2QCVyB',
            'origin': 'https://www.instagram.com',
            'referer': 'https://www.instagram.com/accounts/password/reset/?next=%2Faccounts%2Flogout%2F',
            'sec-ch-prefers-color-scheme': 'light',
            'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            'viewport-width': '1261',
            'x-asbd-id': '198387',
            'x-csrftoken': 'vEG96oJnlEsyUWNS53bHLkVTMFYQKCBV',
            'x-ig-app-id': '936619743392459',
            'x-ig-www-claim': '0',
            'x-instagram-ajax': '1007389883',
            'x-requested-with': 'XMLHttpRequest',
        }

    def send_password_reset(self, user_email):
        data = {
            "user_email": user_email
        }
        try:
            response = requests.post(self.url, headers=self.headers, data=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

# Example usage
if __name__ == "__main__":
    instagram_api = InstagramAPI()
    email = input("Enter the email to reset password: ")
    result = instagram_api.send_password_reset(email)
    print(result)
