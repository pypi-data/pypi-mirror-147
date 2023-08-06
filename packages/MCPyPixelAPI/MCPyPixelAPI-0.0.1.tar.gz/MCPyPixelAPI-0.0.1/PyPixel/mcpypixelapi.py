import requests
from imports import ThreadWithResult

# Hypixel class, stores all functions, Skyblock class soon
class Hypixel:
    def __init__(self, key, my_uuid):
        self.key = key
        self.my_uuid = my_uuid


    # Get raw, unformated json containing all of the hypixel player data(NOT RECOMMENED, can contain hundreds of lines of player data)
    def rawdata(self, player_name):
        get_uuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{player_name}").json()
        return requests.get(f"https://api.hypixel.net/player?key={self.key}&uuid={get_uuid['id']}").json()

    # Gets your Hypixel API Key
    def getkey(self, **kwargs):
        if "isVerbose" in kwargs.keys() and kwargs["isVerbose"] == True:
            return requests.get(f"https://api.hypixel.net/key?key={self.key}&uuid={self.my_uuid}").json()
        elif "isVerbose" not in kwargs.keys():
            return requests.get(f"https://api.hypixel.net/key?key={self.key}&uuid={self.my_uuid}").json()["record"]["key"]
        return requests.get(f"https://api.hypixel.net/key?key={self.key}&uuid={self.my_uuid}").json()["record"]["key"]
    
    # Ranked Skywars Info
    def rankedSkywars(self, player_name):
        get_uuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{player_name}").json()
        return requests.get(f"https://api.hypixel.net/player/ranked/skywars?key={self.key}&uuid={get_uuid['id']}").json()

    def games(self, player_name):
        get_uuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{player_name}").json()
        return requests.get(f"https://api.hypixel.net/resources/games?key={self.key}&uuid={get_uuid['id']}").json()

    # Shows your Hypixel achievements
    def achievements(self, player_name):
        get_uuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{player_name}").json()
        return requests.get(f"https://api.hypixel.net/resources/achievements?key={self.key}&uuid={get_uuid['id']}").json()
    
    def challenges(self, player_name):
        get_uuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{player_name}").json()
        return requests.get(f"https://api.hypixel.net/resources/challenges?key={self.key}&uuid={get_uuid['id']}").json()

    def quests(self, player_name):
        get_uuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{player_name}").json()
        return requests.get(f"https://api.hypixel.net/resources/quests?key={self.key}&uuid={get_uuid['id']}").json()

    def vanityPets(self, player_name):
        get_uuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{player_name}").json()
        return requests.get(f"https://api.hypixel.net/resources/vanity/pets?key={self.key}&uuid={get_uuid['id']}").json()

    def vanityCompanions(self, player_name):
        get_uuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{player_name}").json()
        return requests.get(f"https://api.hypixel.net/resources/vanity/companions?key={self.key}&uuid={get_uuid['id']}").json()

    def boosters(self):
        return requests.get(f"https://api.hypixel.net/boosters?key={self.key}").json()

    def counts(self):
        return requests.get(f"https://api.hypixel.net/counts?key={self.key}").json()

    def leaderboards(self):
        return requests.get(f"https://api.hypixel.net/leaderboards?key={self.key}").json()
    
    def punishmentstats(self): 
        return requests.get(f"https://api.hypixel.net/punishmentstats?key={self.key}").json()
    
    def recentgames(self, player_name, **kwargs):
        myRecentGames = []
        get_uuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{player_name}").json()
        myGames = requests.get(f"https://api.hypixel.net/recentgames?key={self.key}&uuid={get_uuid['id']}").json()
        
        for i in range(len(myGames["games"])):
            game = {}
            game["GameType"] = myGames["games"][i]["gameType"]
            game["Mode"] = myGames["games"][i]["mode"]
            game["Map"] = myGames["games"][i]["map"]
            myRecentGames.append(game)
        if "isVerbose" in kwargs.keys() and kwargs["isVerbose"] == True:
            return myGames
        elif "isVerbose" not in kwargs.keys():
            return myRecentGames
        return myRecentGames

    def status(self, player_name, **kwargs):
        get_uuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{player_name}").json()
        if "isVerbose" in kwargs.keys() and kwargs["isVerbose"] == True:
            return requests.get(f"https://api.hypixel.net/status?key={self.key}&uuid={get_uuid['id']}").json()
        elif "isVerbose" not in kwargs.keys():
            return requests.get(f"https://api.hypixel.net/status?key={self.key}&uuid={get_uuid['id']}").json()["session"]["online"]
        return requests.get(f"https://api.hypixel.net/status?key={self.key}&uuid={get_uuid['id']}").json()["session"]["online"]
        

    # Get friends list of selected player
    def friends(self, uuid):
        friend_data = {}
        player_num = 0
        get_uuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{uuid}").json()
        data = requests.get(f"https://api.hypixel.net/friends?key={self.key}&uuid={get_uuid['id']}").json()
        threads_list = list()

        # Fetch data from Hypixel
        def get_data(self, uuid, data, player_num, data_loc):
            if data["records"][player_num][data_loc] != uuid:
                player = data["records"][player_num][data_loc]
                name = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{player}").json()
                status = requests.get(f"https://api.hypixel.net/status?key={self.key}&uuid={player}").json()
                full_data = [name["name"], status["session"]["online"]]
                return full_data
            else:
                return None
        # Execute function in threads, Speeds up api
        if len(data["records"]) <= 30:
            for i in range(0, len(data["records"])):
                thread = ThreadWithResult(target=get_data, args=(self, uuid, data, player_num, "uuidReceiver"))
                thread2 = ThreadWithResult(target=get_data, args=(self, uuid, data, player_num, "uuidSender"))
                thread.start()
                thread2.start()
                threads_list.append(thread)
                threads_list.append(thread2)
                player_num += 1
            
            # Fetch data from each threaded function
            for j in threads_list:
                if j.join() != None:
                    friend_data[j.join()[0]] = j.join()[1]
                else:
                    pass
            del friend_data[uuid]
            return friend_data
        else:
            print(f"Imposible Action: Too many threads")

        # Return player's friend list
        del friend_data[uuid]
        return friend_data