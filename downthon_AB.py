import os
import pathlib
import markdown
from datetime import datetime
import time
import json



config = str("./config/config.json")
files = list()
posts = dict()
tags = set()
authors = set()
years = set()


def main(): # script flow
    files_setup()
    define_html_templates()
    read_markdown_fill_posts(files)
    folder_checker()
    read_markdown_write_posts_html(files)
    read_markdown_create_indices(posts)
    return


def define_html_templates():
    templates_directory = parse_json_config(config, "templates_directory")
    global header_html
    global footer_html
    global swag_html
    global index_html
    global post_html
    header_html = os.path.join(templates_directory, "header.html")
    footer_html = os.path.join(templates_directory, "footer.html")
    swag_html = os.path.join(templates_directory, "swag.html")
    index_html = os.path.join(templates_directory, "index.html")
    post_html = os.path.join(templates_directory, "post.html")

    return


def parse_json_config(config_file, key_request): # config_file = json file where the config options live, e.g. 'config', key_request = lookup key from json file
    with open(config_file) as f:
        data = json.load(f)
        value_return = data.get(key_request)
        return value_return


def convert_date_format():
    twenty_four_hour_time_format = parse_json_config(config, "twenty_four_hour_time_format")
    datetime_formatted_date_format = parse_json_config(config, "date_format")
    datetime_formatted_date_format = datetime_formatted_date_format.replace("MM", "%m")
    datetime_formatted_date_format = datetime_formatted_date_format.replace("DD", "%d")
    datetime_formatted_date_format = datetime_formatted_date_format.replace("YYYY", "%Y")
    datetime_formatted_date_format = datetime_formatted_date_format.replace("mm", "%M")
    if twenty_four_hour_time_format == False:
        datetime_formatted_date_format = datetime_formatted_date_format.replace("HH", "%I")
        datetime_formatted_date_format = datetime_formatted_date_format.replace("[AM/PM]", "%p")
    else:
        datetime_formatted_date_format = datetime_formatted_date_format.replace("HH", "%H")
        datetime_formatted_date_format = datetime_formatted_date_format.replace("[AM/PM]", "")       

    return datetime_formatted_date_format


def parse_date_time(date, return_value): 
    date_format = parse_json_config(config, "date_format")
    twenty_four_hour_time_format = parse_json_config(config, "twenty_four_hour_time_format")
    date_year = str(date.year)
    date_day = str(date.day).zfill(2)
    date_month = str(date.month).zfill(2)
    date_hour = str(date.hour).zfill(2)
    date_minute = str(date.minute).zfill(2)
    if twenty_four_hour_time_format == False:
        if int(date_hour) > 12:
            date_period = "PM"
            manual_format_date_hour = str(int(date_hour)-12).zfill(2)
        else:
            date_period = "AM"
            manual_format_date_hour = date_hour
    else:
        date_period = ""    
    manual_formatted_date = date_format.replace("YYYY", date_year).replace("MM", date_month).replace("DD", date_day).replace("HH", manual_format_date_hour).replace("mm", date_minute).replace("[AM/PM]", date_period)
    sortable_date = f"{date_year}{date_month}{date_day}{date_hour}{date_minute}"

    if return_value == "sortable_date":
        return sortable_date
    if return_value == "manual_formatted_date":
        return manual_formatted_date
    if return_value == "date_year":
        return date_year
    if return_value == "date_month":
        return date_month
    if return_value == "date_day":
        return date_day
    if return_value == "date_hour":
        return date_hour
    if return_value == "date_minute":
        return date_minute
    if return_value == "date_period":
        return date_period


def files_setup(): # Creating list of files
    for subdir, dirs, files_names in os.walk(parse_json_config(config, "markdown_directory")):
        for file in files_names:
            if pathlib.Path(file).suffix == ".md" or pathlib.Path(file).suffix == ".txt":
                files.append(os.path.join(subdir, file))


def folder_checker(): # Checking for output folders, and creating them if they don't exist.
    author_dir = parse_json_config(config, "html_directory") + "/author"
    tag_dir = parse_json_config(config, "html_directory") + "/tags"
    html_dir = parse_json_config(config, "html_directory")
    md_dir = parse_json_config(config, "markdown_directory")

    if os.path.isdir(html_dir) == False:
        os.makedirs(html_dir, mode=0o777, exist_ok=True)
    if parse_json_config(config, "generate_author_index") == True:
        if os.path.isdir(author_dir) == False:   
            os.makedirs(author_dir, mode=0o777, exist_ok=True)
    if parse_json_config(config, "generate_tag_index") == True:
        if os.path.isdir(tag_dir) == False:          
            os.makedirs(tag_dir, mode=0o777, exist_ok=True)
    if os.path.isdir(md_dir) == False:        
        os.makedirs(md_dir, mode=0o777, exist_ok=True)
    for year in years:
        if os.path.isdir(html_dir + year) == False:
            os.makedirs(html_dir + year, mode=0o777, exist_ok=True)


def read_markdown_write_posts_html(list_of_files): # Creating html files for individual posts
    for file in list_of_files:
        
        file_name = os.path.basename(file).replace(".md", "").replace(".txt", "").strip().lower()
        html_directory = parse_json_config(config, "html_directory")
        templates_directory = parse_json_config(config, "templates_directory")
        output_file_year = str(posts.get(file_name)[3])
        output_file_sortable_date = str(posts.get(file_name)[0])
        output_file_title_as_filename = str(posts.get(file_name)[1]).lower().replace(" ", "-")

        if parse_json_config(config, "use_title_as_file_name") == True:
            if parse_json_config(config, "add_sortable_date_to_file_name") == False:
                output_file_path = f"{html_directory}{output_file_year}/{output_file_title_as_filename}.html"
            else:
                output_file_path = f"{html_directory}{output_file_year}/{output_file_sortable_date}-{output_file_title_as_filename}.html"
        else:
            if parse_json_config(config, "add_sortable_date_to_file_name") == False:
                output_file_path = f"{html_directory}{output_file_year}/{file_name}.html"
            else:
                output_file_path = f"{html_directory}{output_file_year}/{output_file_sortable_date}-{file_name}.html"

        with open(file, "r", encoding="utf-8") as md_file:
            md_text = md_file.read().splitlines(False)
            md_text_header = md_file.read().splitlines(False)
            del md_text[:6]
            del md_text_header[6:]

            for line in md_text_header:
                if "Title:" or "Date:" or "Author:" or "Summary:" or "Tags:" not in line.strip():
                    md_text_header.write(line)

            md_text = "\n".join(md_text_header) + "\n" + "\n".join(md_text)

        with open(post_html, "r", encoding="utf-8") as post:
            post_html_file = post.read()
            post_html_file = post_html_file.replace("[[$FILE_TITLE]]", posts.get(file_name)[1])
            post_html_file = post_html_file.replace("[[$FILE_AUTHOR]]", posts.get(file_name)[4])
            post_html_file = post_html_file.replace("[[$FILE_AUTHOR_LINK]]", f"../author/{posts.get(file_name)[4]}.html".lower())
            post_html_file = post_html_file.replace("[[$FILE_DATE]]", posts.get(file_name)[2])
            post_html_tags = posts.get(file_name)[6]
            tags_html = "<a href=[[$TAG_LINK]]>[[$TAG]]</a> &nbsp"
            tags_html_output = ""
            for tag in post_html_tags:
                tags_html_output += tags_html.replace("[[$TAG]]", tag).replace("[[$TAG_LINK]]", f"../tags/{tag}.html")
            post_html_file = post_html_file.replace("[[$FILE_TAGS]]", tags_html_output)

        html = markdown.markdown(md_text)
        html = post_html_file + html

        with open(parse_json_config(config, "header_markdown")) as header_md, open(header_html) as header:
            header = header.read()
            header_md = header_md.read()
            site_title = parse_json_config(config, "site_title")
            header = header.replace("[[$HEADER_LINK]]", "../index.html")
            header = header.replace("[[$SITE_TITLE]]", site_title)
            if templates_directory == "./templates/original":
                header = header.replace("[[$CSS_FILE]]", "https://cdn.jsdelivr.net/npm/water.css@2/out/water.css")
            else:
                header = header.replace("[[$CSS_FILE]]", f"{html_directory}/styles.css")
            header = header.replace("[[$CONTENT]]", markdown.markdown(header_md))
            html = header + html
        with open(parse_json_config(config, "swag_markdown")) as swag_md, open(swag_html) as swag:
            swag = swag.read()
            swag_md = swag_md.read()
            swag = swag.replace("[[$CONTENT]]", markdown.markdown(swag_md))
            html = html + swag     
        with open(parse_json_config(config, "footer_markdown")) as footer_md, open(footer_html) as footer:
            footer_md = footer_md.read()
            footer = footer.read()
            if parse_json_config(config, "generate_about_page") == True:
                footer = footer.replace("[[$FOOTER_LINK]]", "../about.html").replace("[[$FOOTER_TEXT]]", "About this blog")
            else:
                footer = footer.replace("[[$FOOTER_LINK]]", "").replace("[[$FOOTER_TEXT]]", "")
            footer = footer.replace("[[$CONTENT]]", markdown.markdown(footer_md))
            html = html + markdown.markdown(footer)
        
        with open(output_file_path, "w", encoding="utf-8", errors="xmlcharrefreplace") as html_file:
            html_file.write(html)


def read_markdown_fill_posts(list_of_files): # Creating posts dictionary
    for file in list_of_files:
        file_title = ""
        file_date = datetime.min
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
                    datetime_formatted_date_format = convert_date_format()
                    file_date = datetime.strptime(file_date, datetime_formatted_date_format)
                    file_year = str(file_date.year)
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
                    if file_date == datetime.min:
                        file_date = datetime.strptime(time.ctime(os.path.getmtime((file))), "%a %b %d %H:%M:%S %Y")
                        file_year = str(file_date.year)
                    if file_author == "":
                        file_author = parse_json_config(config, "default_author")
                        authors.add(file_author)

                years.add(file_year)
                sortable_date = parse_date_time(file_date, "sortable_date")
                manual_formatted_date = parse_date_time(file_date, "manual_formatted_date")

            posts.update({file_name: (sortable_date, file_title, manual_formatted_date, file_year, file_author, file_summary, file_tags)}) 


def read_markdown_create_indices(list_of_posts): # Creating html files for indexes
    sorted_posts = dict()
    sorted_posts_authors = dict()
    sorted_posts_tags = dict()
    templates_directory = parse_json_config(config, "templates_directory")
    html_directory = parse_json_config(config, "html_directory")

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
        site_title = parse_json_config(config, "site_title")
        header = header.replace("[[$HEADER_LINK]]", "./index.html")
        header = header.replace("[[$SITE_TITLE]]", site_title)
        if templates_directory == "./templates/original":
            header = header.replace("[[$CSS_FILE]]", "https://cdn.jsdelivr.net/npm/water.css@2/out/water.css")
        else:
            header = header.replace("[[$CSS_FILE]]", f"{html_directory}/styles.css")
        header = header.replace("[[$CONTENT]]", markdown.markdown(header_md))
        index_html_output = header

    for post in sorted_posts: # filling index_html_output
        if parse_json_config(config, "use_title_as_file_name") == True:
            if parse_json_config(config, "add_sortable_date_to_file_name") == False:
                output_file_path =  str(posts.get(post)[3]) + "/" + str(posts.get(post)[1]).lower().replace(" ", "-") + ".html"
            else:
                output_file_path =  str(posts.get(post)[3]) + "/" + str(posts.get(post)[0]) + "-" + str(posts.get(post)[1]).lower().replace(" ", "-") + ".html"
        else:
            if parse_json_config(config, "add_sortable_date_to_file_name") == False:
                output_file_path =  str(posts.get(post)[3]) + "/" + post + ".html"
            else:
                output_file_path = str(posts.get(post)[3]) + "/" + str(posts.get(post)[0]) + "-" + post + ".html"

        with open(index_html) as index_html_file:
            index_html_output += index_html_file.read()
            index_html_output = index_html_output.replace("[[$FILE_TITLE]]", posts.get(post)[1])
            index_html_output = index_html_output.replace("[[$LINK]]", output_file_path)
            index_html_output = index_html_output.replace("[[$FILE_AUTHOR]]", posts.get(post)[4])
            if parse_json_config(config, "generate_author_index") == True:
                index_html_output = index_html_output.replace("[[$FILE_AUTHOR_LINK]]", f"./author/{posts.get(post)[4]}.html".lower())
            index_html_output = index_html_output.replace("[[$FILE_DATE]]", posts.get(post)[2])
            index_html_output = index_html_output.replace("[[$FILE_SUMMARY]]", posts.get(post)[5])
            index_html_tags = posts.get(post)[6]
            tags_html = "<a href=[[$TAG_LINK]]>[[$TAG]]</a> &nbsp"
            tags_html_output = ""
            for html_tag in index_html_tags:
                if parse_json_config(config, "generate_tag_index") == True:
                    tags_html_output += tags_html.replace("[[$TAG]]", html_tag).replace("[[$TAG_LINK]]", f"./tags/{html_tag}.html")
                else:
                    tags_html_output += f"{html_tag} "
            index_html_output = index_html_output.replace("[[$FILE_TAGS]]", tags_html_output)

    with open(parse_json_config(config, "footer_markdown")) as footer_md, open(footer_html) as footer: # finishing index_html_output
        footer_md = footer_md.read()
        footer = footer.read()
        if parse_json_config(config, "generate_about_page") == True:
            footer = footer.replace("[[$FOOTER_LINK]]", "./about.html").replace("[[$FOOTER_TEXT]]", "About this blog")
        else:
            footer = footer.replace("[[$FOOTER_LINK]]", "").replace("[[$FOOTER_TEXT]]", "")
        footer = footer.replace("[[$CONTENT]]", markdown.markdown(footer_md))
        index_html_output = index_html_output + footer
    with open(parse_json_config(config, "html_directory") + "index.html", "w", encoding="utf-8", errors="xmlcharrefreplace") as html_file: # writing index_html_output
        html_file.write(index_html_output)


    if parse_json_config(config, "generate_author_index") == True:
        for author in sorted_posts_authors.values():
            def author_match(post):
                if author == sorted_posts_authors.get(post):
                    return True
                else:
                    return False
            filtered_posts_by_author = set(filter(author_match, sorted_posts_authors))

            if parse_json_config(config, "use_title_as_file_name") == True:
                if parse_json_config(config, "add_sortable_date_to_file_name") == False:
                    output_file_path =  "../" + str(posts.get(post)[3]) + "/" + str(posts.get(post)[1]).lower().replace(" ", "-") + ".html"
                else:
                    output_file_path =  "../" + str(posts.get(post)[3]) + "/" + str(posts.get(post)[0]) + "-" + str(posts.get(post)[1]).lower().replace(" ", "-") + ".html"
            else:
                if parse_json_config(config, "add_sortable_date_to_file_name") == False:
                    output_file_path =  "../" + str(posts.get(post)[3]) + "/" + post + ".html"
                else:
                    output_file_path = "../" + str(posts.get(post)[3]) + "/" + str(posts.get(post)[0]) + "-" + post + ".html"

            with open(parse_json_config(config, "header_markdown")) as header_md, open(header_html) as header: # starting author_index_html
                header = header.read()
                header_md = header_md.read()
                site_title = parse_json_config(config, "site_title")
                header = header.replace("[[$HEADER_LINK]]", "../index.html")
                header = header.replace("[[$SITE_TITLE]]", site_title)
                if templates_directory == "./templates/original":
                    header = header.replace("[[$CSS_FILE]]", "https://cdn.jsdelivr.net/npm/water.css@2/out/water.css")
                else:
                    header = header.replace("[[$CSS_FILE]]", f"..{html_directory}/styles.css")
                header = header.replace("[[$CONTENT]]", markdown.markdown(header_md))
                authors_html_output = header

            for post in filtered_posts_by_author:
                with open(index_html) as authors_html_file:
                    authors_html_output += authors_html_file.read()
                    authors_html_output = authors_html_output.replace("[[$FILE_TITLE]]", list_of_posts.get(post)[1])
                    authors_html_output = authors_html_output.replace("[[$LINK]]", output_file_path) 
                    authors_html_output = authors_html_output.replace("[[$FILE_AUTHOR]]", list_of_posts.get(post)[4])
                    authors_html_output = authors_html_output.replace("[[$FILE_AUTHOR_LINK]]", f"./{posts.get(post)[4]}.html".lower())
                    authors_html_output = authors_html_output.replace("[[$FILE_DATE]]", list_of_posts.get(post)[2])
                    authors_html_output = authors_html_output.replace("[[$FILE_SUMMARY]]", list_of_posts.get(post)[5])
                    author_html_tags = posts.get(post)[6]
                    tags_html = "<a href=[[$TAG_LINK]]>[[$TAG]]</a> &nbsp"
                    tags_html_output = ""
                    for html_tag in author_html_tags:
                        if parse_json_config(config, "generate_tag_index") == True:
                            tags_html_output += tags_html.replace("[[$TAG]]", html_tag).replace("[[$TAG_LINK]]", f"../tags/{html_tag}.html")
                        else:
                            tags_html_output += f"{html_tag} "
                    authors_html_output = authors_html_output.replace("[[$FILE_TAGS]]", tags_html_output)

            with open(parse_json_config(config, "footer_markdown")) as footer_md, open(footer_html) as footer: # finishing author_index_html
                footer_md = footer_md.read()
                footer = footer.read()
                if parse_json_config(config, "generate_about_page") == True:
                    footer = footer.replace("[[$FOOTER_LINK]]", "../about.html").replace("[[$FOOTER_TEXT]]", "About this blog")
                else:
                    footer = footer.replace("[[$FOOTER_LINK]]", "").replace("[[$FOOTER_TEXT]]", "")
                footer = footer.replace("[[$CONTENT]]", markdown.markdown(footer_md))
                authors_html_output = authors_html_output + footer

            with open(parse_json_config(config, "html_directory") + "/author/" + author.lower() + ".html", "w", encoding="utf-8", errors="xmlcharrefreplace") as html_file: # writing author_index_html
                html_file.write(authors_html_output)


    if parse_json_config(config, "generate_tag_index") == True:
        for tags in sorted_posts_tags.values():
            for tag in tags:
                def author_match(post):
                    if tag in sorted_posts_tags.get(post):
                        return True
                    else:
                        return False
                filtered_posts_by_tag = set(filter(author_match, sorted_posts_tags))

                if parse_json_config(config, "use_title_as_file_name") == True:
                    if parse_json_config(config, "add_sortable_date_to_file_name") == False:
                        output_file_path =  "../" + str(posts.get(post)[3]) + "/" + str(posts.get(post)[1]).lower().replace(" ", "-") + ".html"
                    else:
                        output_file_path =  "../" + str(posts.get(post)[3]) + "/" + str(posts.get(post)[0]) + "-" + str(posts.get(post)[1]).lower().replace(" ", "-") + ".html"
                else:
                    if parse_json_config(config, "add_sortable_date_to_file_name") == False:
                        output_file_path =  "../" + str(posts.get(post)[3]) + "/" + post + ".html"
                    else:
                        output_file_path = "../" + str(posts.get(post)[3]) + "/" + str(posts.get(post)[0]) + "-" + post + ".html"

                with open(parse_json_config(config, "header_markdown")) as header_md, open(header_html) as header: # starting tag_index_html
                    header = header.read()
                    header_md = header_md.read()
                    site_title = parse_json_config(config, "site_title")
                    header = header.replace("[[$HEADER_LINK]]", "../index.html")
                    header = header.replace("[[$SITE_TITLE]]", site_title)
                    if templates_directory == "./templates/original":
                        header = header.replace("[[$CSS_FILE]]", "https://cdn.jsdelivr.net/npm/water.css@2/out/water.css")
                    else:
                        header = header.replace("[[$CSS_FILE]]", f"..{html_directory}/styles.css")
                    header = header.replace("[[$CONTENT]]", markdown.markdown(header_md))
                    tags_html_output = header

                for post in filtered_posts_by_tag:
                    with open(index_html) as tags_html_file:
                        tags_html_output += tags_html_file.read()
                        tags_html_output = tags_html_output.replace("[[$FILE_TITLE]]", list_of_posts.get(post)[1])
                        tags_html_output = tags_html_output.replace("[[$LINK]]", output_file_path) 
                        tags_html_output = tags_html_output.replace("[[$FILE_AUTHOR]]", list_of_posts.get(post)[4])
                        if parse_json_config(config, "generate_author_index") == True:
                            tags_html_output = tags_html_output.replace("[[$FILE_AUTHOR_LINK]]", f"../author/{posts.get(post)[4]}.html".lower())
                        tags_html_output = tags_html_output.replace("[[$FILE_DATE]]", list_of_posts.get(post)[2])
                        tags_html_output = tags_html_output.replace("[[$FILE_SUMMARY]]", list_of_posts.get(post)[5])
                        tags_html_tags = posts.get(post)[6]
                        tags_html = "<a href=[[$TAG_LINK]]>[[$TAG]]</a> &nbsp"
                        tags_html_output_string = ""
                        for html_tag in tags_html_tags:
                            tags_html_output_string += tags_html.replace("[[$TAG]]", html_tag).replace("[[$TAG_LINK]]", f"./tags/{html_tag}.html")
                        tags_html_output = tags_html_output.replace("[[$FILE_TAGS]]", tags_html_output_string)

                with open(parse_json_config(config, "footer_markdown")) as footer_md, open(footer_html) as footer: # finishing tag_index_html
                    footer_md = footer_md.read()
                    footer = footer.read()
                    if parse_json_config(config, "generate_about_page") == True:
                        footer = footer.replace("[[$FOOTER_LINK]]", "../about.html").replace("[[$FOOTER_TEXT]]", "About this blog")
                    else:
                        footer = footer.replace("[[$FOOTER_LINK]]", "").replace("[[$FOOTER_TEXT]]", "")
                    footer = footer.replace("[[$CONTENT]]", markdown.markdown(footer_md))
                    tags_html_output = tags_html_output + footer

                with open(parse_json_config(config, "html_directory") + "/tags/" +  tag.lower() + ".html", "w", encoding="utf-8", errors="xmlcharrefreplace") as html_file: # writing tag_index_html
                    html_file.write(tags_html_output)


    if parse_json_config(config, "generate_about_page") == True:
        with open(parse_json_config(config, "about_markdown"), "r", encoding="utf-8") as md_file:
            md_text = md_file.read()
            html = markdown.markdown(md_text)

        with open(parse_json_config(config, "header_markdown")) as header_md, open(header_html) as header:
            header = header.read()
            header_md = header_md.read()
            site_title = parse_json_config(config, "site_title")
            header = header.replace("[[$HEADER_LINK]]", "./index.html")
            header = header.replace("[[$SITE_TITLE]]", site_title)
            if templates_directory == "./templates/original":
                header = header.replace("[[$CSS_FILE]]", "https://cdn.jsdelivr.net/npm/water.css@2/out/water.css")
            else:
                header = header.replace("[[$CSS_FILE]]", f"..{html_directory}/styles.css")
            header = header.replace("[[$CONTENT]]", markdown.markdown(header_md))
            html = header + html

        with open(parse_json_config(config, "footer_markdown")) as footer_md, open(footer_html) as footer:
            footer_md = footer_md.read()
            footer = footer.read()
            if parse_json_config(config, "generate_about_page") == True:
                footer = footer.replace("[[$FOOTER_LINK]]", "./about.html").replace("[[$FOOTER_TEXT]]", "About this blog")
            else:
                footer = footer.replace("[[$FOOTER_LINK]]", "").replace("[[$FOOTER_TEXT]]", "")
            footer = footer.replace("[[$CONTENT]]", markdown.markdown(footer_md))
            html = html + markdown.markdown(footer)

        with open(parse_json_config(config, "html_directory") + "about.html", "w", encoding="utf-8", errors="xmlcharrefreplace") as html_file:
                html_file.write(html)


main()

