import subprocess
import time


class GPUTemperatureMonitor:
    def __init__(self, interval=5):
        self.interval = interval

    def query_temperature(self):
        try:
            output = subprocess.check_output(
                ['nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader,nounits'],
                stderr=subprocess.STDOUT
            )
            return [int(temp) for temp in output.decode('utf-8').strip().split('\n')]
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to query GPU temperatures: {e.output.decode('utf-8')}")

    def monitor(self):
        try:
            while True:
                temps = self.query_temperature()
                for idx, temp in enumerate(temps):
                    print(f"GPU {idx}: {temp}°C")
                time.sleep(self.interval)
        except KeyboardInterrupt:
            print("Temperature monitoring stopped.")


def main():
    monitor = GPUTemperatureMonitor()
    monitor.monitor()


if __name__ == "__main__":
    main()