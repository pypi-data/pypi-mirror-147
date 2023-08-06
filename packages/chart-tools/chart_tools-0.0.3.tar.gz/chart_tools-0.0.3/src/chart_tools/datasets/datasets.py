import pandas as pd

def load_data(name, **kwargs):
    # In the future start using different branch to store data, so I won't mess it up
    url = f'https://raw.githubusercontent.com/ryayoung/datasets/main/{name}.csv'

    return pd.read_csv(url, **kwargs)


