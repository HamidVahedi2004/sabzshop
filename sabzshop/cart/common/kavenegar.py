from kavenegar import *
from order import *
from kavenegar import KavenegarAPI, APIException, HTTPException



def send_sms_template(receptor, token:dict, template):
    try:
        api= KavenegarAPI('6172777A596E3368396B355A6C4C55556C4233774B6E2B484E465276436B487064463343694A74594546343D')
        params={
            'receptor':receptor,
            'template':template
            
        }
        for key, value in token.items():
            params[key]= value
            
        response= api.verify_lookup(params)
        print(response)
        return(True)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)
        
        
        

API_KEY = "6172777A596E3368396B355A6C4C55556C4233774B6E2B484E465276436B487064463343694A74594546343D"
SENDER = "2000660110"


def send_sms(receptor, message):
    try:
        api = KavenegarAPI(API_KEY)
        params = {
            "sender": SENDER,
            "receptor": receptor,
            "message": message,
        }
        response = api.sms_send(params)
        print(response)
        return True

    except APIException as e:
        print("API ERROR:", e)
    except HTTPException as e:
        print("HTTP ERROR:", e)

    return False

   
