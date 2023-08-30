import hashlib
import json
import secrets
import requests

class MT5RestAPI:

    def __init__(self, login, password, server, port):
        self.login = login
        self.password = password
        self.server = server
        self.port = port
        self.session = requests.session()

    def auth_1_get(self):
        print("auth_start")
        url = "https://"+self.server+":"+str(self.port)+"/auth_start?version=2980&agent=WebManager&login="+str(self.login)+"&type=manager"
        headers = {
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0",
            }
        # response = requests.request("GET",url,headers=headers,verify=False)
        response = self.session.get(url,headers=headers,verify=False)
        # print(response.text)
        data = json.loads(response.text)
        print(url)
        print(data)
        return data["srv_rand"]

    def auth_2_get(self):
        srv_rand = self.auth_1_get()
        # srv_rand = "73007dc7184747ce0f7c98516ef1c851"
        print(" ")
        print("auth_answer")
        print("srv_rand = " + str(srv_rand))
        # Password
        encode_password = self.password.encode("utf-16-le")
        hash_password = hashlib.md5(encode_password)
        hex_hash_password = hash_password.hexdigest()
        byte_hex_hash_password = bytes.fromhex(hex_hash_password)
        #
        list_byte_hex_hash_password = list(byte_hex_hash_password)
        print("#1. pass in byte array: " + str(self.password))
        print(list_byte_hex_hash_password)
        # WebAPI
        encode_webapi = "WebAPI".encode("utf-8")
        #
        list_encode_webapi_byte = list(encode_webapi)
        print("#2. WebAPI byte array:")
        print(list_encode_webapi_byte)
        #
        byte_password_webapi = byte_hex_hash_password + encode_webapi
        list_byte_password_webapi = list(byte_password_webapi)
        print("#3. byte array of password + WebAPI:")
        print(list_byte_password_webapi)
        #
        hash_password_webapi = hashlib.md5(byte_password_webapi)
        hex_hash_password_webapi = hash_password_webapi.hexdigest()
        byte_hex_hash_password_webapi = bytes.fromhex(hex_hash_password_webapi)
        #
        list_byte_hex_hash_password_webapi = list(byte_hex_hash_password_webapi)
        print("#4. MD5 of password + WebAPI byte array:")
        print(list_byte_hex_hash_password_webapi)
        #
        byte_srv_rand = bytes.fromhex(srv_rand)
        list_byte_srv_rand = list(byte_srv_rand)
        print("#5. byte array of SRV_RAND:")
        print(list_byte_srv_rand)
        #
        byte_srv_rand_answer = byte_hex_hash_password_webapi + byte_srv_rand
        list_byte_srv_rand_answer = list(byte_srv_rand_answer)
        print("#6. byte array of steps1-4 + SRV_RAND:")
        print(list_byte_srv_rand_answer)
        #
        hash_byte_srv_rand_answer = hashlib.md5(byte_srv_rand_answer)
        hex_srv_rand_answer = hash_byte_srv_rand_answer.hexdigest()
        byte_hex_srv_rand_answer = bytes.fromhex(hex_srv_rand_answer)
        list_byte_hex_srv_rand_answer = list(byte_hex_srv_rand_answer)
        print("#7. final hash:")
        print(list_byte_hex_srv_rand_answer)
        #
        srv_rand_answer = hex_srv_rand_answer
        print("srv_rand_answer=" + srv_rand_answer)
        cli_rand = secrets.token_hex(16) # cli_rand = "09556255c035cdbd7cf20c2d571b5b28"
        #
        url = "https://" + self.server + ":" + str(self.port) + "/auth_answer?srv_rand_answer=" + str(srv_rand_answer) + "&cli_rand=" + cli_rand
        headers = {
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0",
        }
        #
        response = self.session.get(url, headers=headers, verify=False)
        print(url)
        print(response.text)
        data = json.loads(response.text)
        #print(data)
        #
        return data["cli_rand_answer"]

    def symbol_get(self, symbol):
        url = "https://" + self.server + ":" + str(self.port) + "/api/symbol/get?symbol=" + symbol
        headers = {
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0",
        }
        #
        response = self.session.get(url, headers=headers, verify=False)
        print(url)
        print(response.text)
        #data = json.loads(response.text)
        #print(data)

    def deposit(self, login, type_par, balance, comment):
        url = "https://" + self.server + ":" + str(self.port) + "/api/trade/balance?login=" + str(login) + "&type=" + str(type_par) + "&balance=" + str(balance) + "&comment=" + comment
        response = self.session.get(url)
        print(url)
        print(response.text)
        answer = json.loads(response.text)
        return answer
    
    def format_id(self, login, id):
        url = "https://" + self.server + ":" + str(self.port) + "/api/user/update?login=" +str(login) +"&id=" +str(id)
        response = self.session.get(url)
        print(url)
        print(response.text)
    
    def get_by_login(self, login):
        url = "https://" + self.server + ":" + str(self.port) + "/api/user/get?login=" +str(login)
        response = self.session.get(url)
        print(url)
        print(response.text)

    def get_all_logins(self):
        url = "https://" + self.server + ":" + str(self.port) + "/api/user/logins"
        response = self.session.get(url)
        #print(response.text)
        return response

    def update_account(self, login, field, field_value):
        url = "https://" + self.server + ":" + str(self.port) + "/api/user/update?login=" +str(login) +"&"+str(field)+"="+str(field_value)
        headers = {
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0",
        }
        response = self.session.get(url, headers=headers, verify=False)
        print(url)
        print(response.text)

    def create_demo(self, Login, master_pass, investor_pass, nname, email):
        url = "https://" + self.server + ":" + str(self.port) + "/api/user/add?Login=" +str(Login) + "&pass_main=" + str(master_pass) + "&pass_investor=" + str(investor_pass) + "&group=demo\demo-mg"+ "&name=" + str(nname) + "&email=" + str(email)
        headers = {
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0",
        }
        response = self.session.get(url, headers=headers, verify=False)
        print(url)
        print(response.text)
        return response.text