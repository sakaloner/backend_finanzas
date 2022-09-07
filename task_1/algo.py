from datetime import datetime, timedelta
import json
import time
import uuid
import random

from threading import Thread

## Function to make uuid json parseable
class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)

class OrdersManager():
    __orders = []
    __orders_processed = 0
    __last_printed_log = datetime.now()
    # adding a list of threads

    def __init__(self, num_orders=1_000) -> None:
        self.__num_orders = num_orders
        self.__generate_fake_orders(quantity=self.__num_orders)
        self.list_threads = []
    
    def __generate_fake_orders(self, quantity):
        self.__log(f"Generating fake orders")
        self.__orders = [(uuid.uuid4(), x) for x in range(quantity)]
        self.__log(f"{len(self.__orders)} generated...")

    ## Storing the transaction in a json file
    ## we will create chunk of files to save the json data
    
    def save_to_json_db(self, path):
        if self.__num_orders <= 1000:
            y = json.dumps(self.__orders, cls=UUIDEncoder)
            with open(f'{path}.json', 'w') as f:
                for x in y:
                    f.write(y)
        else:
            size_chunks = 1000
            chunks = self.__num_orders / size_chunks
            for i_file in range(int(chunks+1)):
                start_chunk = i_file * size_chunks
                end_chunk = start_chunk + size_chunks
                json_data = json.dumps(self.__orders[start_chunk:end_chunk], cls=UUIDEncoder)
                with open(f'{path}_{i_file}.json', 'w') as f:
                    for line in json_data:
                        f.write(line)
            
            

    def __log(self, message):
        print(f"{datetime.now()} > {message}")

    def __fake_save_on_db(self, order):
        id, number = order

        self.__log(
            message=f"Order [{id}] {number} was successfully prosecuted."
        )

        time.sleep(random.uniform(0, 1))

    def process_orders(self, orders=None):
        ## Cree un argumento nuevo llamado orders para poder separar
        ## las ordenes que processa cada thread
        if orders == None:
            orders = self.__orders
        for order in orders:
            self.__fake_save_on_db(order=order)
            self.__orders_processed += 1

            if datetime.now() > self.__last_printed_log:
                self.__last_printed_log = datetime.now() + timedelta(seconds=5)
                self.__log(
                    message=f"Total orders executed: {self.__orders_processed}/{len(self.__orders)}"
                )
        ## restart orders processed
        __orders_processed = 0

    def process_thread_orders(self, num_threads):
        orders = self.__orders
        num_orders = len(orders)
        per_thread = int(num_orders / num_threads)
        print(f'{num_orders=}')

        ## creation of threads
        # list for thread
        print('num_threads', num_threads)
        for i in range(num_threads):
            start_order = per_thread * i
            end_order = per_thread * (i+1)
            print(f'creating thread for orders from {start_order} to {end_order}')
            current_batch = orders[start_order:end_order]
            thread = Thread(target=self.process_orders, kwargs={'orders':current_batch}) # quitar el self?
            self.list_threads.append(thread)
            print(f'thread  #{i} was succesfully created')
        ## start the threads by looping
        ## this makes sure list_threads is created and that 
        ## our other function otuside of threads can use it
        ## to stop the threads with join
        for thr in self.list_threads:
            thr.start()

# om = OrdersManager(10000)

# om.save_to_json_db('files/perro')