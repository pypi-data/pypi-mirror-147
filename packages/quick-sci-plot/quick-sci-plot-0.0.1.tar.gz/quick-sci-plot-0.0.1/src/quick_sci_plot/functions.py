import pandas as pd
from collections import OrderedDict
import seaborn as sns
import matplotlib.pyplot as plt

def sorted_to_ordered_dict(d,reverse=True):
    d = OrderedDict(sorted(d.items(), key=lambda obj: obj[1], reverse=reverse))
    return d

def plot_bar(dict_tags_count,x_label="Term", max_num=30, y_label="Count",vertical=False,save=False,save_path="",dpi=600,show=True):


    dict_tags_count=OrderedDict(sorted(dict_tags_count.items(), key=lambda obj: obj[1],reverse=True))
    # print()
    list_med_terms = []
    list_count = []
    # print(f"{x_label}\t{y_label}")
    for k in list(dict_tags_count.keys())[:max_num]:
        # print(f"{k}\t{dict_tags_count[k]}")
        list_med_terms.append(k)
        list_count.append(dict_tags_count[k])

    # print(line)
    d = {f'{x_label}': list_med_terms, f'{y_label}': list_count}
    df = pd.DataFrame(data=d)

    sns.set_style(style="whitegrid")
    ax=None
    if vertical:
        ax = sns.barplot(x=f"{x_label}", y=f"{y_label}", data=df)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
    else:
        ax = sns.barplot(x=f"{y_label}", y=f"{x_label}", data=df)
        plt.xlabel(y_label)
        plt.ylabel(x_label)

    plt.tight_layout()
    if save:
        plt.savefig(save_path, dpi=dpi)
    if show:
        plt.show()

def plot_reg(csv_path, metrics,sub_fig,save=False,save_folder="",x_label="number"):
    sns.set(style='ticks', font_scale=1.2)
    data = pd.read_csv(csv_path)

    for idx, metric in enumerate(metrics):
        sns.regplot(data=data, x=x_label, y=metric, order=3, marker="+")
        plt.title(sub_fig[idx], y=-0.22)
        plt.xlabel(x_label)
        plt.ylabel(metric)
        plt.tight_layout()
        if save:
            plt.savefig(f"{save_folder}/{metric}.jpg", dpi=600)
        plt.show()

