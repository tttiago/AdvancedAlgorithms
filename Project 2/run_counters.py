"""Run the counters in the books."""

from counters import *

from glob import glob
import json


BOOK_PATH = './book'
RESULTS_PATH = './results'


def main(funcs=(det_count, fix_prob_count, dec_prob_count), n_counts=1000):
    
    if det_count in funcs:
        print('Running the deterministic counter...')
        det_results = {}
        for file in glob(f'{BOOK_PATH}/*_letters.txt'):
            lang = file.split('/')[-1][:2]
            print(f'\tlanguage: {lang.upper()} ...', end='')
            det_results[lang] = det_count(file)
            print(' DONE')

        print('ALL DONE.', end=' ')
        with open(f'{RESULTS_PATH}/det_counter.json', 'w', ) as f:
            json.dump(det_results, f, indent=4)
        print('RESULTS SAVED.')

    if fix_prob_count in funcs:
        print('\nRunning the fixed probability counter...')
        fix_prob_results = {}
        for file in glob(f'{BOOK_PATH}/*_letters.txt'):
            lang = file.split('/')[-1][:2]
            print(f'\tlanguage: {lang.upper()} ...', end='', flush=True)
            fix_prob_results[lang] = fix_prob_count(file, prob=1/16, 
                                                    n_counts=n_counts)
            print(' DONE')
        print('ALL DONE.', end=' ')
        with open(f'{RESULTS_PATH}/fix_prob_counter_x{n_counts}.json', 'w', ) as f:
            json.dump(fix_prob_results, f, indent=4)
        print('RESULTS SAVED.')

    if dec_prob_count in funcs:
        print('\nRunning the decreasing probability counter...')
        dec_prob_results = {}
        for file in glob(f'{BOOK_PATH}/*_letters.txt'):
            lang = file.split('/')[-1][:2]
            print(f'\tlanguage: {lang.upper()} ...', end='', flush=True)
            dec_prob_results[lang] = dec_prob_count(file, denominator=2, 
                                                    n_counts=n_counts)
            print(' DONE')
        print('ALL DONE.', end=' ')
        with open(f'{RESULTS_PATH}/dec_prob_counter_x{n_counts}.json', 'w', ) as f:
            json.dump(dec_prob_results, f, indent=4)
        print('RESULTS SAVED.')


if __name__ == '__main__':
    main(funcs=(dec_prob_count, ), n_counts=900)