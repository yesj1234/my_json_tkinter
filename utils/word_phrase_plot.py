def get_word_phrase(origin_lang, tc_text):
    if origin_lang == "한국어" or origin_lang == "영어":
        return len(tc_text.strip().split(" "))
    else:
        return len(tc_text)
        
def word_phrase_plot(plt, sns, json_path, df):
    plt.figure(figsize = (20, 15))
    ax = sns.countplot(data = df, y="tc_text_len", order = df['tc_text_len'].value_counts().index.sort_values(ascending=False)) # draw a bar plot
    ax.bar_label(container = ax.containers[0]) # bar labeling
    ax.set_xlabel("건", fontsize = 12)
    ax.set_ylabel("어절 수", fontsize = 12)
    ax.set_title(label="전사텍스트 어절 수 분포", fontsize=15)
    fig = ax.get_figure()
    fig.savefig(f"{json_path}/전사텍스트어절수분포.png", transparent=False, dpi=80, bbox_inches="tight") # save
    return f"{json_path}/전사텍스트어절수분포.png"