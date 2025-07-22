import matplotlib.pyplot as plt
import seaborn as sns

def create_chart(data, x_column, y_column, title):
    plt.figure(figsize=(6,4))
    sns.set_style("whitegrid")
    ax = sns.barplot(x=x_column, y=y_column, data=data, hue=x_column, palette="Blues_d")
    plt.title(title, fontsize=12)
    # plt.title(title, fontsize=12, fontweight='bold')
    plt.xlabel(x_column.capitalize(), fontsize=11)
    plt.ylabel(y_column, fontsize=11)
    # plt.xticks(rotation=45)
    for bars in ax.containers:
        ax.bar_label(bars,fontsize=10,fmt='{:,.0f}' )
        # ax.bar_label(bars,fontsize=10, label_type='center')
    plt.tight_layout()
    # Save to BytesIO object
    from io import BytesIO
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
    img_buffer.seek(0)
    return img_buffer