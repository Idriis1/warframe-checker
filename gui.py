import tkinter as tk
from tkinter import ttk, messagebox
from market_checker import copy_to_clipboard, toggle_sound, toggle_status,update_watcher_list,copy_to_clipboard2
import webbrowser

def open_link(url):
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"Failed to open link: {e}")


def create_gui(root,
               start_checking, stop_checking, update_checking_list, clear_sniping_results,
               grab_update_prices,
               start_watcher, stop_watcher, update_watcher_list, clear_watcher,
               update_checking_priced_list, toggle_status):
    # Create a notebook (tabs container)
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True)

    # Create tabs
    frame_sniping = ttk.Frame(notebook)
    frame_pricing = ttk.Frame(notebook)
    frame_watcher = ttk.Frame(notebook)
    frame_settings = ttk.Frame(notebook)
    frame_about = ttk.Frame(notebook)
    notebook.add(frame_sniping, text='Sniping')
    notebook.add(frame_pricing, text='Pricing')
    notebook.add(frame_watcher, text='Watcher')
    notebook.add(frame_settings, text='Settings')
    notebook.add(frame_about, text='About')

    # Create Sniping tab
    frame_hits_sniping = tk.Frame(frame_sniping, relief=tk.SUNKEN, borderwidth=2)
    frame_hits_sniping.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    tree_sniping = ttk.Treeview(frame_hits_sniping, columns=("Market Hits",), show="headings", height=10)
    tree_sniping.heading("Market Hits", text="Market Hits")
    tree_sniping.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def on_double_click(event):
        copy_to_clipboard(tree_sniping, root)
        
    tree_sniping.bind("<Double-1>", on_double_click)

    frame_buttons_sniping = ttk.Frame(frame_sniping)
    frame_buttons_sniping.pack(pady=10)
    button_start = ttk.Button(frame_buttons_sniping, text="Start", command=lambda: start_checking(button_start, tk.DISABLED))
    button_start.pack(side=tk.LEFT, padx=10)
    button_end = ttk.Button(frame_buttons_sniping, text="End", command=lambda: stop_checking(button_start, tk.NORMAL))
    button_end.pack(side=tk.LEFT, padx=10)
    button_update_list = ttk.Button(frame_buttons_sniping, text="Update List", command=update_checking_list)
    button_update_list.pack(side=tk.LEFT, padx=10)
    clear_sniping = ttk.Button(frame_buttons_sniping, text="Clear", command=lambda: clear_sniping_results(tree_sniping))
    clear_sniping.pack(side=tk.LEFT, padx=10)

    # Create Pricing tab
    frame_pricing_content = tk.Frame(frame_pricing)
    frame_pricing_content.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    text_pricing = tk.Text(frame_pricing_content, wrap=tk.WORD, height=15, width=80)
    text_pricing.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    frame_buttons_pricing = tk.Frame(frame_pricing)
    frame_buttons_pricing.pack(pady=10)
    button_grab_update = ttk.Button(frame_buttons_pricing, text="Grab & Update Price", style="Accent.TButton", command=lambda: grab_update_prices(text_pricing, tk.END, tk.NORMAL, tk.DISABLED))
    button_grab_update.pack(padx=10, pady=5)

    # Create Watcher tab
    label_watcher = tk.Label(frame_watcher, text="Watcher will take last 2 result per item. Watcher runs every minute.", justify=tk.CENTER)
    label_watcher.pack(padx=10, pady=10)
    tree_watcher = ttk.Treeview(frame_watcher, columns=(1,2,3,4,5),height=5, show="headings")
    tree_watcher.pack()
    tree_watcher.heading(1, text="Player")
    tree_watcher.heading(2, text="Price")
    tree_watcher.heading(3, text="Item")
    tree_watcher.heading(4, text="Quantity")
    tree_watcher.heading(5, text="Rank")
    tree_watcher.column(1, width=100)
    tree_watcher.column(2, width=100)
    tree_watcher.column(3, width=100)
    tree_watcher.column(4, width=100)
    tree_watcher.column(5, width=100)
    scroll = ttk.Scrollbar(frame_watcher, orient="vertical", command=tree_watcher.yview)
    scroll.pack(side='right', fill='y')
    tree_watcher.configure(yscrollcommand=scroll.set)

    def on_double_click2(event):
        copy_to_clipboard2(tree_watcher, root)
        
    tree_watcher.bind("<Double-1>", on_double_click2)

    frame_buttons_watcher = ttk.Frame(frame_watcher)
    frame_buttons_watcher.pack(pady=10)
    btn_watcher_start = ttk.Button(frame_buttons_watcher, text="Start Watcher", command=lambda: start_watcher(btn_watcher_start, tk.DISABLED))
    btn_watcher_start.pack(side=tk.LEFT, padx=10)
    btn_watcher_end = ttk.Button(frame_buttons_watcher, text="Stop Watcher", command=lambda: stop_watcher(btn_watcher_start, tk.NORMAL))
    btn_watcher_end.pack(side=tk.LEFT, padx=10)
    btn_update_watcher_list = ttk.Button(frame_buttons_watcher, text="Update Watcher", command=update_watcher_list)
    btn_update_watcher_list.pack(side=tk.LEFT, padx=10)
    btn_clear_watcher = ttk.Button(frame_buttons_watcher, text="Clear Watcher", command=lambda: clear_watcher(tree_watcher))
    btn_clear_watcher.pack(side=tk.LEFT, padx=10)

    # Create Settings tab
    frame_settings_content = tk.Frame(frame_settings)
    frame_settings_content.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    button_toggle_sound = ttk.Checkbutton(frame_settings_content, text="Sound: ON", command=lambda: toggle_sound(button_toggle_sound), style="Switch")
    button_toggle_sound.pack(side=tk.LEFT, padx=10)
    btn_status = ttk.Checkbutton(frame_settings_content, text="Orders Type: Sell", command=lambda: toggle_status(btn_status), style="Switch")
    btn_status.pack(side=tk.RIGHT, padx=10)
    button_update_list_file = ttk.Button(frame_settings_content, text="Update list.txt", command=update_checking_list)
    button_update_list_file.pack(pady=5)
    button_update_priced_list = ttk.Button(frame_settings_content, text="Update priced-list.txt", command=update_checking_priced_list)
    button_update_priced_list.pack(pady=5)
    button_update_watcher_file = ttk.Button(frame_settings_content, text="Update watcher.txt", command=update_watcher_list)
    button_update_watcher_file.pack(pady=5)




    # About tab


    # Frame for the about text
    frame_about_text = ttk.Frame(frame_about)
    frame_about_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    button_toggle_sound = ttk.Checkbutton(frame_about_text, text="Sound: ON", command=lambda: toggle_sound(button_toggle_sound), style="Switch")

    # frame_about_text.pack(pady=10, padx=10)

    about_label = ttk.Label(
        frame_about_text,
        text="""
        This app under development.
        Account in-game : andy31337
        """,
        wraplength=400,
        justify="center",
        padding=5
    )
    about_label.pack()
    frame_contact_links = ttk.Frame(frame_about)
    frame_contact_links.pack(pady=10)
    btn_email = ttk.Button(
        frame_contact_links,
        text="Email Me",
        command=lambda: open_link("mailto:alwwd25@gmail.com")
    )
    btn_email.pack(side=tk.LEFT, padx=5)

    btn_github = ttk.Button(
        frame_contact_links,
        text="Check GitHub",
        command=lambda: open_link("https://github.com/Idriis1/warframe-checker")
    )
    btn_github.pack(side=tk.LEFT, padx=5)

    return (tree_watcher,tree_sniping, button_start, button_end, button_update_list, clear_sniping, button_grab_update, btn_watcher_start, btn_watcher_end, btn_update_watcher_list, btn_clear_watcher, button_update_priced_list, btn_status,button_update_watcher_file)


# def process_queue(root, tree_sniping):
#     from market_checker import queue, update_sniping_tab
#     while not queue.empty():
#         item = queue.get_nowait()
#         update_sniping_tab(tree_sniping, *item)
#     root.after(100, lambda: process_queue(root, tree_sniping))
def process_sniping_queue(root, tree_sniping):
    from market_checker import sniping_queue, update_sniping_tab
    while not sniping_queue.empty():
        item = sniping_queue.get_nowait()
        update_sniping_tab(tree_sniping, *item)
    root.after(100, lambda: process_sniping_queue(root, tree_sniping))

def process_watcher_queue(root, tree_watcher):
    from market_checker import watcher_queue, update_watcher_tab
    while not watcher_queue.empty():
        item = watcher_queue.get_nowait()
        update_watcher_tab(tree_watcher, *item)
    root.after(100, lambda: process_watcher_queue(root, tree_watcher))
