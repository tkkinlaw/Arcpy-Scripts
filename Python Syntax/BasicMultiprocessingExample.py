# This is a simple example of how to get started with the multiprocessing package
import time
import multiprocessing

# This function squares a value. 
def square_value(number):
    # Simulate some time-consuming computation
    time.sleep(1)
    return number ** 2

# This function uses the square_value function when using the "normal" technique for processing data
def normal_execution():
    numbers = [1, 2, 3, 4, 5]
    start_time = time.time()
    results = [square_value(number) for number in numbers]
    end_time = time.time()

    print(f'Normal execution:')
    print(f"Results: {results}")
    print(f"Execution time: {end_time - start_time} seconds")

# This function uses the square_value function using multiprocessing for the data
def parallel_execution():
    numbers = [1, 2, 3, 4, 5]
    num_processes = multiprocessing.cpu_count()

    start_time = time.time()

    pool = multiprocessing.Pool(processes=num_processes)
    results = pool.map(square_value, numbers)

    end_time = time.time()
    pool.close()
    pool.join()

    print(f"Parallel execution (using, {num_processes} processes): ")
    print(f"Results: {results}")
    print(f"Execution time: {end_time - start_time} seconds")

if __name__ == '__main__':
    normal_execution()
    print()
    parallel_execution()
