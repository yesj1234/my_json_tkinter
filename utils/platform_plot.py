from .decorators import try_decorator
@try_decorator
def platform_plot(plt, sns, json_path, df):
    plt.figure(figsize = (15, 3))
    ax = sns.countplot(data = df, y="source", order = df['source'].value_counts().index) # draw a bar plot
    ax.bar_label(container = ax.containers[0]) # bar labeling
    ax.set_title("플랫폼 분포", fontsize = 15) # set title 
    ax.set_xlabel("건", fontsize = 12) # set x label 
    ax.set_ylabel("플랫폼 명", fontsize = 12) # set y label 
    # ax.set_xlim([0, 50000]) # set x axis limitations 
    fig = ax.get_figure()
    fig.savefig(f"{json_path}/플랫폼 분포.png", transparent=False, dpi=80, bbox_inches="tight") # save
    print("platform_plot completed")
    return f"{json_path}/플랫폼 분포.png"