import asyncio, genshin, json, cookies_setup
from datetime import datetime
from os import path

def checkin(nickname, games:list): # Claims MiHoyo Games dailies
    cookies = cookies_setup.setup_cookies(nickname=nickname)
    
    async def claim(game_name): 
        client = genshin.Client(cookies, game=game_name)
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
    
    hoyo_games = cookies_setup.list_games()
    
    for game in hoyo_games:
        if game["game_biz"] in games:
            try:
                asyncio.run(claim(game["game_name"]))
            except Exception as e:
                error = f'{e}'
                print( error)
                log(error, game["game_name"])

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
        nickname = user.get('hoyolab_nickname')
        checkin(nickname,user["games"])

if __name__ == '__main__':
    fischl()
