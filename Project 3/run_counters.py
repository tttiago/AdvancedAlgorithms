"""Run the counters in the books."""

from counters import *

from glob import glob
import pickle


BOOK_PATH = './book'
RESULTS_PATH = './results'


def main(funcs=(det_count, cm_sketch), k=3e2, d=5, m=None):
    
    if det_count in funcs:
        print('Running the deterministic counter...')
        det_results = {}
        for file in glob(f'{BOOK_PATH}/*_processed.txt'):
            lang = file.split('/')[-1][:2]
            print(f'\tlanguage: {lang.upper()} ...', end='')
            det_results[lang] = det_count(file)
            print(' DONE')

        print('ALL DONE.', end=' ')
        with open(f'{RESULTS_PATH}/det_counter.pkl', 'wb') as f:
            pickle.dump(det_results, f)
        print('RESULTS SAVED.')

    if cm_sketch in funcs:
        print('\nRunning the CM Sketch counter...')
        cm_sketch_results = {}
        for file in glob(f'{BOOK_PATH}/*_processed.txt'):
            lang = file.split('/')[-1][:2]
            print(f'\tlanguage: {lang.upper()} ...', end='', flush=True)
            counter, params = cm_sketch(file, k=k, d=d, m=m)
            cm_sketch_results[lang] = counter
            print(' DONE')

        m, d = params['m'], params['d']
        print(f'CM Sketch with {m} columns and {d} rows')
        print('ALL DONE.', end=' ')

        str_m = str(m).zfill(5)
        str_d = str(d).zfill(2)
        fname_desc = f'm={str_m}_d={str_d}'    
        with open(f'{RESULTS_PATH}/cm_sketch_{fname_desc}.pkl', 'wb', ) as f:
            pickle.dump(cm_sketch_results, f)
        print('RESULTS SAVED.')
   

if __name__ == '__main__':

    # Run the deterministic counter once.
    main(funcs=(det_count, ))

    # Run the CM-Sketch in the parameter grid.
    for m in (12, 40, 120, 400, 600, 900, 1200, 
              1500, 2000, 3000, 4000, 6000, 12000):
        for d in range(1, 11):
            main(funcs=(cm_sketch, ), m=m, d=d)
    