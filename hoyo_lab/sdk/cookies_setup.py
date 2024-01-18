import genshin, asyncio, json
from os.path import abspath

def setup_cookies(get_nickname:bool = False, nickname: str = ''):
    user_data = abspath("hoyo_lab/user_data.json")
    with open(user_data, "r") as users:
        users = json.load(users)
    
    if get_nickname:
        nicknames = []
        for user in users:
            nickname = user.get("hoyolab_nickname")
            nicknames.append(nickname)
        return nicknames
    
    else:
        for user in users:
            if user.get("hoyolab_nickname") == nickname:
                ltuid = user.get("ltuid", user.get("ltuid_v2"))
                ltoken = user.get("ltoken", user.get("ltoken_v2"))
                try:
                    ltmid_v2 = user.get("ltmid_v2")
                except:
                    pass
                    
                cookies = {}
                
                if isinstance(ltuid,int):
                    cookies["ltuid"] = ltuid
                else:
                    cookies["ltuid_v2"] = ltuid

                if "v2" not in ltoken:
                    cookies["ltoken"] = ltoken
                else:
                    cookies["ltoken_v2"] = ltoken
                
                if ltmid_v2:
                    cookies["ltmid_v2"] = ltmid_v2
                return cookies

def list_games():
    supported_games = abspath("hoyo_lab/games.json")
    with open(supported_games, "r") as supported_games:
        hoyo_games = json.load(supported_games)
    return hoyo_games