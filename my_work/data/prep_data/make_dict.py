import re
import json

path = "prep.csv"
old_file = "old.csv"
new_file = "new.csv"


def divide(path):
    with open(path) as f:
        all_of_it = f.read()
    ind = all_of_it.find("The New Testament of the King James Bible")
    old_test = all_of_it[:ind]
    new_test = all_of_it[ind:]
    return old_test,new_test


def write_files(old,new):
    with open(old_file,"w") as o:
        o.write(old)
    with open(new_file,"w") as n:
        n.write(new)

def conquer(string,file):
    ind = 0
    boolean = True
    f = open(file, "w")
    for i in range(len(string)):
        try:
            int(string[i])
            if boolean == True:
                pass
            else:
                pass
            i+=4
        except:
            pass
    f.close()


def format(s):
    if s[3] == " ":
        print(s[2] + s[1] + ' "' + s[4:] + '",')
    else:
        print(s[2:4] + s[1] + ' "' + s[5:] + '",')



def parse_kjv_text_with_mapping(file_path, output_json_path):
    """
    Parse raw KJV text into JSON using book_mapping.
    """

    # Mapping raw book titles -> canonical names
    book_mapping = {
        "The First Book of Moses: Called Genesis": "Genesis",
        "The Second Book of Moses: Called Exodus": "Exodus",
        "The Third Book of Moses: Called Leviticus": "Leviticus",
        "The Fourth Book of Moses: Called Numbers": "Numbers",
        "The Fifth Book of Moses: Called Deuteronomy": "Deuteronomy",
        "The Book of Joshua": "Joshua",
        "The Book of Judges": "Judges",
        "The Book of Ruth": "Ruth",
        "The First Book of Samuel": "1 Samuel",
        "The Second Book of Samuel": "2 Samuel",
        "The Third Book of the Kings": "1 Kings",
        "The Fourth Book of the Kings": "2 Kings",
        "The First Book of the Chronicles": "1 Chronicles",
        "The Second Book of the Chronicles": "2 Chronicles",
        "Ezra": "Ezra",
        "The Book of Nehemiah": "Nehemiah",
        "The Book of Esther": "Esther",
        "The Book of Job": "Job",
        "The Book of Psalms": "Psalms",
        "The Proverbs": "Proverbs",
        "Ecclesiastes": "Ecclesiastes",
        "The Song of Solomon": "Song of Solomon",
        "The Book of the Prophet Isaiah": "Isaiah",
        "The Book of the Prophet Jeremiah": "Jeremiah",
        "The Lamentations of Jeremiah": "Lamentations",
        "The Book of the Prophet Ezekiel": "Ezekiel",
        "The Book of Daniel": "Daniel",
        "Hosea": "Hosea",
        "Joel": "Joel",
        "Amos": "Amos",
        "Obadiah": "Obadiah",
        "Jonah": "Jonah",
        "Micah": "Micah",
        "Nahum": "Nahum",
        "Habakkuk": "Habakkuk",
        "Zephaniah": "Zephaniah",
        "Haggai": "Haggai",
        "Zechariah": "Zechariah",
        "Malachi": "Malachi",
        # New Testament
        "The Gospel According to Saint Matthew": "Matthew",
        "The Gospel According to Saint Mark": "Mark",
        "The Gospel According to Saint Luke": "Luke",
        "The Gospel According to Saint John": "John",
        "The Acts of the Apostles": "Acts",
        "The Epistle of Paul the Apostle to the Romans": "Romans",
        "The First Epistle of Paul the Apostle to the Corinthians": "1 Corinthians",
        "The Second Epistle of Paul the Apostle to the Corinthians": "2 Corinthians",
        "The Epistle of Paul the Apostle to the Galatians": "Galatians",
        "The Epistle of Paul the Apostle to the Ephesians": "Ephesians",
        "The Epistle of Paul the Apostle to the Philippians": "Philippians",
        "The Epistle of Paul the Apostle to the Colossians": "Colossians",
        "The First Epistle of Paul the Apostle to the Thessalonians": "1 Thessalonians",
        "The Second Epistle of Paul the Apostle to the Thessalonians": "2 Thessalonians",
        "The First Epistle of Paul the Apostle to Timothy": "1 Timothy",
        "The Second Epistle of Paul the Apostle to Timothy": "2 Timothy",
        "The Epistle of Paul the Apostle to Titus": "Titus",
        "The Epistle of Paul the Apostle to Philemon": "Philemon",
        "The Epistle of Paul the Apostle to the Hebrews": "Hebrews",
        "The General Epistle of James": "James",
        "The First Epistle General of Peter": "1 Peter",
        "The Second General Epistle of Peter": "2 Peter",
        "The First Epistle General of John": "1 John",
        "The Second Epistle General of John": "2 John",
        "The Third Epistle General of John": "3 John",
        "The General Epistle of Jude": "Jude",
        "The Revelation of Saint John the Divine": "Revelation"
    }

    # Keep track of which canonical books are Old vs New Testament
    old_testament_books = {
        "Genesis","Exodus","Leviticus","Numbers","Deuteronomy",
        "Joshua","Judges","Ruth","1 Samuel","2 Samuel",
        "1 Kings","2 Kings","1 Chronicles","2 Chronicles",
        "Ezra","Nehemiah","Esther","Job","Psalms","Proverbs",
        "Ecclesiastes","Song of Solomon","Isaiah","Jeremiah","Lamentations",
        "Ezekiel","Daniel","Hosea","Joel","Amos","Obadiah",
        "Jonah","Micah","Nahum","Habakkuk","Zephaniah",
        "Haggai","Zechariah","Malachi"
    }

    scripture_dict = {"The Old Testament": {}, "The New Testament": {}}

    # Read entire text as a single string
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Normalize line breaks
    text = text.replace('\r\n', '\n').replace('\r', '\n')

    current_book = None
    current_testament = None

    # Detect book headers and split
    book_headers = sorted(book_mapping.keys(), key=lambda x: -len(x))  # longest first to avoid partial matches
    for header in book_headers:
        # Replace header with a unique marker
        text = text.replace(header, f"\n###BOOKSTART###{header}###\n")

    # Split by book markers
    books = re.split(r"\n###BOOKSTART###(.*?)###\n", text)
    # The split results in: ['', header1, content1, header2, content2, ...]
    for i in range(1, len(books), 2):
        raw_header = books[i].strip()
        content = books[i+1]
        canonical_book = book_mapping[raw_header]
        current_book = canonical_book
        current_testament = "The Old Testament" if canonical_book in old_testament_books else "The New Testament"
        scripture_dict[current_testament][current_book] = {}

        # Match all verses in content
        verse_pattern = re.compile(r'(\d+)[.:](\d+)\s+(.+?)(?=(\d+[.:]\d+)|$)', re.DOTALL)
        for match in verse_pattern.finditer(content):
            chapter = int(match.group(1))
            verse = int(match.group(2))
            verse_text = match.group(3).replace("\n", " ").strip()
            if chapter not in scripture_dict[current_testament][current_book]:
                scripture_dict[current_testament][current_book][chapter] = {}
            scripture_dict[current_testament][current_book][chapter][verse] = verse_text

    # Save JSON
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(scripture_dict, f, indent=2, ensure_ascii=False)

    print(f"Saved JSON to {output_json_path}")

parse_kjv_text_with_mapping("prep.csv","scripture.json")