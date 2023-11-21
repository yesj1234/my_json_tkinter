from tkinter import filedialog
import tkinter as tk 
import tkinter.ttk as ttk
from utils.make_plots import make_plots
from utils.validate_jsons import validate_jsons
import logging
import logging.config
import sys
import json
import os 
import traceback

seperator = os.sep 
with open(os.path.join("C:\\" "Users","승준","Downloads","my_json_tkinter","logger_config.json"), mode="r+", encoding="utf-8") as config_file:
    config = json.load(config_file)
    logging.config.dictConfig(config)
    logger = logging.getLogger(__name__)

class MyJsonValidator:
    def __init__(self, window):
        window.title("json_validator")
        window.geometry("500x350")
        # setting up the main frame
        mainframe = ttk.Frame(window, borderwidth=5, relief='ridge', width=500, height=350)
        mainframe.grid(column=0, row=0, sticky="nwes")
        window.columnconfigure(0, weight = 1)
        window.rowconfigure(0, weight = 1)
        mainframe.columnconfigure(0, weight=3)
        mainframe.columnconfigure(1, weight=1)
        
        # selecting folder path 
        global folder_path 
        folder_path = tk.StringVar()
        folder_path_label = ttk.Label(mainframe, 
                                      textvariable=folder_path,
                                      background="white",
                                      foreground="black",
                                      width=50)
        folder_path_label.grid(row=0, column=0, sticky="nwes")
        folder_select_button = ttk.Button(mainframe, text="Browse", command=self.select_path)
        folder_select_button.grid(row=0, column=1, sticky="nwes")
        # confirm the selected path and with the jsons inside the selected path 
        # make plots and validate the jsons. 
        confirm_button = ttk.Button(mainframe, text="Ok", command=self.confirm_callback)
        confirm_button.grid(row=1, column=1, sticky="news")
        
        # selecting language pair with radio button
        global var
        var = tk.StringVar()
        values = {
            "한국어": "ko",
            "일본어": "ja",
            "중국어": "zh",
            "영  어": "en"
        }
        for text, value in values.items():
            tk.Radiobutton(mainframe, text = text, variable=var,value=value, indicator = 0, background="light blue").grid(column=1)
        
    def select_path(self): 
        folder_path.set(filedialog.askdirectory())
    
        
    def confirm_callback(self): 
        json_path = folder_path.get()
        lang = var.get()
        try:
            logger.info(f"generating plots with jsons in {json_path}")
            logger.info(f"Current selected source language is {lang}")
            make_plots(json_path = json_path, lang = lang)
            # logger.info(plots)
        except Exception:
            logger.error(traceback.print_exc())
            pass
        # try:
        #     validate_jsons(json_dir = json_path)
        # except Exception as e:
        #     print(e)
        #     pass

#1. root 
window = tk.Tk()
MyJsonValidator(window)
window.mainloop()


