import pandas as pd
import requests
import json
from chart_tools.datasets.sources import sources
from chart_tools.datasets.datasource import Source, DataSource

def build_source_root(s):
    return f"https://github.com/{s['u']}/{s['r']}/tree/{s['b']}/{s['l']}"


def build_source(s, name):
    return f"https://raw.githubusercontent.com/{s['u']}/{s['r']}/{s['b']}/{s['l']}{name}.csv"


def build_request(s):
    return f"https://api.github.com/repos/{s['u']}/{s['r']}/git/trees/{s['b']}?recursive=1"


def validate(name, source):
    # If no name is passed, provide help
    if not name:
        print("Call load_data('help', '<your_source>') to see on all datasets in a source.")
        print("Call load_data('help') to see all sources and all datasets.")
        print("---------\nSOURCES:")
        for l in locations.keys():
            s = locations[l]
            print(f" '{l}':{(10-len(l))*' '}{build_source_root(s)}")
        return False

    if name == 'help':
        s = locations.get(source, None)
        if source == None or s == None:
            keys = locations.keys()
            print("All available datasets")
            print("------------------")
            for i, source in enumerate(keys):
                s = locations[source]
                url = build_request(s)
                available = requests.get(url).json()['tree']
                names = [f"'{f['path'].removesuffix('.csv').removeprefix(s['l'])}'"
                            for f in available if ".csv" in f['path']]
                print(f"{source}:\n", end="")
                for i, n in enumerate(names):
                    if i > 8:
                        print(f"    (Limit reached. Call load_data('help', '{source}') to see all")
                        break
                    print(f"  {n}")
            return False

        else:
            print(build_source_root(s))
            print(f"Datasets for '{source}':")
            print(" ----------------------")
            url = build_request(s)
            available = requests.get(url).json()['tree']
            names = [f"'{f['path'].removesuffix('.csv').removeprefix(s['l'])}'"
                        for f in available if ".csv" in f['path']]
            print(" ", end="")
            print(*names, sep="\n ")
            return False
    
    else:
        return True


def load_data(name=None, source=None, **kwargs):
    if not validate(name, source):
        return None
    
    if name and source == None:
        source = 'main'

    s = locations.get(source, None)
    if not s:
        print(f"Unknown source '{source}'. The following are available:")
        print("-------------------------------------------")
        print(*locations.keys(), sep=", ")
        return None

    url = build_source(s, name)
    
    # Now we know the source is valid.
    # Try to fetch the dataset
    try:
        df = pd.read_csv(url, **kwargs)
        return df
    except Exception as e:
        url = build_request(s)
        r = requests.get(url) # This should work, since source is valid
        res = r.json()['tree']
        names = [f"'{f['path'].removesuffix('.csv').removeprefix(s['l'])}'"
                    for f in res if ".csv" in f['path']]
        print(f"Couldn't find dataset.\nThe following are currently available for '{source}':")
        print("-------------------------------------------------------")
        print(*names, sep=", ")
        return None
