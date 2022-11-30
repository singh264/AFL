from pathlib import Path
import matplotlib.pyplot as plt

def obtain_the_gnu_coreutils_program(file_name):
    return file_name.split("_")[3]

def obtain_the_map_size_pow2(file_name):
    return int(file_name.split("_")[4])

def is_the_fuzzer_in_the_llvm_mode(file_name):
    return "llvm_mode" in file_name

def obtain_the_key_of_the_gnu_coreutils_program_plot_data(map_size_pow2, is_llvm_mode, path):
    key = str(map_size_pow2) + "_llvm_mode" if is_llvm_mode else str(map_size_pow2)
    key += str(path)
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
        for key in gnu_coreutils_program_data.keys():
            if statistic_name in key:
                gnu_coreutils_program_plot_data = gnu_coreutils_program_data[key]
                time = gnu_coreutils_program_plot_data["time"]
                statistic = gnu_coreutils_program_plot_data[statistic_name]
                label = "AFL fuzzer with the LLVM mode" if "llvm_mode" in str(key) else "AFL fuzzer"
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
