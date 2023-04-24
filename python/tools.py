from functools import wraps
from itertools import islice
import time


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function "{func.__name__}" took {total_time:.4f} seconds')
        return result
    return timeit_wrapper


def chunks(input, chunk_size: int) -> list[list]:
    output = []

    nb_chunks = len(input) // chunk_size + (1 if len(input) % chunk_size != 0 else 0)

    for i in range(0, nb_chunks):
        output.append(list(islice(input, i*chunk_size, chunk_size*(i+1))))

    return output


def chunks_iter(input, chunk_size: int):

    nb_chunks = len(input) // chunk_size + (1 if len(input) % chunk_size != 0 else 0)

    for i in range(0, nb_chunks):
        yield islice(input, i*chunk_size, chunk_size*(i+1))
