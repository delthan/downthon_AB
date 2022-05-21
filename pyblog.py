import os
import markdown
from datetime import datetime
import time
import json
from pathlib import Path


files = list()
header_html = str("./config/header.html")
footer_html = str("./config/footer.html")
index_html = str("./config/index.html")
config = str("./config/config.json")
tags = set()
authors = set()
years = set()
posts = dict()


def main():
    parse_config_json(config)
    make_list_of_files()
    read_markdown_fill_posts(files)
    # read_markdown_write_individual_html(files)
    read_markdown_create_indices(posts)
    return


def parse_config_json(config_file):
    with open(config_file) as f:
        data = json.load(f)
        parse_config_json.date_format = data.get("date_format")
        parse_config_json.html_directory = data.get("html_directory")
        parse_config_json.markdown_directory = data.get("markdown_directory")
        parse_config_json.add_sortable_date_to_file_name = data.get("add_sortable_date_to_file_name")
        parse_config_json.header_markdown = data.get("header_markdown")
        parse_config_json.footer_markdown = data.get("footer_markdown")
        parse_config_json.swag_markdown = data.get("swag_markdown")


def make_list_of_files():
    for subdir, dirs, files_names in os.walk(parse_config_json.markdown_directory):
        for file in files_names:
            files.append(os.path.join(subdir, file))


def read_markdown_write_individual_html(files):
    for file in files:
        file_name = os.path.basename(file).replace(".md", "").replace(".txt", "").strip().lower()
        with open(file, "r", encoding="utf-8") as md_file:
            md_text = md_file.read()
            html = markdown.markdown(md_text)
        with open(parse_config_json.header_markdown) as header_md, open(header_html) as header:
            header = header.read()
            header_md = header_md.read()
            header = header.replace("[[$CONTENT]]", markdown.markdown(header_md))
            html = header + html
        with open(parse_config_json.footer_markdown) as footer_md, open(footer_html) as footer:
            footer_md = footer_md.read()
            footer = footer.read()
            footer = footer.replace("[[$CONTENT]]", markdown.markdown(footer_md))
            html = html + markdown.markdown(footer)
        with open(parse_config_json.html_directory + str(posts.get(file_name)[3]) + "/" + file_name + ".html", "w", encoding="utf-8", errors="xmlcharrefreplace") as html_file:
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
    index_html_output = ""
    authors_html = ""
    tags_html = ""
    sorted_posts = dict()
    for post in posts: # pulling post name and date out of posts dict
        post_value = str(posts.get(post)[0])
        sorted_posts.update({post: post_value})
    sorted_posts = dict(sorted(sorted_posts.items(),key=lambda x:x[1],reverse=True))
    with open(parse_config_json.header_markdown) as header_md, open(header_html) as header: # starting index_html
        header = header.read()
        header_md = header_md.read()
        header = header.replace("[[$CONTENT]]", markdown.markdown(header_md))
        index_html_output = header
    for post in sorted_posts: # filling index_html_output
        with open(index_html) as index_html_file:
            index_html_output += index_html_file.read()
            index_html_output = index_html_output.replace("[[$FILE_TITLE]]", posts.get(post)[1])
            index_html_output = index_html_output.replace("[[$FILE_AUTHOR]]", posts.get(post)[4])
            index_html_output = index_html_output.replace("[[$FILE_TAGS]]", str(posts.get(post)[6]))
            index_html_output = index_html_output.replace("[[$FILE_DATE]]", posts.get(post)[2])
            index_html_output = index_html_output.replace("[[$FILE_SUMMARY]]", posts.get(post)[5])
    with open(parse_config_json.footer_markdown) as footer_md, open(footer_html) as footer: # finishing index_html_output
        footer_md = footer_md.read()
        footer = footer.read()
        footer = footer.replace("[[$CONTENT]]", markdown.markdown(footer_md))
        index_html_output = index_html_output + markdown.markdown(footer)
    with open(parse_config_json.html_directory + "index.html", "w", encoding="utf-8", errors="xmlcharrefreplace") as html_file: # writing index_html_output
        html_file.write(index_html_output)


main()
