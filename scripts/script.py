from pathlib import Path
import matplotlib.pyplot as plt

def obtain_the_gnu_coreutils_program(file_name):
    return file_name.split("_")[3]

def obtain_the_map_size_pow2(file_name):
    if "afl-llvm-pass_" in file_name:
        return int(file_name.split("_")[2])
    return int(file_name.split("_")[4])

def is_the_fuzzer_in_the_llvm_mode(file_name):
    return "llvm_mode" in file_name

def obtain_the_key_of_the_gnu_coreutils_program_plot_data(map_size_pow2, is_llvm_mode, path):
    key = str(map_size_pow2) + "_llvm_mode" if is_llvm_mode else str(map_size_pow2)
    key += "_" + str(path)
    return key

def initialize_the_data(data, gnu_coreutils_program, map_size_pow2, is_llvm_mode, path, statistic_name):
    if gnu_coreutils_program not in data.keys():
        data[gnu_coreutils_program] = dict()

    key = obtain_the_key_of_the_gnu_coreutils_program_plot_data(map_size_pow2, is_llvm_mode, path)
    data[gnu_coreutils_program][key] = dict()
    data[gnu_coreutils_program][key]["time"] = []
    data[gnu_coreutils_program][key][statistic_name] = []

def is_data_in_the_log_file(file_data):
    return len(file_data) > 4

def obtain_the_time(line):
    return float(line.split(" ")[0]) / 60 / 60

def obtain_the_statistic(line):
    return int(line.split(" ")[1])

def is_the_afl_llvm_pass_data_correct(data):
    is_the_afl_llvm_pass_data_correct = True
    entities_in_the_data = data.split(", ")
    if (len(entities_in_the_data) != 3):
        is_the_afl_llvm_pass_data_correct = False
    else:
        for entity in entities_in_the_data:
            if not entity.isnumeric():
                is_the_afl_llvm_pass_data_correct = False;
            break
    return is_the_afl_llvm_pass_data_correct

def obtain_the_map_size_pow2_from_the_key(key):
    return key.split("_")[0]

def add_the_log_file_to_the_data(data, map_size_pow2, is_llvm_mode, path, statistic_name):
    file_data = path.read_text().split("\n")
    if is_data_in_the_log_file(file_data):
        start_time = obtain_the_time(file_data[3])
        key = obtain_the_key_of_the_gnu_coreutils_program_plot_data(map_size_pow2, is_llvm_mode, path)
        gnu_coreutils_program_plot_data = data[gnu_coreutils_program][key]
        gnu_coreutils_program_plot_data["time"].append(0)
        gnu_coreutils_program_plot_data[statistic_name].append(obtain_the_statistic(file_data[3]))
        for index in range(4, len(file_data) - 1):
            time = obtain_the_time(file_data[index]) - start_time
            statistic = obtain_the_statistic(file_data[index])
            if ((time - gnu_coreutils_program_plot_data["time"][-1]) > 0):
                gnu_coreutils_program_plot_data["time"].append(time)
                gnu_coreutils_program_plot_data[statistic_name].append(statistic)

def display_the_data(data, statistic_name):
    for gnu_coreutils_program in data.keys():
        gnu_coreutils_program_data = data[gnu_coreutils_program]
        for key in sorted(gnu_coreutils_program_data.keys()):
            if statistic_name in key:
                gnu_coreutils_program_plot_data = gnu_coreutils_program_data[key]
                time = gnu_coreutils_program_plot_data["time"]
                statistic = gnu_coreutils_program_plot_data[statistic_name]
                map_size_pow2 = obtain_the_map_size_pow2_from_the_key(key)
                label = "AFL LLVM, map_size_pow2 = " + str(map_size_pow2) if "llvm_mode" in str(key) else "AFL, map_size_pow2 = " + str(map_size_pow2) 
                if (len(time) == 1 and len(statistic) == 1):
                    plt.plot(time, statistic, label=label, marker="o", markersize=10)
                else:
                    plt.plot(time, statistic, label=label)
        plt.xlabel("time in hours")
        plt.ylabel(statistic_name)
        plt.title(gnu_coreutils_program)
        plt.legend()
        plt.show()

def display_the_log_file_with_the_time_in_hours(path):
    file_data = path.read_text().split("\n")
    if is_data_in_the_log_file(file_data):
        start_time = obtain_the_time(file_data[3])
        for index in range(4, len(file_data) - 1):
            time = obtain_the_time(file_data[index]) - start_time
            statistic = obtain_the_statistic(file_data[index])
            print(str(time) + " " + str(statistic))

def obtain_the_information_about_the_bitmap(directory_path):
    paths = [path for path in directory_path.rglob("afl-llvm-pass_*.txt")]
    for path in paths:
        file_name = path.stem
        print("Reading: ", file_name)
        file_data = path.read_text().split("\n")
        bitmap_data = dict()
        number_of_hash_collisions = 0
        number_of_hashes = 0
        for data in file_data:
            if is_the_afl_llvm_pass_data_correct(data):
                entities_in_the_data = data.split(", ")
                current_location = entities_in_the_data[0]
                previous_location = entities_in_the_data[1]
                hash = entities_in_the_data[2]
                if hash not in bitmap_data.keys():
                    bitmap_data[hash] = list()
                else:
                    number_of_hash_collisions += 1
                bitmap_data[hash].append(current_location + " " + previous_location)
                number_of_hashes += 1
        print("Hash collisions = number_of_hash_collisions / number_of_hashes = " + str(number_of_hash_collisions / number_of_hashes))

def obtain_the_good_size_of_the_bitmap(data, statistic_name):
    good_map_size_pow2 = 0
    for gnu_coreutils_program in data.keys():
        good_statistic = 0
        gnu_coreutils_program_data = data[gnu_coreutils_program]
        for key in sorted(gnu_coreutils_program_data.keys()):
            if statistic_name in key:
                gnu_coreutils_program_plot_data = gnu_coreutils_program_data[key]
                statistic = gnu_coreutils_program_plot_data[statistic_name]
                if len(statistic) > 0:
                    last_statistic = statistic[-1]
                    map_size_pow2 = obtain_the_map_size_pow2_from_the_key(key)
                    if last_statistic > good_statistic:
                        good_map_size_pow2 = map_size_pow2
                        good_statistic = last_statistic
        print(gnu_coreutils_program + ", " + statistic_name)
        print("Good map_size_pow2 = " + good_map_size_pow2)

if __name__ == '__main__':
    data = dict()
    directory_path = Path(input("Provide the directory path: "))
    for statistic_name in ["total_crashes", "total_paths", "unique_crashes"]:
        paths = [path for path in directory_path.rglob("afl-fuzz_" + statistic_name + "_*.txt")]
        for path in paths:
    	    file_name = path.stem
    	    gnu_coreutils_program = obtain_the_gnu_coreutils_program(file_name)
    	    map_size_pow2 = obtain_the_map_size_pow2(file_name)
    	    is_llvm_mode = is_the_fuzzer_in_the_llvm_mode(file_name)
    	    print("Reading: ", file_name)
    	    initialize_the_data(data, gnu_coreutils_program, map_size_pow2, is_llvm_mode, path, statistic_name)
    	    add_the_log_file_to_the_data(data, map_size_pow2, is_llvm_mode, path, statistic_name)
    	    
        display_the_data(data, statistic_name)
        obtain_the_good_size_of_the_bitmap(data, statistic_name)