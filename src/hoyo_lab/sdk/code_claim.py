import asyncio, genshin, json, cookies_setup, requests
from datetime import datetime
from os import path
from bs4 import BeautifulSoup
from time import sleep

def get_codes(game):
    if game == "STARRAIL":
        source = requests.get("https://honkai-star-rail.fandom.com/wiki/Redemption_Code")
    elif game == "GENSHIN":
        source = requests.get("https://genshin-impact.fandom.com/wiki/Promotional_Code")
    else:
        "game not supported, exiting.."
        return 1
    
    parse = BeautifulSoup(source.text, "html.parser")
    
    codes = []
    for tr in parse.find("table").findAll("tr"):
        tds = tr.findAll("td")
        for i, td in enumerate(tds):
            code = str(td.find("code"))
            if code != "None":
                if "Expired:" in str(tds[i+3]):
                    continue
                codes.append(code[code.find('>')+1 : code.find('</')])
    
    return codes

async def code_claim(game_name:str,redeem_code:str|None=None):
    client = genshin.Client(cookies=cookies, game=game_name)
    user = await client.get_game_accounts()
    user = user[1].nickname
    game = client.game.name
    
    code_file_path = path.abspath(f"hoyo_lab/{user}_{game}_redeemed_codes.txt")
    
    redeemed_codes = []
    
    try:
        with open(code_file_path, 'r') as code_file:
            redeemed_codes = code_file.readlines()
            redeemed_codes = [code.strip() for code in redeemed_codes]
        
    except:
        print(f"Couldn't open {code_file_path}, ignoring it")
    
    if not redeem_code:
        redeem_code = get_codes(game)
        
        for code in redeem_code:
            if code in redeemed_codes:
                message = F"[-2017] Redemption code {code} has been claimed already."
            else:
                try:
                    redemption = await client.redeem_code(code=code)
                except Exception as e:
                    message = (f"{e} {code}")
                else:
                    message = (f"Claimed {code}")
                
            print(message,game,user)    
            log(message, game,"codeRedeem", user)
            
            sleep(5)
    else:
        try:
            if redeem_code in redeemed_codes:
                raise Exception(F"[-2017] Redemption code {redeem_code} has been claimed already.")
            redemption = await client.redeem_code(code=redeem_code)
        
        except Exception as e:
            message = (e)
        else:
            message = (f"Claimed {redeem_code}")
        
        print(message,game,user)    
        log(message, game,"codeRedeem", user)
        
    with open(code_file_path, "a") as code_file:
        for code in redeem_code:
            code_file.write(f"{code}\n")
    
        
def log(message:str, game:str, log_type:str, user:str = ''):  # Saves the results in a log file
    log = f"{datetime.now()} - {user} {game}: {message}\n"
    print(log)
    log_path = path.abspath(f"logs/{log_type}.log")
    with open(log_path, "a") as jean:
        jean.writelines(log)

if __name__ == "__main__":
    cookies = cookies_setup.setup_cookies(nickname="Snootic")
    asyncio.run(code_claim(game_name="hkrpg"))