import time, os
from datetime import datetime, timedelta
from matplotlib import pyplot as plt

from algo import OrdersManager

def process_things(num_orders=1_000,num_threads=None, type_of_processing='threading'):
    orders_manager = OrdersManager(num_orders)
    if type_of_processing  == 'linear':
        start_time = time.time()
        orders_manager.process_orders()
        # wait for all threads to finish
        for thr in orders_manager.list_threads:
            thr.join()
        delay = time.time() - start_time
        print(f"{datetime.now()} > Tiempo de ejecucion: {delay} segundos...")
        return delay

    if type_of_processing  == 'threading':
        start_time = time.time()
        orders_manager.process_thread_orders(num_threads)
        # wait for all threads to finish
        for thr in orders_manager.list_threads:
            thr.join()
        delay = time.time() - start_time
        print(f"{datetime.now()} > Tiempo de ejecucion: {delay} segundos...")
        return delay
    else:
        print('you need to choose between "linear" or "threading" in the type_of_processing argument')

'''
Vamos a comparar los resultados de el algoritmo orginal y el de threading
'''

# orders_manager = OrdersManager(num_orders=100)
# #delay2 = process_things(type_of_processing='linear')
# delay1 = process_things(num_threads=5, type_of_processing='threading')

sample_sizes = [10, 50, 100, 500]
delays_threading = []
for sample in sample_sizes:
    current_delay = process_things(num_orders=sample,num_threads=10, type_of_processing='threading')
    delays_threading.append(current_delay)

print(sample_sizes, delays_threading)

## dibujar el processo tipo threading
fig = plt.figure()
plt.title('blue = original_algo, red = new_algo')
plt.xlabel('Sample sizes')
plt.ylabel('Execution Time')

plt.scatter(sample_sizes, delays_threading, c='red', label='og')

#### dsfd ########
delays_linear = []
for sample in sample_sizes:
    current_delay = process_things(num_orders=sample,num_threads=None, type_of_processing='linear')
    delays_linear.append(current_delay)
## dibujar el proceso normal
plt.scatter(sample_sizes, delays_linear, c='blue', label='dd')
plt.show()

fig.savefig('files/graph.png')
