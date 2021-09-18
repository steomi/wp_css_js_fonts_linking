import os


def get_name(word):
    for letter in word:
        if letter == ".":
            word = word.replace(letter, "-")
    return word


def get_extension(word):
    return os.path.splitext(word)[1]


def is_font(word):
    extension = get_extension(word)
    fonts_extensions = ['.otf', '.ttf', '.eot']
    if extension in fonts_extensions:
        return True
    else:
        return False


file = open('functions.txt', 'w')

path = os.getcwd()

functionName = str(input("Название функции, которая подключает скрипты и стили (theme_name_scripts): "))
isJquery = str(input("Есть jQuery в проекте? (да/нет): "))
pathToJs = str(input("Скрипты в папке темы (/assets/js/): "))
pathToCss = str(input("Стили в папке темы (/assets/css/): "))
pathToFonts = str(input("Шрифты в папке темы (/assets/fonts/): "))

if isJquery.lower() == "да":
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
        # печать всех записей, являющихся файлами
        if entry.is_file():
            if ".js" in entry.name:
                if isJquery:
                    scriptsLines.append("    wp_enqueue_script('jquery');")
                    isJquery = False

                scriptsLines.append("    wp_enqueue_script('" + get_name(entry.name) + "', get_template_directory_uri() . '" + pathToJs + entry.name + "', array(), '1.0.0', true );")

            elif ".css" in entry.name:
                stylesLines.append("    wp_enqueue_style('" + get_name(entry.name) + "', get_template_directory_uri() . '" + pathToCss + entry.name + "', array(), '1.0.0' );")

            elif is_font(entry.name):
                fontsLines.append("    wp_enqueue_style('" + get_name(entry.name) + "', get_template_directory_uri() . '" + pathToCss + entry.name + "', array(), '1.0.0' );")


file.write("    // Scripts" + '\n')
for line in scriptsLines:
    file.write(line + '\n')

for line in range(0, 2):
    file.write('\n')

file.write("    // Styles" + '\n')
for line in stylesLines:
    file.write(line + '\n')

for line in range(0, 2):
    file.write('\n')

file.write("    // Fonts" + '\n')
for line in fontsLines:
    file.write(line + '\n')


file.write("}" + '\n')
file.write('\n')
file.write("add_action( 'wp_enqueue_scripts', '" + functionName + "' );" + '\n')

file.close()
