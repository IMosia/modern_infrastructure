import os
import json
import psutil
from datetime import datetime
from math import ceil, sqrt
import dotenv
import re

def load_pattern():
    """
    Load pattern from .env file
    """
    dotenv.load_dotenv()
    pattern_str = os.getenv('REGEXP_NAME_PATTERN')

    return re.compile(pattern_str)


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

def get_input_from_user():
    """
    Get input from user on how we want to proceed
    """
    input_on_mode = input('Do you want to generate or check? (g for generate): ')
    if input_on_mode != 'g':
        mode = 'check'
        return mode, False
    else:
        mode = 'generate'

    input_on_regexp = input('Do you want to use regexp for process name? (y for yes): ')
    if input_on_regexp == 'y':
        use_regexp_flg = True
    else:
        use_regexp_flg = False

    return mode, use_regexp_flg


def run_generation_mode(use_regexp_flg):
    """
    Function to generate JSON with description of processes
    """
    regexp_name_pattern = load_pattern()
    list_processes = []
    counter_process = 0

    for process in psutil.process_iter():
        counter_process += 1
        try:
            process_info = process.as_dict(attrs=['pid', 'name', 'cmdline'])
            process_name = os.path.basename(process_info['name'])

            if use_regexp_flg and not regexp_name_pattern.match(process_name):
                continue

            is_prime = is_number_prime(process_info['pid'])
            dict_for_now = {'Process name': clean_process_name(process_name),
                            'Process ID': process_info['pid'],
                            'Is Prime': is_prime
                            }
            list_processes.append(dict_for_now)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    if use_regexp_flg:
        print(f'Processes that match the pattern: {len(list_processes)} out of {counter_process}', flush=True)

    folder_name = "results_of_generation"
    file_name = make_name_for_json()
    file_path = os.path.join(folder_name, file_name)

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    with open(file_path, 'w') as f:
        json.dump(list_processes, f,  indent=4)

    print('Your JSON is ready!', flush=True)
    
def check_processes_from_json(processes):
    """
    To check if processes are prime or not and compare with the list of processes
    """
    error_count = 0
    error_messages = []
    try:
        for process in processes:
            pid = process["Process ID"]
            if process["Is Prime"] != is_number_prime(process["Process ID"]):
                error_count += 1
                if process["Is Prime"]:
                    first_word, second_word = 'составное', 'простое'
                else:
                    first_word, second_word = 'простое', 'составное'
        
                error_messages.append(
                    f"________Для {process['Process name']} процесса найдена ошибка."
                    f"\n________Число(PID) {pid} на самом деле {first_word}, а в файле написано {second_word}."
                )
        
        if error_count > 0:
            error_messages.append(f"____В файле найдены ошибки: {error_count} штук_и")
            for error in error_messages:
                    print(error, flush=True)
        else:
            print("____Ошибок не найдено", flush=True)
    except:
        print("____Ошибка при чтении файла")
        
    return
    
def run_check_mode():
    """
    Function to check if process is prime
    """
    for file in os.listdir('files_to_check'):
        with open(f'files_to_check/{file}', 'r') as f:
            processes = json.load(f)
            print(f'File {file} analysis:', flush=True)
            check_processes_from_json(processes)
            

def main():
    mode, use_regexp_flg = get_input_from_user()

    if mode == 'check':
        run_check_mode()
    else:
        run_generation_mode(use_regexp_flg)
    

if __name__ == '__main__':
    main()
