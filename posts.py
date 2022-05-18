import os

import os
import markdown
import datetime
from datetime import datetime
import time
import json
from pathlib import Path

markdown_directory = Path.cwd() / "markdown"
html_directory = Path.cwd() / "html"
template_directory = Path.cwd() / "templates"
files = list(markdown_directory.rglob("*.md*"))
txt_files = list(markdown_directory.rglob("*.txt*"))
files.extend(txt_files)
posts = dict()
config = str("./config/config.json")
tags = set()
authors = set()
years = set()



 

