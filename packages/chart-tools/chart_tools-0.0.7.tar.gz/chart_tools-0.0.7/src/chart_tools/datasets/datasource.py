from dataclasses import dataclass
from chart_tools.datasets.sources import sources
from operator import countOf
import pandas as pd
import requests
import json

@dataclass
class Source:
    __user: str
    __repo: str
    __branch: str
    __path: str
    __datasets = []
    truncated_datasets = False

    @property
    def user(self):
        return self.__user
    @property
    def repo(self):
        return self.__repo
    @property
    def branch(self):
        return self.__branch
    @property
    def path(self):
        # if self.__path.endswith("/") or self.__path == "":
        return self.__path
        # else:
            # return f"{self.__path}/"
    @property
    def datasets(self) -> list:
        if self.__datasets == []:
            self.refresh_datasets()

        return self.__datasets

    @property
    def subdirs(self) -> list:
        if self.__datasets == []:
            self.refresh_datasets()

        return list(set([
                f.split('/')[0] for f in self.datasets if "/" in f
            ]))
    
    @property
    def datasets_base(self) -> list:
        if self.__datasets == []:
            self.refresh_datasets()

        return [f.rsplit('/', 1)[-1] for f in self.datasets]

    @property
    def root(self) -> str:
        """
        Returns user-friendly url to visit the source on Github.com
        """
        return f"https://github.com/{self.user}/{self.repo}/tree/{self.branch}/{self.path}"
    
    @property
    def req_url(self) -> str:
        """
        Returns url to Github API for getting all files in repo and branch
        """
        return f"https://api.github.com/repos/{self.user}/{self.repo}/git/trees/{self.branch}?recursive=1"
    
    @user.setter
    def user(self, value):
        if "/" in value:
            raise ValueError("Github username can't have slashes")
        self.__user = value

    @repo.setter
    def repo(self, value):
        if "/" in value:
            raise ValueError("Github repository name can't have slashes")
        self.__repo = value

    @branch.setter
    def branch(self, value):
        if "/" in value:
            raise ValueError("Github branch name can't have slashes")
        self.__branch = value

    @path.setter
    def path(self, value):
        if value.endswith("/"):
            raise ValueError("Path must not end with a slash")
        self.__path = value
        # Update datasets since path changed
        self.refresh_datasets()


    def file_url(self, filename) -> str:
        """
        Returns url to raw file
        """
        path = f"{self.path}/" if len(self.path) > 0 else self.path
        return f"https://raw.githubusercontent.com/{self.user}/{self.repo}/{self.branch}/{path}{filename}.csv"


    def req_files(self) -> list:
        return requests.get(self.req_url).json()
    

    def dir_contents(self, dir) -> list:
        return [f.removeprefix(f"{dir}/") for f in self.datasets if f.startswith(dir)]


    def load(self, fname, **kwargs) -> pd.DataFrame:
        if self.__datasets == []:
            self.refresh_datasets()
        
        if countOf(self.datasets, fname) == 1:
            return pd.read_csv(self.file_url(fname), **kwargs)

        if countOf(self.datasets_base, fname) == 1:
            full_fname = [f for f in self.datasets if f.rsplit('/', 1)[-1] == fname][0]
            return pd.read_csv(self.file_url(full_fname), **kwargs)

        raise ValueError(
            "Either the file doesn't exist, or you specified a filename "
            "that is duplicated across multiple sub-directories in the chosen path. "
            "If the latter is true, please use the full subpath instead."
            )
        
    def refresh_datasets(self):
        res = self.req_files()
        if res.get("message") == "Not Found":
            raise ValueError("No files found. Likely an invalid data source")
        
        self.truncated_datasets = res.get('truncated', False)

        self.__datasets = [f['path'].removesuffix('.csv').removeprefix(f"{self.path}/")
                    for f in res['tree'] if ".csv" in f['path']]



class DataSource(Source):
    sources = []

    def __init__(self, user=None, repo=None, branch=None, path="", name=None):

        if path.endswith("/"):
            path = path.removesuffix("/")

        if user and repo and branch:
            super().__init__(user, repo, branch, path)
            # self.refresh_datasets()
            self.name = None
            return

        if name:
            source = sources.get(name, None)
            if not source:
                raise ValueError(f"Unknown source, '{name}'")

            super().__init__(source['u'], source['r'], source['b'], source['p'])
            self.name = name
            # self.refresh_datasets()
            return
        


    def display_datasets(self, header=True, trunc=1000):
        if header:
            if self.name != None:
                print(f"Datasets for '{self.name}':")
            if self.name == None:
                print(f"Datasets in '{self.user}/{self.repo}/{self.path}':")
            if len(self.subdirs) > 0:
                print("(refer files inside folders using the full path. Ex: 'folder/file')")
            print("---------------------------")
        
        # Files in base directory
        for file in [f for f in self.datasets if "/" not in f]:
            print(f"  {file}")

        # Files in subdirectories
        count = 0
        for dir in self.subdirs:
            print(f"  {dir}/")
            count += 1
            for f in self.dir_contents(dir):
                count += 1
                if count > trunc: break
                print(f"    {f}")

            if count > trunc: break

        if count > trunc:
            name = self.name if self.name else f"{self.user}/{self.repo}"
            print(f"      ({len(self.datasets)-count} more files in {name})")
            
    

    def display_subdirs(self):
        print(f"Sub-directories in '{self.user}/{self.repo}/{self.path}'")
        print("---------------------------------------")
        print("  ", end="")
        print(*self.subdirs, sep="\n  ")


        

# --------------------------------------------------------------------------------
def get_sources() -> list:
    return {
            k: DataSource(name=k)
    for k, v in sources.items() }

def display_sources(srcs) -> None:
    for s in srcs.values():
        print(f" '{s.name}':{(10-len(s.name))*' '}{s.root}")

def display_sources_full(srcs) -> None:
    print("(Use load_data(source_name, filename) to load data)")
    print("(Use load_data(source_name) to see available datasets in source)")
    print("")
    for s in srcs.values():
        print(f"'{s.name}'  -  {s.root}")
        print("---------------------------------")
        s.display_datasets(header=False, trunc=15)
        print()

def load_data(source=None, file=None, **kwargs) -> pd.DataFrame:

    if DataSource.sources == []:
        DataSource.sources = get_sources()
    srcs = DataSource.sources

    if not source and not file:
        print("Use load_data(source_name, filename) to load dataframe")
        print("Use load_data(source_name) to see all datasets in a source.")
        print("Use load_data('all') to see all datasets.")
        print("---------\nSOURCES:")
        display_sources(srcs)
        return None
    
    if source == 'all' and not file:
        display_sources_full(srcs)
        return None
    
    if not file:
        if source in srcs.keys():
            srcs[source].display_datasets()
            return None
        if source in srcs['main'].datasets:
            return srcs['main'].load(source, **kwargs)

        print(f"Unknown source, '{source}'")
        return None
        
    if source not in srcs.keys():
        print(f"Unknown source, '{source}'")
        return None
    
    return srcs[source].load(file, **kwargs)
