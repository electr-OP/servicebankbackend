import json
from json.decoder import JSONDecodeError
from django.conf import settings
import requests


class TermiiSmsClassGeneric(object):
    """
        Handles all sms integration with termii
        https://developers.termii.com/
    """


    @staticmethod
    def send_sms(to,message):

        """
        send sms using termii
        """

        url = settings.TERMII_BASE_URL + "/api/sms/send"

        headers = {
            "Content-type": "application/json",
            "Accept":"application/json"
        }

        payload = {
            "to": to[1:],
            "from": settings.TERMII_SENDER_ID_DND,
            "sms": "Your Confirmation code is "+str(message)+"\nFrom ServiceBank, expires in 10 minutes.",
            "type": "plain",
            "channel": "dnd",
            "api_key": settings.TERMII_API_KEY
		}
        print(payload)
 
        try:
            termii_request =  requests.post(
                url, headers=headers, json=payload,timeout=30,
                
            )
            print(termii_request.text)
            if termii_request.status_code == 200:

                termii_response = termii_request.json()
                
                # get response from sedchmap
                if termii_response['code'] == 'ok':
                    
                    termii_response = {
                        "status": True,
                        "response_code":"00",
                        "message": "SMS sent successfully",
                        "data": termii_response,
                     }

                    return termii_response
                else:
                    return {
                        "status": False,
                        "response_code": "01",
                        "message": termii_response['message'],
                    }
            else:
                return {
                    "status": False,
                    "response_code": "02",
                    "message": "SMS Service not available",
                }

        except (requests.exceptions.RequestException, JSONDecodeError, KeyError) as err:
            print(err)
            return {
                "status": False,
                "response_code": "02",
                "message": "SMS Service not available",
            }

 

class TermiiSmsClassDND(object):
    """
        Handles all sms integration with termii
        https://developers.termii.com/
    """


    @staticmethod
    def send_sms(to,message):

        """
        send sms using termii
        """

        url = settings.TERMII_BASE_URL + "/api/sms/send"

        headers = {
            "Content-type": "application/json",
            "Accept":"application/json"
        }

        payload = {
            "to": to[1:],
            "from": settings.TERMII_SENDER_ID_DND,
            "sms": str(message)+"\nFrom ServiceBank, expires in 10 minutes.",
            "type": "plain",
            "channel": "dnd",
            "api_key": settings.TERMII_API_KEY
		}
        print(payload)
 
        try:
            termii_request =  requests.post(
                url, headers=headers, json=payload,timeout=30,
                
            )
            print(termii_request.text)
            if termii_request.status_code == 200:

                termii_response = termii_request.json()
                
                # get response from sedchmap
                if termii_response['code'] == 'ok':
                    
                    termii_response = {
                        "status": True,
                        "response_code":"00",
                        "message": "SMS sent successfully",
                        "data": termii_response,
                     }

                    return termii_response
                else:
                    return {
                        "status": False,
                        "response_code": "01",
                        "message": termii_response['message'],
                    }
            else:
                return {
                    "status": False,
                    "response_code": "02",
                    "message": "SMS Service not available",
                }

        except (requests.exceptions.RequestException, JSONDecodeError, KeyError) as err:
            print(err)
            return {
                "status": False,
                "response_code": "02",
                "message": "SMS Service not available",
            }
