'''Functions for data loading, cleaning and preparing '''
import logging
import pandas as pd


def get_shape_csv(file_path: str) -> tuple[int, int] | tuple[None, None]:
    '''Get the size of a CSV data file without loading'''
    try:
        df = pd.read_csv(file_path, nrows=0)
        return df.shape
    except FileNotFoundError as e:
        logging.info("File not found: %e", e)
    except pd.errors.ParserError as e:
        logging.info("Parsing error: %e", e)
    except pd.errors.EmptyDataError as e:
        logging.info("Empty file: %e", e)
    except UnicodeDecodeError as e:
        logging.info("Decode error: %e", e)

    return (None, None)


def get_random_sample(
        file_path: str,
        sample_size: int) -> pd.DataFrame | None:
    '''Get a random sample of given size from a CSV'''
    try:
        df = pd.read_csv(file_path)
        sample = df.sample(sample_size)
        return sample
    except FileNotFoundError as e:
        logging.info("File not found: %e", e)
    except pd.errors.ParserError as e:
        logging.info("Parsing error: %e", e)
    except pd.errors.EmptyDataError as e:
        logging.info("Empty file: %e", e)
    except MemoryError as e:
        logging.info("File too large: %e", e)
    except ValueError as e:
        logging.info("Sample size is too large: %e", e)

    return
