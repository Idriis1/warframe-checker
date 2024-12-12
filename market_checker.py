import asyncio
import time
import websockets
import json
import threading
import requests
from queue import SimpleQueue
import os
import re
from sound import play_sound,sound_enabled
from tkinter import messagebox  # Import messagebox from tkinter
import pygame.mixer
import subprocess
from queue import Queue
# Initialize global variables
items = []
running = False

queue = SimpleQueue()
sniping_queue = Queue()
watcher_queue = Queue()


sound_enabled = True
orders_type = "sell"
items_dict = {}
watcher_running = False





# Initialize pygame mixer for sound effects
pygame.mixer.init()

def play_sound(sound_file='wf.mp3'):
    try:
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
    except pygame.error as e:
        print(f"Error playing sound: {e}")

def toggle_sound(x):
    global sound_enabled
    sound_enabled = not sound_enabled
    if sound_enabled:
        x.config(text="Sound: ON")
    else:
        x.config(text="Sound: OFF")

def toggle_status(x):
    global orders_type
    if orders_type == "sell":
        x.config(text="orders type : buy")
        orders_type = "buy"
    else:
        x.config(text="orders type : sell")
        orders_type = "sell"


def load_items_from_file():
    global items
    global items_dict
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "list.txt")

    try:
        with open(file_path, "r") as file:
            items = [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        print("list.txt not found. Using empty list.")
    items_dict.clear()
    for item in items:
        if '|' in item:
            name, price_limit = item.split('|')
            items_dict[name] = int(price_limit)
        else:
            items_dict[item] = None    

load_items_from_file()






def start_watcher(button,action):
    global watcher_running
    watcher_running = True
    threading.Thread(target=watcher_thread, daemon=True).start()
    button.config(state=action)
    print("watcher starting")


def stop_watcher(button,action):
    global watcher_running
    watcher_running = False
    button.config(state=action)
    print("watcher stopped")




async def watcher_loop():
    global watcher_running
    print('Looping...')
    print("watcher running ?", watcher_running)
    while watcher_running:
        print('enter while')
        try:
            with open('watcher.txt', 'r') as file:
                watcher_list = [line.strip() for line in file.readlines()]

            for item in watcher_list:
                if not watcher_running:
                    break

                if '|' in item:
                    item_name, max_price = item.split('|')
                    max_price = float(max_price)
                else:
                    item_name, max_price = item, None

                headers = {
                    # 'User-Agent': 'WarframeMarketChecker/1.0 (+https://example.com)'
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36'
                }
                response = requests.get(f'https://api.warframe.market/v1/items/{item_name}/orders', headers=headers)
                
                if response.status_code != 200:
                    print(f"Error fetching data for {item_name}: Status code {response.status_code}")
                    continue

                orders = response.json()['payload']['orders']
                orders = response.json()['payload']['orders']
                filtered_orders = []
                for order in orders:
                    if order['order_type'] == 'sell' and order['user']['status'] == 'ingame':
                        order['player_name'] = order['user']['ingame_name']
                        order['mod_rank'] = order['mod_rank'] if 'mod_rank' in order else None
                        filtered_orders.append(order)

                sorted_orders = sorted(filtered_orders, key=lambda x: x['platinum'])

                top_orders = sorted_orders[:2]
                for order in top_orders:
                    if max_price is None or order['platinum'] <= max_price:
                        print(order)
                        {'platinum': 38, 'visible': True, 'order_type': 'sell', 'quantity': 4, 'user': {'reputation': 10, 'locale': 'zh-hans', 'avatar': None, 'last_seen': '2024-07-04T10:21:37.712+00:00', 'ingame_name': 'pengming0712', 'id': '65c484c7c0684003363572a2', 'region': 'en', 'status': 'ingame'}, 'platform': 'pc', 'creation_date': '2024-07-04T12:11:39.000+00:00', 'last_update': '2024-07-04T12:11:39.000+00:00', 'id': '6686917b5ca3221aa70a34b1', 'region': 'en'}
                        item_name_en = item_name
                        player_name = order['user']['ingame_name']
                        mod_rank = order['mod_rank']
                        platinum =order['platinum']
                        quantity =order['quantity']
                        watcher_queue.put((order['player_name'] ,item_name_en,order['platinum'] ,order['quantity'], order['mod_rank']))

                time.sleep(0.34)
        except Exception as e:
            print(f"Error in watcher loop: {e}")

        await asyncio.sleep(60)
        # clear_watcher()


def watcher_thread():
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(watcher_loop())


def update_watcher_tab(tree_watcher, *item):

    player_name,item_name_en, price, quantity,mod_rank = item
    status_text = f"{player_name}{item_name_en}: {price}p x{quantity} r{mod_rank}"
    tree_watcher.insert("", "end", values=(player_name,item_name_en, price,quantity,mod_rank))
    
    print("Updated watcher tab view")
    if sound_enabled:
        play_sound('wf.mp3')


    
def clear_watcher(tree):
    for item in tree.get_children():
        tree.delete(item)



def update_watcher_list():
    try:
           script_dir = os.path.dirname(os.path.abspath(__file__))
           file_path = os.path.join(script_dir, "watcher.txt")
           subprocess.Popen(["geany",file_path])

           
    except Exception as e:
            messagebox.showerror("Error", f"Failed to open watcher.txt: {e}")










def update_sniping_tab(tree_sniping,player_name, player_status, item_name, quantity, price,rank):
    status_text = f"Player: {player_name} ({player_status}) {orders_type}ing \"{item_name}\" x{quantity} for {price} platinum r{rank}"
    tree_sniping.insert("", "end", values=(status_text,))
    if sound_enabled:
        play_sound()
async def check_market():
    global running
    global items_dict
    url = "wss://warframe.market/socket?platform=pc"
    
    async with websockets.connect(url) as websocket:
        await websocket.send(json.dumps({"type": "@WS/SUBSCRIBE/MOST_RECENT"}))
        while running:
            message = await websocket.recv()
            data = json.loads(message)            
            if data["type"] == "@WS/SUBSCRIPTIONS/MOST_RECENT/NEW_ORDER":
                item_url_name = data["payload"]["order"]["item"]["url_name"]
                item_price = data["payload"]["order"]["platinum"]
                if item_url_name in items_dict:
                    price_limit = items_dict[item_url_name]
                    if price_limit is None:
                        price_check = True
                    else:
                        if orders_type == "sell":
                            price_check = item_price <= price_limit 
                        elif orders_type == "buy":
                            price_check = item_price >= price_limit
                        else:
                            price_check = False
                    if price_check and data["payload"]["order"]["order_type"] == orders_type:
                        item_name = data["payload"]["order"]["item"]["en"]["item_name"]
                        player_name = data["payload"]["order"]["user"]["ingame_name"]
                        player_status = data["payload"]["order"]["user"]["status"]
                        price = data["payload"]["order"]["platinum"]
                        rank = data["payload"]["order"].get("mod_rank", 0)  # Default to 0 if mod_rank is not present 
                        quantity = data["payload"]["order"]["quantity"]
                        sniping_queue.put((player_name, player_status, item_name, quantity, price,rank))
                        print(player_name, player_status, item_name, quantity, price,rank)

def asyncio_thread():
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(check_market())



def start_checking(button,action):
    global running
    running = True
    threading.Thread(target=asyncio_thread, daemon=True).start()
    button.config(state=action)
    print("app starting")

def stop_checking(button,action):
    global running
    running = False
    button.config(state=action)
    print("app stopped")
    load_items_from_file()
    print("item reloaded while stopped!")


def update_checking_list():
    
    global items
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "list.txt")
    print(file_path)
    try:
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                pass
        process = subprocess.Popen(["geany", file_path])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open list.txt: {e}")
        print("Error", f"Failed to open list.txt: {e}")
    load_items_from_file()
    print('list updated.')



def update_checking_priced_list():
    global items
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, "priced-list.txt")
        subprocess.Popen(["geany",file_path])
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open list.txt: {e}")
    load_items_from_file()

def grab_update_prices(t, end,normal,disabled):
    try:
        priced_list = []
        for item in items:
            url = f"https://api.warframe.market/v1/items/{item}/orders"
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200:
                sell_orders = data["payload"]["orders"]
                if sell_orders:
                    prices = [order["platinum"] for order in sell_orders if order["order_type"] == orders_type and order['user']['status'] =="ingame"]
                    if prices:
                        min_price = min(prices)
                        max_price = max(prices)
                        avg_price = sum(prices) / len(prices)
                        avg_price = round(avg_price)
                        priced_list.append(f"{item} | {min_price} | {max_price} | {avg_price}")
                    else:
                        priced_list.append(f"{item} | - | - | -")
                else:
                    priced_list.append(f"{item} | - | - | -")
            else:
                messagebox.showerror("Error", f"Failed to fetch data for {item}")


        t.config(state=normal)  
        t.delete('1.0', end) 
        for item_info in priced_list:
            t.insert(end, item_info + "\n")
        t.config(state=disabled) 

        script_dir = os.path.dirname(os.path.abspath(__file__))
        priced_list_file = os.path.join(script_dir, "priced-list.txt")
        
        if not os.path.exists(priced_list_file):
            with open(priced_list_file, "w") as file:
                pass  

        with open(priced_list_file, "w") as file:
            for item_info in priced_list:
                file.write(item_info + "\n")

    
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update prices: {e}")
def copy_to_clipboard(tree, root):
    item = tree.item(tree.focus())
    if item:
        item_text = item['values'][0]
        print(item_text)
        parts = item_text.split(" ")
        user = parts[1].get('Hyper')
        item_name = re.search('"(.*)"', item_text).group(1)
        amount = parts[-2]
        if orders_type == 'sell':
            message = f"/w {user} Hi I wanna buy {item_name} for {amount}p"
        elif orders_type == 'buy':
            message = f"/w {user} Hi I wanna sell you {item_name} for {amount}p"
        root.clipboard_clear()
        root.clipboard_append(message)
        root.update()
        print("item copied")
        messagebox.showinfo("Clipboard", "Message copied to clipboard:\n\n" + message)
        

def copy_to_clipboard2(tree, root):
    item = tree.item(tree.focus())
    if item:
        user = item['values'][0]
        item_text = item['values'][1]
        item_name = item_text.replace('_',' ')
        amount = item['values'][2]
        rank = item['values'][4]
        qty=item['values'][3]
        message = f"/w {user} Hi I wanna buy {item_name} x{qty} for {amount}p r{rank}"        
        root.clipboard_clear()
        root.clipboard_append(message)
        root.update()
        print("watcher copied")
        messagebox.showinfo("Clipboard", "Message copied to clipboard:\n\n" + message)



def clear_sniping_results(tree_sniping):
    tree_sniping.delete(*tree_sniping.get_children())
    print('Clearing')