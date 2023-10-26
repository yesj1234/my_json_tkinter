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



def make_plots(json_path, lang):
    plot_paths = []
    # 전체 데이터 받아오기    
    if json_path:
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
        # df.to_csv(f"{json_path}/file.csv", mode="w", encoding="utf-8")
    
    # 성별 분포 그래프
    gender_plot(plt, sns, json_path, df)
    # 플랫폼 분포 그래프
    platform_plot(plt, sns, json_path, df)
    #화자수 분포 그래프
    speaker_plot(plt, sns, json_path, df)
    #음절수 분포 그래프 
    df["tc_text_len"] = df[["origin_lang", "tc_text"]].apply(lambda row : get_word_phrase(row["origin_lang"], row["tc_text"]), axis=1)
    word_phrase_plot(plt, sns, json_path, df)

    #카테고리(문장 기준) 분포 그래프
    domain_data = df["category"].value_counts().sort_values() # sort in ascending order
    domain_plot_x = domain_data.keys()
    domain_plot_y = domain_data.values
    percent = []
    percent_label = []
    for category, count in zip(domain_plot_x, domain_plot_y):
        percent.append(get_percent(category, count))
        percent_label.append(get_percent_label(category, count))
    domain_plot(x = domain_plot_x, y = domain_plot_y, percent =percent, percent_label=percent_label, plt=plt, json_path=json_path, lang=lang)
    #카테고리(시간 기준) 분포 그래프
    categories = df["category"].unique()
    categories_dict = {key:0 for key in categories}
    contentsIdx = df["contentsIdx"].unique()
    for idx in contentsIdx:
        temp = df.loc[df["contentsIdx"] == idx].iloc[0]
        cat, id, total = temp["category"], temp["contentsIdx"], temp["li_total_voice_time"]
        categories_dict[cat] += float(total)
    domain_time_plot_x = list(categories_dict.keys())
    domain_time_plot_y = list(categories_dict.values())
    percent_time = []
    percent_time_label = []
    for category, total_time in zip(domain_time_plot_x, domain_time_plot_y):
        percent_time.append(get_percent_time(category, total_time))
        percent_time_label.append(get_percent_time_label(category, round(total_time, 2)))
        
    domain_time_plot(x = domain_time_plot_x, y = domain_time_plot_y, percent=percent_time, percent_label=percent_time_label, plt = plt, json_path = json_path, lang=lang)
   
   #콘텐츠별 음성 발화 비율 그래프
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
    