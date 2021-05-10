from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns

def plot_numeric_features(df, numerical_features_list):
    import seaborn as sns
    sns.set()  # Setting seaborn as default style even if use only matplotlib
    sns.set_palette("Paired")  # set color palette
    fig, axes = plt.subplots(nrows=len(numerical_features_list),
                             ncols=2,
                             figsize=(10, 13))
    for i, feature in enumerate(numerical_features_list):
        sns.histplot(data=df, x=feature, kde=True, ax=axes[i, 0])
        sns.boxplot(data=df, x=feature, ax=axes[i, 1])
    plt.tight_layout()
    plt.show()


# Function to get statistics of all numerical features
def print_stat(df, numerical_features_list):
    for feature in numerical_features_list:
        print(
        """
        ** {} ** 
        ------------------------
        min:    {}  
        max:    {} 
        mean:   {:.1f} 
        median: {:.1f} 
        """.format(feature,
                   df[feature].min(),
                   df[feature].max(),
                   df[feature].mean(),
                   df[feature].median()))


def print_best_scores_movies(df, numeric_features):
    print("                              Movies with best scores".upper())
    print("""**************************************************************************************""")
    for feature in numeric_features:
        df.sort_values(by=feature, ascending=False, inplace=True, ignore_index=True)
        année = df.loc[0, 'year']
        titre = df.loc[0, 'title']
        realisateur = df.loc[0, 'directors']
        max_feature = df.loc[0, feature]

        print("""{:} ({:}) by {:} with  the highest {:} = {:}\n""".format(titre, année, ', '.join(realisateur),
                                                                           feature.replace('_', ' '), max_feature))


def create_transformed_df(old_df, elem_list, features_list):
    """elem_list should be in type list"""
    from statistics import mean
    new_dict = {}
    for index, elems in zip(old_df.index, old_df[elem_list]):
        for elem in elems:
            if elem in new_dict.keys():
                for j, feature in enumerate(features_list):
                    new_dict[elem][j].append(float(old_df.loc[index, feature]))
            else:
                new_dict[elem] = [[] for i in range(len(features_list))]
                for j, feature in enumerate(features_list):
                    new_dict[elem][j].append(float(old_df.loc[index, feature]))

    headers = [elem_list]
    for i in features_list:
        headers.append(f'avg_movie_{i}')
    headers.append('number_of_movies')  ##? how to name?

    new_df = pd.DataFrame(columns=headers)

    for key in new_dict:
        row = []
        row.append(key)
        for i, col in enumerate(headers[1:-1]):
            mean_val = mean(new_dict[key][i])
            row.append(mean_val)
        num = len(new_dict[key][0])
        row.append(num)

        length = len(new_df)
        new_df.loc[length] = row

    return new_df


## Plot top 20 with the highest rate/recette/movie_duration
def barplot_top_N(df, label, n_top):
    """
    Function to make barblot of the top N realisateur with the highest value of feature
    df = data frame
    features = list of names of columns
    n_top = number of names in final barblot
    """
    features = list(df.columns)
    features = features[1:]
    num_rows = len(features) // 2
    if len(features) % 2 == 1: num_rows += 1
    f, axes = plt.subplots(nrows=num_rows, ncols=2, figsize=(18, 10))
    for i, feature in enumerate(features):
        df_sorted = df.sort_values(by=feature,
                                   ascending=False,
                                   inplace=False,
                                   ignore_index=True)
        sns.barplot(data=df_sorted.head(n_top),
                    y=label,
                    x=feature,
                    ax=axes[i // 2, i % 2])
        min_rate = df_sorted[feature].min()
        max_rate = df_sorted[feature].max()
        # Add a legend and informative axis label
        axes[i // 2, i % 2].set(xlim=(min_rate, max_rate * 1.01),
                                xlabel=feature)  #, ylabel="",)
        sns.despine(left=True, bottom=True, ax=axes[i // 2, i % 2])
        axes[i // 2, i % 2].set_title(
            f"Top {n_top} {label} with the highest {feature} ", size=12)
    plt.subplots_adjust()
    plt.tight_layout()





