import tkinter as tk
from gui import create_gui, process_sniping_queue, process_watcher_queue
from market_checker import start_checking, stop_checking, update_checking_list, update_checking_priced_list, grab_update_prices, clear_sniping_results, toggle_status, start_watcher, stop_watcher, update_watcher_list, clear_watcher

from tkinter import ttk

root = tk.Tk()
root.title("Warframe Market Checker")

root.tk.call('source', r'./forest-dark.tcl')
ttk.Style().theme_use('forest-dark')


tree_watcher,tree_sniping, button_start, button_end, button_update_list, clear_sniping, button_grab_update, start_watcher, stop_watcher, update_watcher_list, clear_watcher, button_update_priced_list, btn_status,button_update_watcher_file = create_gui(
    root,
    start_checking, stop_checking, update_checking_list, clear_sniping_results,
    grab_update_prices,
    start_watcher, stop_watcher, update_watcher_list, clear_watcher,
    update_checking_priced_list, toggle_status
)


root.after(100, lambda: process_sniping_queue(root, tree_sniping))
root.after(100, lambda: process_watcher_queue(root, tree_watcher))

root.mainloop()
