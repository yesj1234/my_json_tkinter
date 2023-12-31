from .constants import (
    DOMAIN_DISTRIBUTION_KO,
    DOMAIN_DISTRIBUTION_EN,
    DOMAIN_DISTRIBUTION_CH,
    DOMAIN_DISTRIBUTION_JP,
    TOTAL,
    TIME_TOTAL,
    YTICK_INFO
)
import numpy as np
import logging
import traceback
from .decorators import try_decorator

logger = logging.getLogger()

def get_percent(category,current_count):
    infos = category.split("_")
    domain, origin_lang = infos[0], infos[1]
    domain = domain.replace("/", ",")
    origin_lang = origin_lang.lower()
    try:
        if origin_lang == "ko":
            return current_count / (DOMAIN_DISTRIBUTION_KO[domain] * TOTAL) * 100
        elif origin_lang == "en":
            return current_count / (DOMAIN_DISTRIBUTION_EN[domain] * TOTAL) * 100
        elif origin_lang == "jp":
            return current_count / (DOMAIN_DISTRIBUTION_JP[domain] * TOTAL) * 100
        else:
            return current_count / (DOMAIN_DISTRIBUTION_CH[domain] * TOTAL) * 100
    except Exception:
        logger.error(traceback.print_exc())
        pass
    return False
def get_percent_label(category,current_count):
    infos = category.split("_")
    domain, origin_lang = infos[0], infos[1]
    domain = domain.replace("/", ",")
    origin_lang = origin_lang.lower()
    try:
        if origin_lang  == "ko":
            return (f"{current_count}({((current_count / (DOMAIN_DISTRIBUTION_KO[domain] * TOTAL)) * 100):0.2f})%")
        elif origin_lang  == "en":
            return (f"{current_count}({((current_count / (DOMAIN_DISTRIBUTION_EN[domain] * TOTAL)) * 100):0.2f})%")
        elif origin_lang  == "jp":
            return (f"{current_count}({((current_count / (DOMAIN_DISTRIBUTION_JP[domain] * TOTAL)) * 100):0.2f})%")
        else:
            return (f"{current_count}({((current_count / (DOMAIN_DISTRIBUTION_CH[domain] * TOTAL)) * 100):0.2f})%")
    except:
        logger.error(traceback.print_exc())
        pass
    return False
@try_decorator
def domain_plot(x, y, percent, percent_label, plt, json_path, lang):
    y_pos = np.arange(len(x))
    y1 = [100 for _ in range(len(y))]
    
    fig = plt.figure(figsize=(15, 6))
    plt.barh(y_pos, y1, color="silver")  # 100% 배경
    plt.barh(y_pos, percent, color="yellowgreen", label=True)  # 해당카테고리의 %
    plt.axvline(x=100, linestyle="--")  # 100% 수직 라인
    barh_container = plt.barh(y_pos, percent, color="yellowgreen", label=True)  # 해당카테고리의 %
    plt.bar_label(barh_container, labels = percent_label)

    plt.title(f"카테고리분포(total: {TOTAL}건)", fontsize=15)
    plt.xlabel("구축비율", fontsize=12)
    plt.ylabel("카테고리", fontsize=12)
    ytick_info = YTICK_INFO[lang]
    x = list(map(lambda x: x.split("_")[0], x))
    x = list(map(lambda x: x + f"\n({int(round(ytick_info[x][0], 0))}건: {int(ytick_info[x][1])}%)", x))
    
    plt.yticks(y_pos, x)  # 건수와 % 는 상황에 맞게 조정되도록 수정하셈
    print("domain plot completed")
    fig.savefig(f"{json_path}/카테고리 분포(문장).png", transparent=False, dpi=80, bbox_inches="tight")  # 저장(요것도 수정하시고)
    return f"{json_path}/카테고리 분포(문장).png"