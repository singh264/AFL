from pathlib import Path
import matplotlib.pyplot as plt

def obtain_the_gnu_coreutils_program(file_name):
    return file_name.split("_")[1]

def obtain_the_map_size_pow2(file_name):
    return int(file_name.split("_")[2])

def initialize_the_data(data, gnu_coreutils_program, map_size_pow2):
    if gnu_coreutils_program not in data.keys():
        data[gnu_coreutils_program] = dict()
    data[gnu_coreutils_program][map_size_pow2] = dict()
    data[gnu_coreutils_program][map_size_pow2]["time"] = []
    data[gnu_coreutils_program][map_size_pow2]["total_paths"] = []

def is_data_in_the_log_file(file_data):
    return len(file_data) > 4

def obtain_the_time(line):
    return float(line.split(" ")[0]) / 60 / 60

def obtain_the_total_paths(line):
    return int(line.split(" ")[1])

def add_the_log_file_to_the_data(data, path):
    file_data = path.read_text().split("\n")
    if is_data_in_the_log_file(file_data):
        start_time = obtain_the_time(file_data[3])
        gnu_coreutils_program_plot_data = data[gnu_coreutils_program][map_size_pow2]
        gnu_coreutils_program_plot_data["time"].append(0)
        gnu_coreutils_program_plot_data["total_paths"].append(obtain_the_total_paths(file_data[3]))
        for index in range(4, len(file_data) - 1):
            time = obtain_the_time(file_data[index]) - start_time
            total_paths = obtain_the_total_paths(file_data[index])
            if ((time - gnu_coreutils_program_plot_data["time"][-1]) > 0):
                gnu_coreutils_program_plot_data["time"].append(time)
                gnu_coreutils_program_plot_data["total_paths"].append(total_paths)

def display_the_plots(gnu_coreutils_program, gnu_coreutils_program_data, index1, index2):
    for map_size_pow2 in sorted(gnu_coreutils_program_data.keys())[index1:index2]:
        gnu_coreutils_program_plot_data = gnu_coreutils_program_data[map_size_pow2]
        time = gnu_coreutils_program_plot_data["time"]
        total_paths = gnu_coreutils_program_plot_data["total_paths"]
        if (len(time) == 1 and len(total_paths) == 1):
            plt.plot(time, total_paths, label="map_size_pow2 = " + str(map_size_pow2), marker="o", markersize=10)
        else:
            plt.plot(time, total_paths, label="map_size_pow2 = " + str(map_size_pow2))
    plt.xlabel("time in hours")
    plt.ylabel("total paths")
    plt.title(gnu_coreutils_program)
    plt.legend()
    plt.show()

def display_the_plots_close_to_the_middle_plot(gnu_coreutils_program, gnu_coreutils_program_data, plots_count):
    map_size_pow2_count = len(gnu_coreutils_program_data.keys())
    middle_plot_index = int(map_size_pow2_count / 2)
    index11 = int(middle_plot_index - plots_count / 2 + 1)
    index12 = middle_plot_index + 1
    index21 = middle_plot_index
    index22 = int(middle_plot_index + plots_count / 2)
    display_the_plots(gnu_coreutils_program, gnu_coreutils_program_data, index1=index11, index2=index12)
    display_the_plots(gnu_coreutils_program, gnu_coreutils_program_data, index1=index21, index2=index22)

def display_the_data(data, plots_count=10):
    for gnu_coreutils_program in data.keys():
        gnu_coreutils_program_data = data[gnu_coreutils_program]
        if len(gnu_coreutils_program_data.keys()) < plots_count:
            map_size_pow2_count = len(gnu_coreutils_program_data.keys())
            display_the_plots(gnu_coreutils_program, gnu_coreutils_program_data, index1=0, index2=map_size_pow2_count)
        else:
            display_the_plots_close_to_the_middle_plot(gnu_coreutils_program, gnu_coreutils_program_data, plots_count)

if __name__ == '__main__':
    data = dict()
    directory_path = Path(input("Provide the directory path: "))
    paths = [path for path in directory_path.rglob("log_*.txt")]
    for path in paths:
        file_name = path.stem
        gnu_coreutils_program = obtain_the_gnu_coreutils_program(file_name)
        map_size_pow2 = obtain_the_map_size_pow2(file_name)
        print("Reading: ", file_name)
        initialize_the_data(data, gnu_coreutils_program, map_size_pow2)
        add_the_log_file_to_the_data(data, path)
        
    display_the_data(data)
