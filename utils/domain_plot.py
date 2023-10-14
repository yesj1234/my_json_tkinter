from .constants import (
    DOMAIN_DISTRIBUTION_KO,
    DOMAIN_DISTRIBUTION_EN,
    DOMAIN_DISTRIBUTION_CH,
    DOMAIN_DISTRIBUTION_JP,
    TOTAL,
    TIME_TOTAL
)
import numpy as np
def get_percent(category,current_count):
    domain, origin_lang, _ = category.split("_")
    if origin_lang in ["KO", "ko"]:
        return current_count / (DOMAIN_DISTRIBUTION_KO[domain] * TOTAL) * 100
    elif origin_lang in ["EN", "en"]:
        return current_count / (DOMAIN_DISTRIBUTION_EN[domain] * TOTAL) * 100
    elif origin_lang in ["JP", "jp"]:
        return current_count / (DOMAIN_DISTRIBUTION_JP[domain] * TOTAL) * 100
    else:
        return current_count / (DOMAIN_DISTRIBUTION_CH[domain] * TOTAL) * 100
    
def get_percent_label(category,current_count):
    domain, origin_lang, _ = category.split("_")
    if origin_lang in ["KO", "ko"]:
        return (f"{current_count}({((current_count / (DOMAIN_DISTRIBUTION_KO[domain] * TOTAL)) * 100):0.2f})%")
    elif origin_lang in ["EN", "en"]:
        return (f"{current_count}({((current_count / (DOMAIN_DISTRIBUTION_EN[domain] * TOTAL)) * 100):0.2f})%")
    elif origin_lang in ["JP", "jp"]:
        return (f"{current_count}({((current_count / (DOMAIN_DISTRIBUTION_JP[domain] * TOTAL)) * 100):0.2f})%")
    else:
        return (f"{current_count}({((current_count / (DOMAIN_DISTRIBUTION_CH[domain] * TOTAL)) * 100):0.2f})%")

def domain_plot(x, y, percent, percent_label, plt, json_path):
    y_pos = np.arange(len(x))
    y1 = [100 for _ in range(len(y))]
    
    fig = plt.figure(figsize=(15, 3))
    plt.barh(y_pos, y1, color="silver")  # 100% 배경
    plt.barh(y_pos, percent, color="yellowgreen", label=True)  # 해당카테고리의 %
    plt.axvline(x=100, linestyle="--")  # 100% 수직 라인
    for i, v in enumerate(percent):  # 레이블링(색이랑 그런건 조정하셈)
        plt.text(v / 2, 0, percent_label[i],
                fontsize=9,
                color='blue',
                horizontalalignment='center',
                verticalalignment='bottom')

    plt.title(f"카테고리분포(total: {TOTAL}건)", fontsize=15)
    plt.xlabel("구축비율", fontsize=12)
    plt.ylabel("카테고리", fontsize=12)
    ytick_info = {
        "일상,소통": (TOTAL * 0.2, 20),
        "여행": (TOTAL * 0.15, 15),
        "게임": (TOTAL * 0.15, 15),
        "경제": (TOTAL * 0.05, 5),
        "교육": (TOTAL * 0.2, 5),
        "스포츠": (TOTAL * 0.05, 5),
        "라이브커머스": (TOTAL * 0.15, 15),
        "음식,요리": (TOTAL * 0.2, 20)
    }
    x = list(map(lambda x: x.split("_")[0], x))
    x = list(map(lambda x: x + f"\n({int(round(ytick_info[x][0], 0))}건: {int(ytick_info[x][1])}%)", x))
    
    plt.yticks(y_pos, x)  # 건수와 % 는 상황에 맞게 조정되도록 수정하셈

    fig.savefig(f"{json_path}/카테고리 분포(문장).png", transparent=False, dpi=80, bbox_inches="tight")  # 저장(요것도 수정하시고)
    