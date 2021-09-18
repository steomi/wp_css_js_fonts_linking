import os


def get_name(word):
    for letter in word:
        if letter == ".":
            word = word.replace(letter, "-")
    return word.lower()


def get_extension(word):
    return os.path.splitext(word)[1]


def is_font(word):
    extension = get_extension(word)
    fonts_extensions = ['.otf', '.ttf', '.eot', '.woff', '.woff2']
    if extension in fonts_extensions:
        return True
    else:
        return False


file = open('RESULT.txt', 'w')

path = os.getcwd()

functionName = str(input("The name of the function that connects scripts and styles (add_theme_scripts): ")
                   or "add_theme_scripts")
isJquery = str(input("Is there jQuery in the project? (Default: no, print yes, if you use jQuery in project): ")
               or "no")
pathToJs = str(input("Scripts in the theme folder (Default: /assets/js/): ") or "/assets/js/")
pathToCss = str(input("Styles in the theme folder (Default: /assets/css/): ") or "/assets/css/")
pathToFonts = str(input("Fonts in the theme folder (Default: /assets/fonts/): ") or "/assets/fonts/")

if isJquery.lower() == "yes":
    isJquery = True
else:
    isJquery = False

scriptsLines = []
stylesLines = []
fontsLines = []

file.write("/**" + '\n' + "* Enqueue scripts and styles." + '\n' + "*/" + '\n')
file.write("function " + functionName + "() {" + '\n')

with os.scandir(path) as listOfEntries:
    for entry in listOfEntries:
        if entry.is_file():
            if ".js" in entry.name:
                if isJquery:
                    scriptsLines.append("    wp_enqueue_script('jquery');")
                    isJquery = False

                scriptsLines.append("    wp_enqueue_script('" + get_name(entry.name)
                                    + "', get_template_directory_uri() . '" + pathToJs + entry.name
                                    + "', array(), '1.0.0', true );")

            elif ".css" in entry.name:
                stylesLines.append("    wp_enqueue_style('" + get_name(entry.name)
                                   + "', get_template_directory_uri() . '"
                                   + pathToCss + entry.name + "', array(), '1.0.0' );")

            elif is_font(entry.name):
                fontsLines.append("    wp_enqueue_style('" + get_name(entry.name)
                                  + "', get_template_directory_uri() . '"
                                  + pathToCss + entry.name + "', array(), '1.0.0' );")


file.write("    // Theme scripts" + '\n')
for line in scriptsLines:
    file.write(line + '\n')

for line in range(0, 2):
    file.write('\n')

file.write("    // Theme styles" + '\n')
for line in stylesLines:
    file.write(line + '\n')

for line in range(0, 2):
    file.write('\n')

file.write("    // Theme fonts" + '\n')
for line in fontsLines:
    file.write(line + '\n')


file.write("}" + '\n')
file.write('\n')
file.write("add_action( 'wp_enqueue_scripts', '" + functionName + "' );" + '\n')

file.close()
