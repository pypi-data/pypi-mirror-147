import pandas as pd
import requests
import json

other_names = 'https://api.github.com/repos/ryayoung/datasets/git/trees/main?recursive=1'

def load_data(name, **kwargs):
    # In the future start using different branch to store data, so I won't mess it up
    url = f'https://raw.githubusercontent.com/ryayoung/datasets/main/{name}.csv'
    index_col = kwargs.get("index_col", None)

    try:
        df = pd.read_csv(url, index_col=index_col, **kwargs)
    except Exception as e:
        r = requests.get(other_names)
        res = r.json()['tree']
        names = [f"'{f['path'].removesuffix('.csv')}'" for f in res]
        print("Couldn't find dataset. The following are currently available:")
        print(*names, sep=", ")
        return None

    return df
