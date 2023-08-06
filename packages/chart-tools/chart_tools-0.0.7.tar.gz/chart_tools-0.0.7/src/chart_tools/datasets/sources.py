# from chart_tools.datasets.datasource import Source

# SOURCE: https://raw.githubusercontent.com/[USER]/[REPO]/[BRANCH]/[LOC]/[FILE]
# API: https://api.github.com/repos/[USER]/[LOC]/git/trees/[BRANCH]?recursive=1

# sources = {
#     "main":     Source('ryayoung', 'datasets', 'main', 'data'),
#     "covid":    Source('datasets', 'covid-19', 'main', 'data'),
#     "sp500":    Source('datasets', 's-and-p-500-companies', 'master', 'data'),
#     "football": Source('datasets', 'football-datasets', 'master', 'datasets'),
# }

sources = {
        "main": {
            "u": "ryayoung",
            "r": "datasets",
            "b": "main",
            "p": "data",
            },
        "covid": {
            "u": "datasets",
            "r": "covid-19",
            "b": "main",
            "p": "data",
            },
        "football": {
            "u": "datasets",
            "r": "football-datasets",
            "b": "master",
            "p": "datasets",
            },
        "sp500": {
            "u": "datasets",
            "r": "s-and-p-500-companies",
            "b": "master",
            "p": "data",
            },
        "openml": {
            "u": "datasets",
            "r": "openml-datasets",
            "b": "master",
            "p": "data",
            },

    }
