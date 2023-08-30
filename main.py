from hubspot import HubSpot
from pprint import pprint
from hubspot.crm.contacts import ApiException, SimplePublicObjectInput
import pandas as pd
import numpy as np
#import MetaTrader5
#import file
import json
import urllib3
import logging
import secrets
import string
import os
import io
import time

#os.chdir('hubspot_mt5_api')

from Classes.MT5RestAPI import MT5RestAPI

alphabet = string.ascii_letters + string.digits

login = 1111
password = "api_pass_MG"
server = "trading.mercadosg.com"
port = 443
rest_api = MT5RestAPI(login, password, server, port)

def connect_mt5():
    # --
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    format_msg = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format_msg, level=logging.INFO, datefmt="%H:%M:%S")
    logging.info("Main    : start")
    # --
    cli_rand_answer = rest_api.auth_2_get()

def create_demo_acc(Login, master_pass, inves_pass, name, email):
    response = rest_api.create_demo(Login, master_pass, inves_pass, name, email)
    return response

def get_all_clients():
    response = rest_api.get_all_logins()
    df_clients = pd.read_csv(io.StringIO(response.text))
    df_clients.rename(columns={'{ "retcode" : "0 Done"':'Login',' "answer" : [':'Something'}, inplace=True)
    df_clients.Login = pd.to_numeric(df_clients['Login'], errors='coerce')
    df_clients.sort_values('Login',ascending=False,inplace=True,ignore_index=True)
    return df_clients

def deposit_mt5(login, type_par, balance, comment):
    response = rest_api.deposit(login=login,type_par=type_par,balance=balance,comment=comment)
    return response

api_client = HubSpot(access_token='pat-na1-e71ad220-f5b2-4fe9-b388-d5ca536488aa')

try:
    read_last_id=np.loadtxt('last_id_n.txt')
    api_response = api_client.crm.contacts.basic_api.get_page(limit = 100, after=int(read_last_id), archived=False)
    api_response_dict = api_response.to_dict()['results']
    df = pd.DataFrame.from_dict(data=api_response_dict)
    #df = df.explode('properties')
    #df.reset_index(drop=True, inplace=True)

    last_id = (df['id'].iloc[-1])

    if (df.shape[0]>1):
        connect_mt5()
        for index,row in df.iterrows():
            if(index>0):
                name = str(row.properties['firstname'])+" "+str(row.properties['lastname'])
                email = str(row.properties['email'])
                password_master = ''.join(secrets.choice(alphabet) for i in range(10))
                password_investor = ''.join(secrets.choice(alphabet) for i in range(10))
                #clients=get_all_clients()
                #last_account = clients.iloc[0,0]
                #Login=int(last_account+1)
                Login=0
                mt5_response = create_demo_acc(Login,password_master, password_investor, name, email)
                #print("Last registered account is: "+str(last_account))
                #print("Next login for demo would be: "+str(last_account+1))
                mt5_json = json.loads(mt5_response)
                demo_login = int(mt5_json['answer']['Login'])
                deposit_answer = deposit_mt5(demo_login, 2, 1000000, 'Demo')
                ### Update contact on HubSpot ###
                properties = {
                    'id_lead_mt5_demo' : str(demo_login),
                    'primera_contrasena_mt5_demo' : password_master
                }
                simple_public_object_input = SimplePublicObjectInput(properties=properties)
                response_2 = api_client.crm.contacts.basic_api.update(row.id, simple_public_object_input=simple_public_object_input)
                pprint(response_2)
        file = open("last_id_n.txt", "w")
        file.write(last_id)
        file.close()

    else:
        print("No new accounts on HS")


except ApiException as e:
    print("Exception when calling basic_api->get_page: %s\n" % e)