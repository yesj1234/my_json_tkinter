import numpy as np 
from .decorators import try_decorator
@try_decorator
def contents_voice_ratio_plot(x,y, percent, plt, json_path):
    fig, ax = plt.subplots(figsize=(15, 30)) # change the figsize manually
    y_pos = np.arange(len(x))
    # first axes to draw in all 100%
    y1 = [100 for _ in range(len(y))]
    ax.barh(y_pos, y1, height=0.6, align="center", color="silver")
    ax.set_yticks(y_pos, x)
    ax.set_xlabel("발화시간비율", fontsize = 12)
    ax.set_ylabel("컨텐츠", fontsize = 12)
    ax.set_title(label="컨텐츠 별 음성 발화 시간", fontsize=15)
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
    print("contents voice ratio plot completed")
    fig.savefig(f"{json_path}/컨텐츠 별 음성 발화 시간.png", transparent=False, dpi=80, bbox_inches="tight")
    return f"{json_path}/컨텐츠 별 음성 발화 시간.png"