'''
@File    :   grading.py
@Time    :   2023/09/28 15:24:37
@Author  :   Ching-Wen Yang
@Version :   1.0
@Contact :   P76114511@gs.ncku.edu.tw
@Desc    :   Grading script for Data Mining Project 1
             Your file should be a csv in the following format:

                antecedent,consequent,support,confidence,lift
                ['18'],['14'],0.53,0.75,1.04
                ['14'],['18'],0.53,0.74,1.04
                ['34'],['18'],0.47,0.73,1.03
                ['18'],['34'],0.47,0.66,1.03
                ['34'],['14'],0.47,0.74,1.03
                ...
@Usage   :  python3 grading.py --file_path=your_file_path --reference_path=reference_file_path --log_path=log_file_path
            --file_path: the path to your file
            --reference_path: the path to the correct answer
            --log_path: the path to the log file
'''

import logging
from argparse import ArgumentParser
from collections import namedtuple
from pathlib import Path

import pandas as pd

# from utils import timer

# ==== Variables ====
PRECISION = 2
# ===================
RuleTuple = namedtuple('RuleTuple', ['antecedent', 'consequent', 'lift', 'confidence', 'support'])


def setup_logger(log_path: str):
    l = logging.getLogger('l')


    # create log directory if not exists
    log_dir = Path(log_path).parent
    log_dir.mkdir(parents=True, exist_ok=True)

    l.setLevel(logging.DEBUG)

    fileHandler = logging.FileHandler(
        filename=log_path,
        mode='a'
    )
    streamHandler = logging.StreamHandler()

    allFormatter = logging.Formatter(
        "%(asctime)s [%(filename)s:%(lineno)d] %(levelname)s: %(message)s"
    )

    fileHandler.setFormatter(allFormatter)
    fileHandler.setLevel(logging.INFO)

    streamHandler.setFormatter(allFormatter)
    streamHandler.setLevel(logging.INFO)

    l.addHandler(streamHandler)
    l.addHandler(fileHandler)

    return l


def read_csv(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)


def turn_row_to_tuple(row: pd.Series) -> RuleTuple:
    # for antecedent, consequent, sort the set first
    # then turn it into a string
    ante = sorted(eval(row['antecedent']))
    csqt = sorted(eval(row['consequent']))
    ante = str(ante)
    csqt = str(csqt)
    lift, conf, sup = row['lift'], row['confidence'], row['support']
    # rounding to precision 2
    lift = round(lift, PRECISION)
    conf = round(conf, PRECISION)
    sup = round(sup, PRECISION)
    return RuleTuple(ante, csqt, lift, conf, sup)

def main(args: ArgumentParser) -> None:

    file_path = args.file_path
    reference_path  = args.reference_path
    data = read_csv(file_path)
    reference = read_csv(reference_path)
    data_set = set(); reference_set = set()
    for _, row in data.iterrows():
        data_set.add(turn_row_to_tuple(row))
    for _, row in reference.iterrows():
        reference_set.add(turn_row_to_tuple(row))

    logger.info("================= Filepaths =================")
    logger.info(f'input file: {file_path}')
    logger.info(f'reference file: {reference_path}')

    # "['34', '14']",['18'],0.36,0.76,1.08

    # check and list their difference
    pass_flag = True
    if len(data_set) != len(reference_set):
        pass_flag = False
        logger.info(f'length of rules in test file and reference are not equal, reference: {len(reference_set)}, test files: {len(data_set)}')
    logger.info("Rules not in reference:")
    for rule in data_set:
        if rule not in reference_set:
            pass_flag = False
            logger.info(f'{rule}')
    logger.info("=================Results=================")
    logger.info(f'Pass: {pass_flag}')

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--file_path', type=str, default='./outputs/example-fp_growth-0.1-0.1.csv')
    parser.add_argument('--reference_path', type=str, default='./outputs/example-fp_growth-0.1-0.1.csv')
    parser.add_argument('--log_path', type=str, default='grading_logs/example.log')
    args = parser.parse_args()
    logger = setup_logger(args.log_path)
    try:
        main(args)
    except Exception as e:
        logger.exception(e)



