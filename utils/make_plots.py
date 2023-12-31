import pandas as pd
import json
import matplotlib.pyplot as plt 
import os
import seaborn as sns
import logging
import sys
import traceback
from utils.gender_plot import gender_plot
from utils.platform_plot import platform_plot
from utils.speaker_plot import speaker_plot
from utils.word_phrase_plot import (get_word_phrase, word_phrase_plot)
from utils.domain_plot import (get_percent, get_percent_label, domain_plot)
from utils.domain_time_plot import (get_percent_time, get_percent_time_label, domain_time_plot )
from utils.contents_voice_ratio_plot import contents_voice_ratio_plot


plt.style.use("ggplot")
plt.rc('font', family = 'Malgun Gothic')

logger = logging.getLogger()

def merge_same_categories(x, y):
  x = list(map(lambda x: x.replace("/", ","), x))
  x = list(map(lambda x: x.lower(), x))
  x_temp = list(map(lambda x: "_".join(x.split("_")[0:2]), x))
  x_temp_dict = {}
  for i, category_temp in enumerate(x_temp):
    if not x_temp_dict.get(category_temp):
      x_temp_dict[category_temp] = y[i]
    else:
      x_temp_dict[category_temp] += y[i]
  return list(x_temp_dict.keys()), list(x_temp_dict.values()) 

def make_plots(json_path, lang, **kwargs):
    plot_paths = []
    # ��ü ������ �޾ƿ���    
    
    if kwargs:
        logger.info(f"kwargs: {kwargs}")
        df = pd.read_csv(kwargs["csv_file_path"])
    
    if json_path:
        logger.info(f"json_path: {json_path}")
        jsons = [] 
        for root, dir, files in os.walk(json_path):
            if files:
                for file in files:
                    _, ext = os.path.splitext(file)
                    if ext == ".json":
                        with open(os.path.join(root, file), "r+", encoding="utf-8") as f:
                            try:
                                json_file = json.load(f)
                                jsons.append(json_file)
                            except Exception as e:
                                logger.warning(e)
                                logger.error(os.path.join(root, file))
        df = pd.DataFrame(jsons)
        df.to_csv(f"{json_path}/file.csv", mode="w", encoding="utf-8")
    
    # ���� ���� �׷���
    try:
        gender_plot(plt, sns, json_path, df)
    except Exception:
       logger.error(traceback.print_exc())
       pass 
    
    # �÷��� ���� �׷���
    try:
        platform_plot(plt, sns, json_path, df)
    except Exception:
       logger.error(traceback.print_exc())
       pass
    
    #ȭ�ڼ� ���� �׷���
    try:
        speaker_plot(plt, sns, json_path, df)
    except Exception:
       logger.error(traceback.print_exc())
       pass
    
    #������ ���� �׷��� 
    try:
        df["tc_text_len"] = df[["origin_lang", "tc_text"]].apply(lambda row : get_word_phrase(row["origin_lang"], row["tc_text"]), axis=1)
        word_phrase_plot(plt, sns, json_path, df)
    except Exception:
       logger.info(traceback.print_exc())
       pass
    
    try:
        #ī�װ���(���� ����) ���� �׷���
        domain_data = df["category"].value_counts().sort_values() # sort in ascending order
        domain_plot_x = domain_data.keys()
        domain_plot_y = domain_data.values
        domain_plot_x, domain_plot_y = merge_same_categories(x = domain_plot_x, y = domain_plot_y)
        percent = []
        percent_label = []
        for category, count in zip(domain_plot_x, domain_plot_y):
            percent_data = get_percent(category, count)
            percent_label_data = get_percent_label(category, count)
            if percent_data and percent_label_data:
                percent.append(get_percent(category, count))
                percent_label.append(get_percent_label(category, count))
            else:
                pass
        domain_plot(x = domain_plot_x, y = domain_plot_y, percent =percent, percent_label=percent_label, plt=plt, json_path=json_path, lang=lang)
        #ī�װ���(�ð� ����) ���� �׷���
    except Exception:
       logger.error(traceback.print_exc())
       pass
    
    try:     
        categories = df["category"].unique()
        categories_dict = {key:0 for key in categories}
        contentsIdx = df["contentsIdx"].unique()
        for idx in contentsIdx:
            temp = df.loc[df["contentsIdx"] == idx].iloc[0]
            cat = temp["category"]
            total = temp["li_total_voice_time"]
            categories_dict[cat] += float(total)
        domain_time_plot_x = list(categories_dict.keys())
        domain_time_plot_y = list(categories_dict.values())
        domain_time_plot_x, domain_time_plot_y = merge_same_categories(x = domain_time_plot_x, y = domain_time_plot_y)
        percent_time = []
        percent_time_label = []
        for category, total_time in zip(domain_time_plot_x, domain_time_plot_y):
            percent_time_data = get_percent_time(category, total_time)
            percent_time_label_data = get_percent_time_label(category, round(total_time, 2))
            if percent_time_data and percent_time_label_data:
                percent_time.append(get_percent_time(category, total_time))
                percent_time_label.append(get_percent_time_label(category, round(total_time, 2)))
            else:
                pass    
        domain_time_plot(x = domain_time_plot_x, y = domain_time_plot_y, percent=percent_time, percent_label=percent_time_label, plt = plt, json_path = json_path, lang=lang)
    except Exception:
       logger.error(traceback.print_exc())
       pass
   
   #�������� ���� ��ȭ ���� �׷���
    try:
        contentsList = df["contentsIdx"].unique()
        pairs = []
        for idx in contentsList:
            temp = df.loc[df["contentsIdx"] == idx].iloc[0]
            _, video_time, voice_time = temp["contentsIdx"],temp["li_total_video_time"], temp["li_total_voice_time"]
            ratio = round((float(voice_time) / float(video_time)) * 100, 2) 
            pairs.append((idx, ratio))
        pairs.sort(key = lambda x: int(x[0]))
        contents = list(map(lambda x: x[0], pairs))
        ratios = list(map(lambda x : x[1], pairs))
        contents_voice_ratio_plot(x = contents, y = ratios, percent = ratios, plt = plt, json_path = json_path)
    except Exception as e:
        logger.warning(e)
        pass     
    
if __name__ == "__main__":
    import argparse
   
    parser = argparse.ArgumentParser()
    parser.add_argument("--json_path", help="json folder path", default="")
    parser.add_argument("--lang", help="en ko ja zh")
    parser.add_argument("--csv_file_path", default = "")
    args = parser.parse_args()
    make_plots(json_path = args.json_path,lang = args.lang, csv_file_path = args.csv_file_path)
    