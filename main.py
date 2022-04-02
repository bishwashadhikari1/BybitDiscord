from dotenv import load_dotenv
import os
from pybit.usdt_perpetual import HTTP
import requests
import time

load_dotenv()

api_key = os.getenv("api_key")
api_secret = os.getenv("api_secret")
discord_web_hook = os.getenv("discord_web_hook")
client = HTTP("https://api.bybit.com", api_key=api_key, api_secret=api_secret)



def new_positions(positions):
    message = "Position has an update!\n"
    message +="{:>0} {:>15} {:>20} {:>20} {:>20}\n".format(*['Symbol', 'Side', 'Entry', 'Take Profit', 'Stop Loss'])

    for position in positions:
        # message += position[0] + "\t" + position[1] + "\t" + str(position[2]) + "\t" + str(position[3]) + "\t" + str(position[4]) + "\n"
        message += "{:>0} {:>15} {:>20} {:>20} {:>20}\n".format(*position)
    requests.post(discord_web_hook, json={"content": message})

def check_positions():
    all_positions = client.my_position()["result"]
    show_positions = []
    for positions in all_positions:
        position = positions["data"]
        if position['size'] != 0:

            show_positions.append([position["symbol"][0:-4], position["side"],position["entry_price"], position["take_profit"], position["stop_loss"]])
    return show_positions
old_position = []
while 1:
    positions = check_positions()
    if positions != old_position: 
        new_positions(positions)
        old_position = positions
    time.sleep(2)