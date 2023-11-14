import pandas as pd
import json
import matplotlib.pyplot as plt 
import os
import seaborn as sns
import logging
import sys
from .gender_plot import gender_plot
from .platform_plot import platform_plot
from .speaker_plot import speaker_plot
from .word_phrase_plot import (get_word_phrase, word_phrase_plot)
from .domain_plot import (get_percent, get_percent_label, domain_plot)
from .domain_time_plot import (get_percent_time, get_percent_time_label, domain_time_plot )
from .contents_voice_ratio_plot import contents_voice_ratio_plot


plt.style.use("ggplot")
plt.rc('font', family = 'Malgun Gothic')

logger = logging.getLogger("make_plots_logger")
logger.setLevel(logging.INFO)
streamhandler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamhandler.setFormatter(formatter)
logger.addHandler(streamhandler)
filehandler = logging.FileHandler("../error_file.log")
filehandler.setFormatter(formatter)
filehandler.setLevel(logging.ERROR)
logger.addHandler(filehandler)



def make_plots(json_path, lang, **kwargs):
    plot_paths = []
    # ��ü ������ �޾ƿ���    
    print(kwargs)
    if kwargs["csv_file_path"]:
        df = pd.read_csv(kwargs["csv_file_path"])
    
    if json_path and not kwargs["csv_file_path"]:
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
    except Exception as e:
        logger.warning(e)
        pass 
    
    # �÷��� ���� �׷���
    try:
        platform_plot(plt, sns, json_path, df)
    except Exception as e:
        logger.warning(e)
        pass
    
    #ȭ�ڼ� ���� �׷���
    try:
        speaker_plot(plt, sns, json_path, df)
    except Exception as e:
        logger.warning(e)
        pass
    
    #������ ���� �׷��� 
    try:
        df["tc_text_len"] = df[["origin_lang", "tc_text"]].apply(lambda row : get_word_phrase(row["origin_lang"], row["tc_text"]), axis=1)
        word_phrase_plot(plt, sns, json_path, df)
    except Exception as e:
        logger.warning(e)
        pass
    
    try:
        #ī�װ���(���� ����) ���� �׷���
        domain_data = df["category"].value_counts().sort_values() # sort in ascending order
        domain_plot_x = domain_data.keys()
        domain_plot_y = domain_data.values
        percent = []
        percent_label = []
        for category, count in zip(domain_plot_x, domain_plot_y):
            percent.append(get_percent(category, count))
            percent_label.append(get_percent_label(category, count))
        domain_plot(x = domain_plot_x, y = domain_plot_y, percent =percent, percent_label=percent_label, plt=plt, json_path=json_path, lang=lang)
        #ī�װ���(�ð� ����) ���� �׷���
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
        percent_time = []
        percent_time_label = []
        for category, total_time in zip(domain_time_plot_x, domain_time_plot_y):
            percent_time.append(get_percent_time(category, total_time))
            percent_time_label.append(get_percent_time_label(category, round(total_time, 2)))
            
        domain_time_plot(x = domain_time_plot_x, y = domain_time_plot_y, percent=percent_time, percent_label=percent_time_label, plt = plt, json_path = json_path, lang=lang)
    except Exception:
       logger.exception("message")
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
    