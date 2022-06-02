# Welcome to downthon_AB

## What is downthon_AB?

downthon_AB is a simple Python script that can turn a folder of Markdown formatted .txt or .md files into a reasonable facsimile of a blog, more or less. It can serve as a simple, feature-light, flat file blogging platform, or could be used to convert a folder of text or markdown notes into a more organized format.

downthon_AB is also my very first coding project. I am starting on my journey of learning to code and this is the project I picked as my starter. I had the idea many years ago, back when new blogging platforms were all the rage, and it seemed like a good choice.

Given that, please have appropriate expectations for how usable or stable this is for anything other than just casual usage.

## What's with the name?

The name is a concatenation of the end of the words Markdown and Python. Obviously. 🙂

## How do I use it?

Just download the files and folders above and place them in a folder in your computer. You will also need to install [Python](https://www.python.org/) and [Python-Markdown](https://python-markdown.github.io/). Then you can run the downthon_AB.py script from a command terminal and the files in the /markdown folder will be recreated as .html files in the /html folder.

You do not have to use any special formatting, or indeed any formatting at all, for the script to work. That said, if you pattern your files after the example_post_format.md file above, the script has more direct context to work with and will generally produce better results.

Please look at the default /markdown folder and /html folder to see an example of input and output.

## Can I customize anything in my blog?

Yes! In the /config folder there is a file called config.json that allows you to adjust several variables, e.g. the location of the input folder or output folder.

One thing you will _definitely_ want to change is the default information entered in the header.md, footer.md, swag.md, and about.md files also located in the /config folder. The header and footer files are added to every file created by the script, the swag file is added to each individual post, and the about.md is rendered as a separate about.html file.

You will also probably want to change the "site_title" and "default_author" option in config.json.

If you want to create a separate set of .html templates, copy the files in the /templates/original folder and move them to a newly created folder inside /templates. Then edit the files as you wish, and change the "templates_directory" option in config.json to your new folder. You will need to place your CSS in a styles.css file inside the /html folder you are outputting to.

## Are you going to keep developing downthon_AB?

Maybe.

Owing to this being my first project, quite a lot of this script could use some improvement. I know there are a ton of things I did in convoluted ways that could be streamlined, and I know some of the areas where I am repeating myself could be refactored into cleaner, better written code. And it might be a good exercise to do the work to make those changes, or even add new features, as a part of learning.

On the other hand, I'm sure there are other tools that do the same thing, likely better, so I'm not sure if there's much value in this as a continuing concern. We'll see.

## Given the first part of your answer above, would you be willing to entertain some constructive feedback on this project?

I would _**love**_ constructive feedback. If anyone reading this has any insights to share on better ways of doing anything I am doing wrong, please feel free to share.

## Random bullet point points

* If you do not wish to use the default date formatting, it can be changed in the config.json file in the /config folder. You do need to have 4 capital 'Y's in a row, 2 capital 'D's in a row, 2 capital 'M's in a row, 2 capital 'H's in a row, two lower case 'm's in a row, and the string [AM/PM] in your date format, but outside of that you can arrange and delimit those elements in any way you wish.
  * If you have changed the option for a 24 hour clock to True, then you can ignore the [AM/PM] string.
  * If you don't follow the format listed above, then it is probable that the script will interpret your dates incorrectly.
* I don't know much about HTML or CSS so I'm grateful for the existence of [Water.css](https://watercss.kognise.dev/) to style the output .html files.
* If I do come back to add more features, the first two would be as follows:
  * Adding pagination to the main index.html file. Currently, everything that the script sees as a post ends up on that file, so it could get over-large with enough posts.
  * Adding a sidebar to the output HTML files.
