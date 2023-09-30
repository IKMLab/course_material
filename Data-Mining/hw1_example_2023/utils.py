import csv
import logging
import time
from collections import Counter, defaultdict
from itertools import chain, combinations
from pathlib import Path
from typing import Any, List, Tuple, Union


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        print(f"Running {func.__name__} ...", end='\r')
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} Done in {end - start:.2f} seconds")
        return result
    return wrapper

@timer
def read_file(filename: Union[str, Path]) -> List[List[int]]:
    """read_file

    Args:
        filename (Union[str, Path]): The filename to read

    Returns:
        List[List[int]]: The data in the file
    """
    return [
        [x for x in line.split()]
        #
        for line in Path(filename).read_text().splitlines()
    ]

@timer
def write_file(data: List[Tuple[Any]], filename: Union[str, Path]) -> None:
    """write_file writes the data to a csv file and
    adds a header row with `antecedent`, `consequent`, `support`, `confidence`, `lift`.
    You can revise the function but please make sure your output is the same as ours
    (See `outputs/example-fp_growth-0.1-0.3.csv` for example).

    Args:
        data (List[Tuple[Any]]): The data to write to the file
        filename (Union[str, Path]): The filename to write to
    """
    proc_data = []
    for rule in data:
        PREC = 2
        # you can modify this line if your "data" has different formats
        a, c, sup, conf, lift = rule # antecedent, consequent, support, confidence, lift

        a, c = list(set(a)), list(set(c))
        sup = round(sup, PREC)
        conf = round(conf, PREC)
        lift = round(lift, PREC)
        proc_data.append([a, c, sup, conf, lift])

    with open(filename, 'w') as f:
        writer = csv.writer(f)
        # rule format: antecedent --> consequent
        writer.writerow(["antecedent", "consequent",
                        "support", "confidence", "lift"])
        writer.writerows(proc_data)




def setup_logger():
    l = logging.getLogger('l')

    log_dir: Path = Path(__file__).parent / "logs"

    # create log directory if not exists
    log_dir.mkdir(parents=True, exist_ok=True)

    # set log file name
    log_file_name = f"{time.strftime('%Y%m%d_%H%M%S')}.log"

    l.setLevel(logging.DEBUG)

    fileHandler = logging.FileHandler(
        filename=log_dir / log_file_name,
        mode='w'
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

l = setup_logger()