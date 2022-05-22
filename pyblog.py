import os
import pathlib
import markdown
from datetime import datetime
import time
import json


header_html = str("./config/header.html")
footer_html = str("./config/footer.html")
index_html = str("./config/index.html")
config = str("./config/config.json")
files = list()
posts = dict()
tags = set()
authors = set()
years = set()


def main():
    make_list_of_files()
    read_markdown_fill_posts(files)
    read_markdown_write_individual_html(files)
    read_markdown_create_indices(posts)
    return


def parse_json_config(config_file, request_string):
    with open(config_file) as f:
        data = json.load(f)
        data_return = data.get(request_string)
        return data_return


def parse_date_time(auto_date, manual_date): # auto_date = date created by looking at file last modifed date, manual_date = date entered on .md file
    date_format = parse_json_config(config, "date_format")
    manual_formatted_date = manual_date
    twenty_four_hour_time_format = parse_json_config(config, "twenty_four_hour_time_format")
    year_position = date_format.find("Y")
    month_position = date_format.find("M")
    day_position = date_format.find("D")
    hour_position = date_format.find("H")
    minute_position = date_format.find("m")
    period_position = date_format.find("[")
    
    if auto_date == None:
        date_period = manual_formatted_date[period_position:period_position+2]
        date_year = manual_formatted_date[year_position:year_position+4]
        date_day = manual_formatted_date[day_position:day_position+2]
        date_month = manual_formatted_date[month_position:month_position+2]
        if twenty_four_hour_time_format == False:
            if date_period == "PM":
                date_hour = str(int(manual_formatted_date[hour_position:hour_position+2])+12)
        else:
            date_period = ""
        date_hour = manual_formatted_date[hour_position:hour_position+2]
        date_minute = manual_formatted_date[minute_position:minute_position+2]
    else:
        date_year = str(auto_date.year)
        date_day = str(auto_date.day).zfill(2)
        date_month = str(auto_date.month).zfill(2)
        date_hour = str(auto_date.hour).zfill(2)
        date_minute = str(auto_date.minute).zfill(2)
        if twenty_four_hour_time_format == False:
            if int(date_hour) > 12:
                date_period = "PM"
                manual_format_date_hour = str(int(date_hour)-12).zfill(2)
            else:
                date_period = "AM"
        else:
            date_period = ""
        
        manual_formatted_date = date_format.replace("YYYY", date_year).replace("MM", date_month).replace("DD", date_day).replace("HH", date_hour).replace("mm", date_minute).replace("[AM/PM]", manual_format_date_hour)
    
    sortable_date = str(date_year) + str(date_month) + str(date_day) + str(date_hour) + str(date_minute)

    return sortable_date, manual_formatted_date, date_year, date_month, date_day, date_hour, date_minute, date_period


def make_list_of_files():
    for subdir, dirs, files_names in os.walk(parse_json_config(config, "markdown_directory")):
        for file in files_names:
            if pathlib.Path(file).suffix == ".md" or pathlib.Path(file).suffix == ".txt":
                files.append(os.path.join(subdir, file))


def read_markdown_write_individual_html(list_of_files):
    for file in list_of_files:
        file_name = os.path.basename(file).replace(".md", "").replace(".txt", "").strip().lower()
        with open(file, "r", encoding="utf-8") as md_file:
            md_text = md_file.read()
            html = markdown.markdown(md_text)
        with open(parse_json_config(config, "header_markdown")) as header_md, open(header_html) as header:
            header = header.read()
            header_md = header_md.read()
            header = header.replace("[[$CONTENT]]", markdown.markdown(header_md))
            html = header + html
        with open(parse_json_config(config, "footer_markdown")) as footer_md, open(footer_html) as footer:
            footer_md = footer_md.read()
            footer = footer.read()
            footer = footer.replace("[[$CONTENT]]", markdown.markdown(footer_md))
            html = html + markdown.markdown(footer)
        if parse_json_config(config, "add_sortable_date_to_file_name") == False:
            with open(parse_json_config(config, "html_directory") + str(posts.get(file_name)[3]) + "/" + file_name + ".html", "w", encoding="utf-8", errors="xmlcharrefreplace") as html_file:
                html_file.write(html)
        else: 
            with open(parse_json_config(config, "html_directory") + str(posts.get(file_name)[3]) + "/" + str(posts.get(file_name)[0]) + "-" + file_name + ".html", "w", encoding="utf-8", errors="xmlcharrefreplace") as html_file:
                html_file.write(html)


def read_markdown_fill_posts(list_of_files):
    for file in list_of_files:
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
                if "Title:" in line:
                    file_title = line.replace("Title:", "").strip()
                elif "Date:" in line:
                    file_date = line.replace("Date:", "").strip()
                    file_year = parse_date_time(None, file_date)[2]
                elif "Author:" in line:
                    file_author = line.replace("Author:", "").strip()
                    authors.add(file_author)
                elif "Summary:" in line:
                    file_summary = line.replace("Summary:", "").strip()
                elif "Tags:" in line:
                    file_tags = list(line.replace("Tags:", "").strip().split(', '))
                    for tag in file_tags:
                        tags.add(tag)
                else:
                    if file_title == "":
                        file_title = file_name
                    if file_date == "":
                        file_cdate = datetime.strptime(time.ctime(os.path.getmtime((file))), "%a %b %d %H:%M:%S %Y")
                        file_date = parse_date_time(file_cdate,file_cdate)
                        file_date = file_date[1]
                        file_year = str(file_cdate.year)
                    if file_author == "":
                        file_author = parse_json_config(config, "default_author")
                        authors.add(file_author)

                years.add(file_year)
                sortable_date = parse_date_time(None, file_date)[0]

            posts.update({file_name: (sortable_date, file_title, file_date, file_year, file_author, file_summary, file_tags)}) 


def read_markdown_create_indices(list_of_posts):
    tags_html_output = ""
    sorted_posts = dict()
    sorted_posts_authors = dict()
    sorted_posts_tags = dict()

    for post in list_of_posts: # pulling post name and date out of posts dict
        post_value = str(list_of_posts.get(post)[0])
        author_value = str(list_of_posts.get(post)[4])
        tags_value = list(list_of_posts.get(post)[6])
        sorted_posts.update({post: post_value})
        sorted_posts_authors.update({post: author_value})
        sorted_posts_tags.update({post: tags_value})
    sorted_posts = dict(sorted(sorted_posts.items(),key=lambda x:x[1],reverse=True))
    sorted_posts_authors = dict(sorted(sorted_posts_authors.items(),key=lambda x:x[1],reverse=True))
    sorted_posts_tags = dict(sorted(sorted_posts_tags.items(),key=lambda x:x[1],reverse=True)) 

    with open(parse_json_config(config, "header_markdown")) as header_md, open(header_html) as header: # starting index_html_output
        header = header.read()
        header_md = header_md.read()
        header = header.replace("[[$CONTENT]]", markdown.markdown(header_md))
        index_html_output = header
    for post in sorted_posts: # filling index_html_output
        with open(index_html) as index_html_file:
            index_html_output = ""
            index_html_output += index_html_file.read()
            index_html_output = index_html_output.replace("[[$FILE_TITLE]]", posts.get(post)[1])
            index_html_output = index_html_output.replace("[[$FILE_AUTHOR]]", posts.get(post)[4])
            index_html_output = index_html_output.replace("[[$FILE_TAGS]]", str(posts.get(post)[6]))
            index_html_output = index_html_output.replace("[[$FILE_DATE]]", posts.get(post)[2])
            index_html_output = index_html_output.replace("[[$FILE_SUMMARY]]", posts.get(post)[5])
    with open(parse_json_config(config, "footer_markdown")) as footer_md, open(footer_html) as footer: # finishing index_html_output
        footer_md = footer_md.read()
        footer = footer.read()
        footer = footer.replace("[[$CONTENT]]", markdown.markdown(footer_md))
        index_html_output = index_html_output + footer
    with open(parse_json_config(config, "html_directory") + "index.html", "w", encoding="utf-8", errors="xmlcharrefreplace") as html_file: # writing index_html_output
        html_file.write(index_html_output)
    if parse_json_config(config, "generate_author_index") == True:
        for author in sorted_posts_authors.values():
            print("loop starting")
            authors_html_output = ""

            def author_match(post):
                if author == sorted_posts_authors.get(post):
                    return True
                else:
                    return False
            filtered_posts_by_author = set(filter(author_match, sorted_posts_authors))

            with open(parse_json_config(config, "header_markdown")) as header_md, open(header_html) as header: # starting author_index_html
                header = header.read()
                header_md = header_md.read()
                header = header.replace("[[$CONTENT]]", markdown.markdown(header_md))
                authors_html_output = header
            for post in filtered_posts_by_author:
                print(post)
                print(author)
                print(filtered_posts_by_author)
                with open(index_html) as authors_html_file:
                    authors_html_output += authors_html_file.read()
                    authors_html_output = authors_html_output.replace("[[$FILE_TITLE]]", list_of_posts.get(post)[1])
                    authors_html_output = authors_html_output.replace("[[$FILE_AUTHOR]]", list_of_posts.get(post)[4])
                    authors_html_output = authors_html_output.replace("[[$FILE_TAGS]]", str(list_of_posts.get(post)[6]))
                    authors_html_output = authors_html_output.replace("[[$FILE_DATE]]", list_of_posts.get(post)[2])
                    authors_html_output = authors_html_output.replace("[[$FILE_SUMMARY]]", list_of_posts.get(post)[5])
            with open(parse_json_config(config, "footer_markdown")) as footer_md, open(footer_html) as footer: # finishing author_index_html
                footer_md = footer_md.read()
                footer = footer.read()
                footer = footer.replace("[[$CONTENT]]", markdown.markdown(footer_md))
                authors_html_output = authors_html_output + footer
            with open(parse_json_config(config, "html_directory") + author.lower() + ".html", "w", encoding="utf-8", errors="xmlcharrefreplace") as html_file: # writing author_index_html
                html_file.write(index_html_output)
            print("loop ended")


main()

