import json
class AccountManager:
    def __init__(self):
        self.file = "user.json"
    def load(self):
        with open(self.file,"r",encoding="utf-8") as f:
            return json.load(f)
    def save(self,data):
        with open(self.file,"w",encoding="utf-8") as f:
            json.dump(data,f,indent=4)
    def login(self,username,password):
        data=self.load()
        for acc in data["admin"]:
            if acc["username"]==username and acc["password"]==password:
                return "admin"
        for acc in data["user"]:
            if acc["username"]==username and acc["password"]==password:
                return "user"
        return None
    def register(self,username,password):
        data=self.load()
        for acc in data["admin"]+data["user"]:
            if acc["username"]==username:
                return False
        data["user"].append({
            "username":username,
            "password":password
        })
        self.save(data)
        return True