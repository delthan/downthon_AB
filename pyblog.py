import os
import markdown
from datetime import datetime
import time
import json
from pathlib import Path


markdown_directory = Path.cwd() / "markdown"
files = list(markdown_directory.rglob("*.md*"))
txt_files = list(markdown_directory.rglob("*.txt*"))
files.extend(txt_files)
header_markdown = str("./config/header.md")
footer_markdown = str("./config/footer.md")
header_html = str("./config/header.html")
footer_html = str("./config/footer.html")
config = str("./config/config.json")
tags = set()
authors = set()
years = set()
posts = dict()


def main():
    parse_config_json()
    read_markdown_fill_posts(files)
    # read_markdown_write_individual_html(files)
    read_markdown_create_indices(posts)
    return

def parse_config_json():
    with open(config) as f:
        data = json.load(f)
        parse_config_json.date_format = data.get("date_format")
        parse_config_json.html_directory = data.get("html_directory")
        parse_config_json.add_sortable_date_to_file_name = data.get("add_sortable_date_to_file_name")

def read_markdown_write_individual_html(files):
    for file in files:
        file_name = os.path.basename(file).replace(".md", "").replace(".txt", "").strip().lower()
        with open(file, "r", encoding="utf-8") as md_file:
            md_text = md_file.read()
            html = markdown.markdown(md_text)
        with open(header_markdown) as header_md, open(header_html) as header:
            header = header.read()
            header_md = header_md.read()
            header = header.replace("[[$CONTENT]]", markdown.markdown(header_md))
            html = header + html
        with open(footer_markdown) as footer_md, open(footer_html) as footer:
            footer_md = footer_md.read()
            footer = footer.read()
            footer = footer.replace("[[$CONTENT]]", markdown.markdown(footer_md))
            html = html + markdown.markdown(footer)
        with open("./html/" + file_name + ".html", "w", encoding="utf-8", errors="xmlcharrefreplace") as html_file:
            html_file.write(html)

def read_markdown_fill_posts(files):
    for file in files:
        file_title = ""
        file_date = ""
        file_year = ""
        file_author = ""
        file_summary = ""
        file_tags = ""
        file_name = os.path.basename(file).replace(".md", "").replace(".txt", "").strip().lower()
        with open(file, "r", encoding="utf-8") as md_file:
            md_text = md_file.read().splitlines(False)
            del md_text[6:]
            for line in md_text:
                if "Title: " in line:
                    file_title = line.replace("Title: ", "").strip()
                elif "Date: " in line:
                    file_date = line.replace("Date: ", "").strip()
                elif "Author: " in line:
                    file_author = line.replace("Author: ", "").strip()
                    authors.add(file_author)
                elif "Summary: " in line:
                    file_summary = line.replace("Summary: ", "").strip()
                elif "Tags: " in line:
                    file_tags = list(line.replace("Tags: ", "").strip().split(', '))
                    for tag in file_tags:
                        tags.add(tag)
                else:
                    if file_title == "":
                        file_title = file_name
                    if file_date == "":
                        file_cdate = datetime.strptime(time.ctime(os.path.getmtime((file))), "%a %b %d %H:%M:%S %Y")
                        file_date = parse_config_json.date_format.replace("YYYY", str(file_cdate.year)).replace("MM", str(file_cdate.month).zfill(2)).replace("DD", str(file_cdate.day).zfill(2))
                        file_year = str(file_cdate.year)
                    if file_author == "":
                        file_author = "anonymous"
                    if file_summary == "":
                        file_summary = False
                    if file_tags == "":
                        file_tags = False

                years.add(file_year)
                year_position = parse_config_json.date_format.find("Y")
                month_position = parse_config_json.date_format.find("M")
                day_position = parse_config_json.date_format.find("D")
                file_year = file_date[year_position:year_position+4]
                file_day = file_date[day_position:day_position+2]
                file_month = file_date[month_position:month_position+2]
                file_date_sortable = file_year + file_month + file_day

            posts.update({file_name: (file_date_sortable, file_title, file_date, file_year, file_author, file_summary, file_tags)}) 
     
def read_markdown_create_indices(posts):
    index_html = ""
    authors_html = ""
    tags_html = ""
    sorted_posts = dict()
    # print(posts)
    for post in posts:
        post_value = str(posts.get(post)[0])
        sorted_posts.update({post: post_value})
    sorted_posts = dict(sorted(sorted_posts.items(),key=lambda x:x[1],reverse=True))
    # print(sorted_posts)
    for post in sorted_posts: # filling index_html
        pass

    return

main()
