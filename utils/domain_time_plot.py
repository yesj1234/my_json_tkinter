from .constants import (
    DOMAIN_DISTRIBUTION_KO,
    DOMAIN_DISTRIBUTION_EN,
    DOMAIN_DISTRIBUTION_CH,
    DOMAIN_DISTRIBUTION_JP,
    TOTAL,
    TIME_TOTAL,
    YTICK_INFO_TIME
)
import numpy as np
from .decorators import try_decorator


def get_percent_time (category,total_time):
    domain, origin_lang, _ = category.split("_")
    if origin_lang in ["KO", "ko"]:
        return (total_time / (DOMAIN_DISTRIBUTION_KO[domain] * TIME_TOTAL)) * 100
    elif origin_lang in ["EN", "en"]:
        return (total_time / (DOMAIN_DISTRIBUTION_EN[domain] * TIME_TOTAL)) * 100
    elif origin_lang in ["JP", "jp"]:
        return (total_time / (DOMAIN_DISTRIBUTION_JP[domain] * TIME_TOTAL)) * 100
    else:
        return (total_time / (DOMAIN_DISTRIBUTION_CH[domain] * TIME_TOTAL)) * 100

def get_percent_time_label(category,current_time):
    domain, origin_lang, _ = category.split("_")
    if origin_lang in ["KO", "ko"]:
        return (f"{int(current_time / 3600)}({((current_time / (DOMAIN_DISTRIBUTION_KO[domain] * TIME_TOTAL)) * 100):0.2f})%")
    elif origin_lang in ["EN", "en"]:
        return (f"{int(current_time / 3600)}({((current_time / (DOMAIN_DISTRIBUTION_EN[domain] * TIME_TOTAL)) * 100):0.2f})%")
    elif origin_lang in ["JP", "jp"]:
        return (f"{int(current_time / 3600)}({((current_time / (DOMAIN_DISTRIBUTION_JP[domain] * TIME_TOTAL)) * 100):0.2f})%")
    else:
        return (f"{int(current_time / 3600)}({((current_time / (DOMAIN_DISTRIBUTION_CH[domain] * TIME_TOTAL)) * 100):0.2f})%")
@try_decorator
def domain_time_plot(x, y, percent, percent_label, plt, json_path, lang):
    y_pos = np.arange(len(x))
    y1 = [100 for _ in range(len(y))]
    
    fig = plt.figure(figsize=(15, 6))
    plt.barh(y_pos, y1, color="silver")  # 100% 배경
    barh_container = plt.barh(y_pos, percent, color="yellowgreen", label=True)  # 해당카테고리의 %
    plt.axvline(x=100, linestyle="--")  # 100% 수직 라인    
    plt.bar_label(barh_container, labels = percent_label)
    plt.title(f"카테고리분포(total: {int(TIME_TOTAL/3600)}시간)", fontsize=15)
    plt.xlabel("구축비율", fontsize=12)
    plt.ylabel("카테고리", fontsize=12)
    ytick_info = YTICK_INFO_TIME[lang]
    x = list(map(lambda x: x.split("_")[0], x))
    x = list(map(lambda x: x + f"\n({int(round(ytick_info[x][0], 0))}시간: {int(ytick_info[x][1])}%)", x))
    
    plt.yticks(y_pos, x)  # 건수와 % 는 상황에 맞게 조정되도록 수정하셈
    print("domain_time plot completed")
    fig.savefig(f"{json_path}/카테고리 분포(시간).png", transparent=False, dpi=80, bbox_inches="tight")  # 저장(요것도 수정하시고)
    return f"{json_path}/카테고리 분포(시간).png"