import os
import json
import psutil
from datetime import datetime
from math import ceil, sqrt

def is_number_prime(number):
    """
    Check if number is prime
    """
    if number < 2:
        return False
    for i in range(2, ceil(sqrt(number)) + 1):  # Include upper bound in range
        if number % i == 0:
            return False
    return True

def make_name_for_json():
    """
    Make name for json file
    """
    time_str = f'{datetime.now()}'.replace(' ', '_').replace('-', '_').replace(':', '_').replace('.', '_')
    return f"processes_{time_str}.json"

def clean_process_name(name):
    """
    Clean up process name
    """
    cleaned_name = ''.join(char for char in name if char.isprintable())
    return os.path.basename(cleaned_name.split()[0])

def main():
    list_processes = []
    for process in psutil.process_iter():
        try:
            process_info = process.as_dict(attrs=['pid', 'name', 'cmdline'])
            process_name = os.path.basename(process_info['name'])
            is_prime = is_number_prime(process_info['pid'])
            dict_for_now = {'Process name': clean_process_name(process_name),
                            'Process ID': process_info['pid'],
                            'Is Prime': is_prime
                            }
            list_processes.append(dict_for_now)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    with open(make_name_for_json(), 'w') as f:
        json.dump(list_processes, f,  indent=4)

    print('Your JSON is ready!', flush=True)

if __name__ == '__main__':
    main()
