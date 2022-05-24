# Welcome to whatever_i_end_up_calling_this

## What is whatever_i_end_up_calling_this?

whatever_i_end_up_calling_this is a simple Python script that can turn a folder of Markdown formatted files into a reasonable facsimile of a blog. It can serve as a simple, feature-light, flat file blogging platform, or could be used to convert a folder of text or markdown notes into a more organized format.

whatever_i_end_up_calling_this is also my very first programming project. I am starting on my journey of learning to code and this is the project I picked as my first. I had the idea of a simple script that converted text files into a static blog many years ago, back when new blogging platforms were all the rage, and it seemed like a good choice when I started thinking of options for a first project.

## How do I use it?

Just download the files and folders and place them in a folder in your computer. You will also need to install Python and Python-Markdown. Then you can run the whatever_i_end_up_calling_this.py script and the files in the /markdown folder will be recreated as .html files in the /html folder.

You do not have to use any special formatting, or indeed any formatting at all, for the script to work. That said, if you pattern your files after the example_post_format.md file above, the script has more direct context to work with and will generally produce better results.

## Can I customize anything in my blog?

Yes! In the /config folder there is a file called config.json that allows you to adjust several variables, e.g. the location of the input folder or output folder.

One thing you will _definitely_ want to change is the default information entered in the header.md, footer.md, swag.md, and about.md files also located in the /config folder. The header and footer files are added to every file created by the script, the swag file is added to each individual post, and the about.md is rendered as a separate about.html file.

You can also edit the associated .html files if you wish.

## Are you going to keep developing whatever_i_end_up_calling_this?

Maybe? Owing to this being my first project, quite a lot of this could use some improvement. And it might be a good exercise to do the work to make those changes, or even add new features. On the other hand, I am sure there are other tools that do this same thing, so I am not sure if there is much value in 
