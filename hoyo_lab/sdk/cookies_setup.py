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
                return user

def list_games():
    supported_games = abspath("hoyo_lab/games.json")
    with open(supported_games, "r") as supported_games:
        hoyo_games = json.load(supported_games)
    return hoyo_games

if __name__ == "__main__":
    setup = setup_cookies(nickname="Snootic")
    print(setup)