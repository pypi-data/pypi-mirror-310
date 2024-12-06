import subprocess
import time
from termcolor import colored


class GPUTemperatureMonitor:
    def __init__(self, interval=5):
        self.interval = interval

    # Query GPU temperatures using nvidia-smi.
    def query_temperature(self):
        try:
            output = subprocess.check_output(
                ['nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader,nounits'],
                stderr=subprocess.STDOUT
            )
            return [int(temp) for temp in output.decode('utf-8').strip().split('\n')]
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to query GPU temperatures: {e.output.decode('utf-8')}")

    # Query GPU names using nvidia-smi.
    def query_gpu_names(self):
        try:
            output = subprocess.check_output(
                ['nvidia-smi', '--query-gpu=name', '--format=csv,noheader'],
                stderr=subprocess.STDOUT
            )
            return output.decode('utf-8').strip().split('\n')
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to query GPU names: {e.output.decode('utf-8')}")

    # Format GPU name and temperature with colors based on thresholds.
    def format_output(self, gpu_index, gpu_name, gpu_temp):
        if gpu_temp < 50:
            temp_str = colored(f"{gpu_temp}°C", "green")
        elif gpu_temp < 75:
            temp_str = colored(f"{gpu_temp}°C", "yellow")
        else:
            temp_str = colored(f"{gpu_temp}°C", "red")

        return f"GPU {gpu_index}: {gpu_name} - {temp_str}"

    # Continuously monitor GPU temperatures.
    def monitor(self):
        try:
            gpu_names = self.query_gpu_names()
            while True:
                gpu_temps = self.query_temperature()
                for idx, (gpu_name, gpu_temp) in enumerate(zip(gpu_names, gpu_temps)):
                    print(self.format_output(idx, gpu_name, gpu_temp))
                time.sleep(self.interval)
        except KeyboardInterrupt:
            print("\nTemperature monitoring stopped.")


def main():
    monitor = GPUTemperatureMonitor()
    monitor.monitor()


if __name__ == "__main__":
    main()