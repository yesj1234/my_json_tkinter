import pandas as pd
import json
import matplotlib.pyplot as plt 
import numpy as np 
import os
import argparse
import seaborn as sns

plt.style.use("ggplot")
plt.rc('font', family = 'Malgun Gothic')

def make_plots(json_path):
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
                            json_file = json.load(f)
                            jsons.append(json_file)
        
        df = pd.DataFrame(jsons)
        df.to_csv(f"{json_path}/file.csv", mode="w", encoding="utf-8")
    
    def gender_plot(df):
        plt.figure(figsize = (15, 3))
        ax = sns.countplot(data = df, y="speaker_gender") # draw a bar plot
        ax.bar_label(container = ax.containers[0]) # bar labeling
        ax.set_title("성별 분포", fontsize = 15) # set title 
        ax.set_xlabel("명", fontsize = 12) # set x label 
        ax.set_ylabel("성별", fontsize = 12) # set y label 
        # ax.set_xlim([0, 50000]) # set x axis limitations 
        fig = ax.get_figure()
        fig.savefig(f"{json_path}/성별분포.png", transparent=False, dpi=80, bbox_inches="tight") # save
        return f"{json_path}/성별분포.png"
    gender_plot_path = gender_plot(df)
    plot_paths.append(gender_plot_path)
    
    def platform_plot(df):
        plt.figure(figsize = (15, 3))
        ax = sns.countplot(data = df, y="source", order = df['source'].value_counts().index) # draw a bar plot
        ax.bar_label(container = ax.containers[0]) # bar labeling
        ax.set_title("플랫폼 분포", fontsize = 15) # set title 
        ax.set_xlabel("건", fontsize = 12) # set x label 
        ax.set_ylabel("플랫폼 명", fontsize = 12) # set y label 
        # ax.set_xlim([0, 50000]) # set x axis limitations 
        fig = ax.get_figure()
        fig.savefig(f"{json_path}/플랫폼 분포.png", transparent=False, dpi=80, bbox_inches="tight") # save
        return f"{json_path}/플랫폼 분포.png"
    platform_plot_path = platform_plot(df)
    plot_paths.append(platform_plot_path)
    
    def speaker_plot(df):
        plt.figure(figsize = (15, 3))
        ax = sns.countplot(data = df, y="li_total_speaker_num", order = df['li_total_speaker_num'].value_counts().index) # draw a bar plot
        ax.bar_label(container = ax.containers[0]) # bar labeling
        ax.set_xlabel("건", fontsize = 12)
        ax.set_ylabel("화자수 (명)", fontsize = 12)
        ax.set_title(label="화자 규모 분포", fontsize=15) 
        # ax.set_xlim([0, 50000]) # set x axis limitations 
        fig = ax.get_figure()
        fig.savefig(f"{json_path}/화자규모분포.png", transparent=False, dpi=80, bbox_inches="tight") # save
        return f"{json_path}/화자규모분포.png"
    speaker_plot_path = speaker_plot(df)
    plot_paths.append(speaker_plot_path)
    
    def get_word_phrase(origin_lang, tc_text):
        if origin_lang == "한국어" or origin_lang == "영어":
            return len(tc_text.strip().split(" "))
        else:
            return len(tc_text)

    df["tc_text_len"] = df[["origin_lang", "tc_text"]].apply(lambda row : get_word_phrase(row["origin_lang"], row["tc_text"]), axis=1)

    def word_phrase_plot(df):
        plt.figure(figsize = (20, 15))
        ax = sns.countplot(data = df, y="tc_text_len", order = df['tc_text_len'].value_counts().index) # draw a bar plot
        ax.bar_label(container = ax.containers[0]) # bar labeling
        ax.set_xlabel("건", fontsize = 12)
        ax.set_ylabel("어절 수", fontsize = 12)
        ax.set_title(label="전사텍스트 어절 수 분포", fontsize=15)
        fig = ax.get_figure()
        fig.savefig(f"{json_path}/전사텍스트어절수분포.png", transparent=False, dpi=80, bbox_inches="tight") # save
        return f"{json_path}/전사텍스트어절수분포.png"
    word_phrase_plot_path = word_phrase_plot(df)
    plot_paths.append(word_phrase_plot_path)
    
    DOMAIN_DISTRIBUTION_KO = {
        "일상,소통": 0.2,
        "여행": 0.15,
        "게임": 0.15,
        "경제": 0.05,
        "교육": 0.05,
        "스포츠": 0.05,
        "라이브커머스": 0.15,
        "음식,요리": 0.2
    }
    DOMAIN_DISTRIBUTION_EN = {
        "일상,소통": 0.2,
        "여행": 0.2,
        "게임": 0.2,
        "음식,요리": 0.2,
        "운동,건강": 0.2
    }
    DOMAIN_DISTRIBUTION_CH = {
        "일상,소통": 0.2,
        "여행": 0.2,
        "게임": 0.2,
        "라이브커머스": 0.2,
        "패션,뷰티": 0.2
    }
    DOMAIN_DISTRIBUTION_JP = {
        "일상,소통": 0.2,
        "여행": 0.2,
        "게임": 0.2,
        "음식,요리": 0.2,
        "패션,뷰티": 0.2
    }
    TOTAL = 400000 # 40만 문장

    def get_percent(category,current_count):
        domain, origin_lang, _ = category.split("_")
        if origin_lang in ["KO", "ko"]:
            return (current_count / (DOMAIN_DISTRIBUTION_KO[domain] * TOTAL)) * 100
        elif origin_lang in ["EN", "en"]:
            return (current_count / (DOMAIN_DISTRIBUTION_EN[domain] * TOTAL)) * 100
        elif origin_lang in ["JP", "jp"]:
            return (current_count / (DOMAIN_DISTRIBUTION_JP[domain] * TOTAL)) * 100
        else:
            return (current_count / (DOMAIN_DISTRIBUTION_CH[domain] * TOTAL)) * 100

    domain_data = df["category"].value_counts().sort_values() # sort in ascending order
    domain_plot_x = domain_data.keys()
    domain_plot_y = domain_data.values
    percent = []
    for category, count in zip(domain_plot_x, domain_plot_y):
        percent.append(get_percent(category, count))


    def domain_plot(x,y, percent):
        fig, ax = plt.subplots(figsize=(15, 3)) # change the figsize manually
        y_pos = np.arange(len(x))
        # first axes to draw in all 100%
        y1 = [100 for _ in range(len(y))]
        ax.barh(y_pos, y1, height=0.6, align="center", color="silver")
        ax.set_yticks(y_pos, x)
        ax.set_xlabel("구축 비율", fontsize = 12)
        ax.set_ylabel("카테고리", fontsize = 12)
        ax.set_title(label="카테고리 분포", fontsize=15)
        x_labels = ax.get_xticklabels() # ax.set_xticklabels()
        y_labels = ax.get_yticklabels() # ax.set_yticklabels()
        plt.setp(x_labels, fontsize= 10) # 혹은 setp 로 여러 설정 한번에 하기
        plt.setp(y_labels, fontsize = 10) # 혹은 setp로 여러 설정 한번에 하기
        # second axes sharing the xaxis
        ax2 = ax.twinx()
        bar_container = ax2.barh(y_pos, percent, height=0.6, align="center", color="yellowgreen")
        ax2.set_yticks([])
        ax2.bar_label(bar_container, label=percent, fmt="{:,.2f}%",fontsize= 10, label_type = "center")
        plt.axvline(x = 100, linestyle = "--")
        plt.rcParams.update({"figure.autolayout": True})
        fig.savefig(f"{json_path}/카테고리 분포.png", transparent=False, dpi=80, bbox_inches="tight") # 저장
        return f"{json_path}/카테고리 분포.png" 
    domain_plot_path = domain_plot(x = domain_plot_x,y = domain_plot_y, percent =percent)
    plot_paths.append(domain_plot_path)
    return plot_paths