import multiprocessing as mp
import requests

def my_func(x):
    for i in range(x):
        try:
            print(requests.get('http://127.0.0.1:5000/'))
        except:
            continue

def main():
    pool = mp.Pool(60)
    pool.map(my_func, range(0, 80000))
if __name__ == "__main__":

    main()