import genshin, asyncio, json
from os.path import abspath

# Get the cookies from browser
def browser_cookies(browser=None):
    ''' supported browsers:
        brave,
        chrome,
        chromium,
        edge,
        firefox,
        opera
    '''
    cookies = genshin.utility.get_browser_cookies(browser,allowed_cookies=("ltuid",
                                                                            "ltoken",
                                                                            "account_id",
                                                                            "cookie_token",
                                                                            "ltuid_v2",
                                                                            "ltoken_v2",
                                                                            "account_mid_v2",
                                                                            "cookie_token_v2",
                                                                            "ltmid_v2"))

    if cookies is not None:
        asyncio.run(save_cookies(cookies))
    else:
        message = "No cookies found, make sure you chose the right browser and that you're logged in hoyolab."
        print(message)
    
async def set_cookies(account, password): # set browser cookies by logging in with username and password
    client = genshin.Client(debug=True)
    try:
        cookies = await client.login_with_password(account=account, password=password)
    except Exception as e:
        message = f"{e}: An error ocurred, please disable your browser's extensions or choose a different browser and try again."
        print(message)
    else:
        await save_cookies(cookies)

async def save_cookies(cookies): # saves the cookies to json
    ltuid = cookies.get("ltuid", cookies.get("ltmid_v2")) # defines what cookies will be used
    ltoken = cookies.get("ltoken", cookies.get("ltoken_v2"))
    
    client_cookies = {}
    
    if "ltuid" in cookies:
        client_cookies["ltuid"] = ltuid
    else:
        client_cookies["ltmid_v2"] = ltuid

    if "ltoken" in cookies:
        client_cookies["ltoken"] = ltoken
    else:
        client_cookies["ltoken_v2"] = ltoken
    
    print(client_cookies)
    
    client = genshin.Client(client_cookies, debug=True)
    
    hoyolab_account = await client.get_hoyolab_user(cookies["ltuid_v2"])
    nickname = hoyolab_account.nickname # gets user's nickname in hoyolab
    
    cookies["hoyolab_nickname"] = nickname

    print(cookies)
    
    user_accounts = await client.get_game_accounts() # get all games accounts the user have
    games = []
    for account in user_accounts:
        if account.game_biz in games:
            pass
        else:
            games.append(account.game_biz) # append the game biz to list
            
    cookies["games"] = games # adds the games to the cookies
    
    user_data = abspath("hoyo_lab/user_data.json")
    with open(user_data, 'r') as users: # loads the old users_data.json file
        users = json.load(users)

    users.append(cookies) # append the new cookies to the json file
    
    with open(user_data, "w") as new_users:
        json.dump(users, new_users, indent=2) # writes the new user_data.json file
        
if __name__ == '__main__':
    browser_cookies()