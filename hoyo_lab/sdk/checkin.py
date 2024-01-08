import asyncio
import genshin
from datetime import datetime
from os import path
import json

# TODO: Fix no "hoyolab id set" warning for accounts using ltmid_v2

def checkin(ltuid:int|str, ltoken:str, games:list): # Claims MiHoyo Games dailies
    cookies = {}
    
    if isinstance(ltuid,int):
        cookies["ltuid"] = ltuid
    else:
        cookies["ltmid_v2"] = ltuid

    if "v2" not in ltoken:
        cookies["ltoken"] = ltoken
    else:
        cookies["ltoken_v2"] = ltoken
        
    async def claim(hoyo_game): 
        client = genshin.Client(cookies, game=hoyo_game)
        user = await client.get_game_accounts()
        user = user[1].nickname
        game = client.game.name
        
        try:
            reward = await client.claim_daily_reward()
        except Exception as e:
            message = e
        else:
            message = (f"Claimed {reward.amount} x {reward.name}")
            
        print(message,game,user)
        log(message,game,user)
    
    supported_games = path.abspath("hoyo_lab/games.json")
    with open(supported_games, "r") as supported_games:
        hoyo_games = json.load(supported_games)
    
    for i in games:
        try:
            asyncio.run(claim(hoyo_games[i]))
        except:
            error = f'Game not supported by hoyolab'
            print( error)
            log(error, i)

def log(message, game, user=''):  # Saves the results in a log file
    checkin_log = f"{datetime.now()} - {user} {game}: {message}\n"
    print(checkin_log)
    log_path = path.abspath("logs/checkin.log")
    with open(log_path, "a") as amber:
        amber.writelines(checkin_log)

def fischl(): # Main function
    user_data = path.abspath("hoyo_lab/user_data.json")
    with open(user_data, "r") as users:
        users = json.load(users)
        
    for user in users:
        ltuid = user.get("ltuid", user.get("ltmid_v2"))
        ltoken = user.get("ltoken", user.get("ltoken_v2"))
        checkin(ltuid,ltoken,user["games"])

if __name__ == '__main__':
    fischl()
