# Standard lib
from typing import List
import os
import shutil
from dataclasses import dataclass

# 3rd party
import requests
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT
from whoosh.qparser import QueryParser
from whoosh.query import Or
from sh import git
import yaml
import tqdm


GIT_PAT = os.environ["GIT_PERSONAL_ACCESS_TOKEN"]


@dataclass
class WolfiPackageResult:
    name: str
    description: str


class WolfiClient:
    def __init__(self):
        self._init_index()
    
    def _init_index(self):
        """
        Initialize the whoosh index with all of Wolfi.
        """
        schema = Schema(filename=TEXT(stored=True), description=TEXT(stored=True))
        index_dir = "wolfi_index"

        # Create index dir
        if os.path.exists(index_dir):
            shutil.rmtree(index_dir)
        os.mkdir(index_dir)

        # Create source file dir
        if os.path.exists("os"):
            shutil.rmtree("os")
        git.clone("https://github.com/wolfi-dev/os.git", "os")

        self.index = create_in(index_dir, schema)
        writer = self.index.writer()

        files = os.listdir("os")
        for file in tqdm.tqdm(files):
            if file.endswith(".yaml"):
                with open(os.path.join("os", file), "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    if "package" not in data.keys():
                        continue
                    name = data["package"]["name"]
                    if "description" in data["package"].keys():
                        desc = data["package"]["description"]
                    else:
                        desc = ""
                    writer.add_document(filename=name, description=desc)
        writer.commit()

    def search(self, keyword) -> List[WolfiPackageResult]:
        """
        Searches Wolfi for package names matching `keyword`.

        Args:
            keyword: The keyword to search package names for.
        
            Returns: A `List` of `WolfiPackageResult` objects.
        
        Raises:
            TypeError: If keyword is not a `str`.


        1) Clone wolfi
        2) Index search files
        3) perform the search
        """
        # TODO: This search is very naive. Implement a search that is smarter and uses package descriptions
        if not isinstance(keyword, str):
            raise TypeError("`keyword` must be a `str`.")
        
        with self.index.searcher() as searcher:
            name_query = QueryParser("filename", self.index.schema).parse(keyword)
            desc_query = QueryParser("description", self.index.schema).parse(keyword)
            combined_query = Or([name_query, desc_query])

            # Perform the search
            results = searcher.search(combined_query)
            return [WolfiPackageResult(r["filename"], r["description"]) for r in results]
