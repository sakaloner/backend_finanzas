import os
import json


def get_lines(offset, limit, filename='transactions'):
    chunk_size = 1000
    
    all_files = os.listdir('db_files/')

    all_files.sort(key=lambda i : i[len(filename)+2])
    start_file_i = int(offset / chunk_size)
    end_file_i = int(limit / 1000)

    ## get filenames where query spans
    query_files = []
    for f in all_files:
        prefix_len = len(filename)
        if int(f[prefix_len+1:-5]) in range(start_file_i, end_file_i+1):
            query_files.append(f)
    ## order files
    query_files.sort(key=lambda x: x[len(filename)+1:-5])
        

    ## get lines 
    final_list = []
    for file_i, file in enumerate(query_files):
        print(f'{file_i=}')
        with open(f'db_files/{file}', 'r') as f:
            for i, line in enumerate(json.load(f)):
                range_query = limit - offset
                ### check if its the first file
                if file_i == 0:
                    start_line = (offset % chunk_size)

                    ## if end line is in the same file
                    if (range_query + start_line) < chunk_size:
                        end_line = (limit % chunk_size)
                    ## if the end line is in another file
                    else:
                        end_line = chunk_size
                ### check if the loop is in its last file
                elif file_i == (len(query_files)-1):
                    start_line = 0
                    end_line = (limit % chunk_size)
                ### its neither the end or start of the file_index loop
                ### so get all the lines
                else:
                    start_line = 0
                    end_line = 1000
                #### start appending data
                if i in range(start_line, end_line+1):
                    #print(f'appended {i=} {line=}')
                    final_list.append(line)
    return final_list

def get_transaction_by_id(trans_id:int, filename='transactions'):
    chunk_size = 1000
    all_files = os.listdir('db_files/')
    all_files.sort(key=lambda i : i[len(filename)+2])
    file_i = int(trans_id / chunk_size)

    ## get filename where query is
    for fi in all_files:
        prefix_len = len(filename)
        if int(fi[prefix_len+1:-5]) == file_i:
            query_file = fi

    with open(f'db_files/{query_file}', 'r') as f:
        for i, line in enumerate(json.load(f)):
            if i == int(trans_id % 1000):
                return line
        ## couldnt find in file the id
        return f'couldnt find transaction with {trans_id} as id'
    
def get_transaction_page(page_num:int, filename='transactions'):
    chunk_size = 1000
    all_files = os.listdir('db_files/')
    all_files.sort(key=lambda i : i[len(filename)+2])
    file_i = page_num

    ## get filename where query is
    for fi in all_files:
        prefix_len = len(filename)
        if int(fi[prefix_len+1:-5]) == file_i:
            query_file = fi

    with open(f'db_files/{query_file}') as f:
        y = json.load(f)
        print(y)
        return y 

if __name__ == '__main__':
    # lines = get_lines(0, 1000)
    # print(lines)
    n = get_transaction_page(1)
    print(n)