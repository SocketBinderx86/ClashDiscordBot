import requests
import db
from threading import Lock, Thread as th

TOKEN = None
get_headers = None
post_headers = None

# TOKEN = ''




def init(clash_token):
    TOKEN = clash_token

    get_headers = {
    'Accept': 'application/json',
    'authorization': f'Bearer {TOKEN}',
    }

    post_headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {TOKEN}',
    }

async def get_member_list() -> str:
    response = requests.get('https://api.clashofclans.com/v1/clans/%232QOGJV9QR', headers=get_headers)
    ret_str = ''
    user_json = response.json()
    for member in user_json['memberList']:
        ret_str += '{0}\t\t{1}\t\t{2}\t\t{3}\n'.format(member['clanRank'], member['name'], member['role'], member['tag'])
    return ret_str

async def verify(tag, clash_token, discord_name) -> tuple:
    if db.is_member(tag):
        return False, "Account already linked"
    data = {
        'token': clash_token,
    }
    post_tag = f'%23{tag.upper().replace("#", "")}'
    response = requests.post(f'https://api.clashofclans.com/v1/players/{post_tag}/verifytoken', json=data, headers=post_headers, timeout=3)
    print(response.text)
    user_json = response.json()
    if "status" not in user_json or user_json['status'] != 'ok':
        return False, 'command failed, please check that your values are correct'
    if db.insert_member(discord_name, tag)[0] != True:
        return False, "Critical error, Please contact server admin"
    return True, "success"
    