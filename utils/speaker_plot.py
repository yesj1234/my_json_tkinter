def speaker_plot(plt, sns, json_path, df):
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