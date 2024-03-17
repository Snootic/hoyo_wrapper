import genshin, asyncio, json, cookies_setup

async def search_users(nickname): # search for users in hoyolab by Nickname
    users = await client.search_users(nickname)
    users_dict = {}
    for user in users:
        print(user, '\n')
        users_dict[f"{user.nickname}"] = user.hoyolab_id
    return users, users_dict

async def build_profile(id: int = 0): # build user profile based on id
    # if no id is provided, it will build the user's own profile
    
    hoyo_games = cookies_setup.list_games()
    
    if id == 0:
        id = cookies['ltuid_v2']
        account = await client.get_hoyolab_user()
    else:
        account = await client.get_hoyolab_user(id)
    print(account)
    
    record_data = await client.get_record_cards(id) # gets the record data from user on hoyolab
    
    for record in record_data:
        for game in hoyo_games:
            if game["game_id"] == record.game_id:
                print('\n', game["game_name"], record)
        
    return account, record_data


async def genshin_chronicle(uid:int = 0,server='America Server'):
    # Gets the battle chronicle of the player
    
    def print_info(account):
        user = await client.get_genshin_user(uid)
        for value in user:
            for item in value:
                print(item.upper() if item == value[0] else item,'\n')
                
    def print_characterirt
    
    if uid == 0:
        user_accounts = await client.get_game_accounts()
        if isinstance(user_accounts,list):
            for account in user_accounts:
                if account.game_biz == 'hk4e_global' and account.server_name == server:
                    user = await client.get_genshin_user(account.uid)
                    print_info(account)
    else:
        await print_account(uid)

async def lisa(): # menu
    choose = int(input("[1] - Search Users, [2] - See own profile: "))
    if choose == 1:
        nickname = input("Nickname to search: ")
        result = await search_users(nickname)
        users = result[0]
        dict = result[1]
        while True:
            choose = input('Insert the nickname to open the profile ("exit" to leave): ')
            if choose != "exit":
                try:
                    nickname = dict[choose]
                    await build_profile(nickname)
                    break
                except Exception as e:
                    print(e)
            else:
                return
    elif choose == 2:
        await build_profile()
        return
    elif choose == 3:
        await genshin_chronicle()
        return

if __name__ == "__main__":
    nickname = input("Your Nickname: ")
    cookies = cookies_setup.setup_cookies(nickname=nickname)
    client = genshin.Client(cookies)
    asyncio.run(lisa())