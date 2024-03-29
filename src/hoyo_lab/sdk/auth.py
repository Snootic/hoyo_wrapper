import genshin, asyncio, json
from os.path import abspath
import tkinter as tk
from tkinter import ttk

#simple frontend for getting cookies
class Screen():
    def __init__(self):
        self.window = tk.Tk()
    
        self.cookies_text = ttk.Label(self.window, text="Digite seu usuário e sua senha da HoyoLab para resgatar os cookies")
        self.cookies_text.pack()
        
        self.user_field_var = tk.StringVar()
        self.usuario_text = ttk.Label(self.window,text="Usuário")
        self.user_field = ttk.Entry(self.window,textvariable=self.user_field_var)
        self.usuario_text.pack()
        self.user_field.pack()
        
        self.senha_field_var = tk.StringVar()
        self.senha_text = ttk.Label(self.window,text="Senha")
        self.senha_field = ttk.Entry(self.window,textvariable=self.senha_field_var)
        self.senha_text.pack()
        self.senha_field.pack()
        
        self.confirmar1 = ttk.Button(self.window, text="Confirmar", command=self.manual_cookie)
        self.confirmar1.pack()
        
        self.ou_text = ttk.Label(self.window, text="OU")
        self.ou_text.pack()
        
        self.browser_auto_text = ttk.Label(self.window, text="Pegue seus cookies automaticamente via Navegador")
        self.browser_auto2_text = ttk.Label(self.window, text="Você precisa estar logado na HoyoLab para usar esta opção")
        self.browser_auto_text.pack()
        self.browser_auto2_text.pack()
        
        self.browser_var = tk.StringVar()
        supported_browsers = [
            "brave",
            "chrome",
            "chromium",
            "edge",
            "firefox",
            "opera"]
        
        self.browser_menu = ttk.OptionMenu(self.window, self.browser_var, supported_browsers[1], *supported_browsers)
        self.browser_menu.pack()
        
        self.confirmar = ttk.Button(self.window, text="Confirmar", command=self.auto_cookie)
        self.confirmar.pack()
        
        self.window.mainloop()
    
    def popup(self, result):
        window2 = tk.Toplevel(self.window)
        text = ttk.Label(window2, text=result)
        text.pack()
        button = ttk.Button(window2, text='Confirmar', command=window2.destroy)
        button.pack()
    
    def auto_cookie(self):
        navegador = self.browser_var.get()
        get = browser_cookies(browser=navegador)
        print(get)
        self.popup(result=get)
        
    def manual_cookie(self):
        usuario = self.user_field_var.get()
        senha = self.senha_field.get()
        manual = asyncio.run(set_cookies(usuario, senha))
        print(manual)
        self.popup(result=manual)
            
    
def browser_cookies(browser=None):
    ''' supported browsers:
        brave,
        chrome,
        chromium,
        edge,
        firefox,
        opera
    '''
    try:
        cookies = genshin.utility.get_browser_cookies(browser,allowed_cookies=("ltuid",
                                                                            "ltoken",
                                                                            "account_id",
                                                                            "cookie_token",
                                                                            "ltuid_v2",
                                                                            "ltoken_v2",
                                                                            "account_mid_v2",
                                                                            "cookie_token_v2",
                                                                            "ltmid_v2",
                                                                            "mi18nLang"))
    except Exception as e:
        return f"{e}: Ocorreu um erro, tente novamente"

    if cookies is not None:
        result = asyncio.run(save_cookies(cookies))
        return result
    else:
        message = "No cookies found, make sure you chose the right browser and that you're logged in hoyolab."
        print(message)
        return message
    
# Get the cookies from browser    
async def set_cookies(account, password): # set browser cookies by logging in with username and password
    client = genshin.Client(debug=True)
    try:
        cookies = await client.login_with_password(account=account, password=password)
    except Exception as e:
        message = f"{e}: An error ocurred, please disable your browser's extensions or choose a different browser and try again."
        print(message)
        return message
    else:
        result = await save_cookies(cookies)
        return result

async def save_cookies(cookies): # saves the cookies to json
    try:
        client = genshin.Client(cookies, debug=True)
    
        print(client.cookie_manager)
    
        hoyolab_account = await client.get_hoyolab_user(cookies["ltuid_v2"], lang=cookies.get("mi18nLang"))
        nickname = hoyolab_account.nickname # gets user's nickname in hoyolab
    except Exception as e:
        return e
    
    cookies["hoyolab_nickname"] = nickname
    
    user_accounts = await client.get_game_accounts() # get all games accounts the user have
    games = []
    for account in user_accounts:
        if account.game_biz in games:
            pass
        else:
            games.append(account.game_biz) # append the game biz to list
            
    cookies["games"] = games # adds the games to the cookies
    
    user_data = abspath("src/hoyo_lab/user_data.json")
    users = []
    try:
        with open(user_data, 'r') as users: # loads the old users_data.json file
            users = json.load(users)
    except:
        pass
    users.append(cookies) # append the new cookies to the json file
    
    with open(user_data, "w") as new_users:
        json.dump(users, new_users, indent=2) # writes the new user_data.json file
    
    return "Cookies resgatados com sucesso"
        
if __name__ == '__main__':
    screen = Screen()
