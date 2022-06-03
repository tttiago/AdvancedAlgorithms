"""Preprocess the book in the different languages."""

from glob import glob
import nltk
import re

try:
    from nltk.corpus import stopwords
    _ = stopwords.words('english')
except LookupError:
    nltk.download('stopwords')


BOOK_PATH = './book'
LANGS = {'pt': 'portuguese', 'en': 'english', 'fr': 'french'}
ADD_STOPWORDS = {
    'pt':   ['á', 'ás', 'delles', 'elles', 'aquelles', 'aquelle', 'd', 'n',
             'ha', 'havia', 'ser', 'ainda', 'j', 't', 'tal', 'porque',
             'ter', 'elle', 'lá', 'lo', 'todos'],
    'en':   ['would', 'j', 'could', 'must', 'every', 'like', 'much', 
             'therefore', 'one', 'upon'],
    'fr':   ['cette', 'être', 'a', 'si', 'donc', 'sans', 'dit', 'plus', 'comme',
            'tout', 'là', 'peu', 'dont', 'où', 'alors', 'tous'],
}

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


def process_words(file):
    """Removes punctuation, common stop words and saves words in lowercase."""

    with open(file, 'r') as f:
        text = f.read()

    lang = file.split('/')[-1][:2]

    # Import list of stopwords and add custom words.
    sw_nltk = stopwords.words(LANGS[lang])
    sw_nltk.extend(ADD_STOPWORDS[lang])
    stop_words = " ".join(sorted(sw_nltk))
    
    # Remove ' in the stopwords and convert back to list. 
    stop_words = re.sub(r'[\']', '', stop_words).split()

    # Remove all non-word characters.
    text = re.sub(r'[^\w\s]', ' ', text)
    # Remove all numbers.
    text = re.sub(r'[0-9]', '', text)
    # Take care of remaining underscores.
    text = re.sub(r'[\_]', '', text)

    # Add all words not in stop_words to a string, in lowercase.
    words = [word.lower() for word in text.split() 
                            if word.lower() not in stop_words]
    new_text = " ".join(words)
    
    # Write the processed text to a new file.
    with open(f'{BOOK_PATH}/{lang}_processed.txt', 'w') as f:
        f.write(new_text)   
    

for file in glob(f'{BOOK_PATH}/*_original.txt'):
    trim_text(file)

for file in glob(f'{BOOK_PATH}/*_trimmed.txt'):
    process_words(file)