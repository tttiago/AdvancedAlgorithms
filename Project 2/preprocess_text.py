"""Preprocess the book in the different languages."""

from glob import glob
import re
from unidecode import unidecode


BOOK_PATH = './book'


def trim_text(file):
    """Removes the Project Gutenberg file headers, notes, 
    and license information. In the case of the English text, also removes the 
    sequel book that follows the book of interest."""

    with open(file, 'r') as f:
        contents = f.read()

    # Find the indices of the starting and ending strings.
    lang = file.split('/')[-1][:2]
    if lang == 'pt':
        start_idx = contents.find('CAPITULO I')
        end_idx = contents.find('FIM DE «DA TERRA Á LUA».')
    elif lang == 'en':
        start_idx = contents.find('CHAPTER I.')
        end_idx = contents.find('(FOR SEQUEL, SEE "AROUND THE MOON.")')
    elif lang == 'fr':
        start_idx = contents.find('''I
                         --------------------''')
        end_idx = contents.find('End of the Project Gutenberg EBook')

    contents = contents[start_idx:end_idx]
    
    # Write the trimmed content to a new file.
    with open(f'{BOOK_PATH}/{lang}_trimmed.txt', 'w') as f:
        f.write(contents)        


def convert_letters(file):
    """Converts all letters to block capitals, while removing all
    non-alphabetic characters. Accented characters
    are transformed in the corresponding "regular" character."""

    with open(file, 'r') as f:
        contents = f.read()

    contents = unidecode(contents).upper()
    contents = re.sub(r'[^A-Z\s]', '', contents)

    lang = file.split('/')[-1][:2]
    
    # Write the cleaned up content (with spaces) to a new file.
    with open(f'{BOOK_PATH}/{lang}_letters_readable.txt', 'w') as f:
        f.write(contents)

    contents = re.sub(r'[^A-Z]', '', contents)
    # Write the cleaned up content (only letters) to a nee file.
    with open(f'{BOOK_PATH}/{lang}_letters.txt', 'w') as f:
        f.write(contents)


for file in glob(f'{BOOK_PATH}/*_original.txt'):
    trim_text(file)

for file in glob(f'{BOOK_PATH}/*_trimmed.txt'):
    convert_letters(file)