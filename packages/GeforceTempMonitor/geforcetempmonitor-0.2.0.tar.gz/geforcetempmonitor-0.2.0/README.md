
# GeforceTempMonitor

**GeforceTempMonitor** is a Python-based library for monitoring NVIDIA GPU temperatures, specifically for GeForce cards. Since NVIDIA's NVML library only provides support for Tesla and Quadro GPUs, and does not natively support GeForce cards, this library abstracts the functionality of `nvidia-smi` to provide a straightforward way to query temperature data programmatically.

To address this limitation, **GeforceTempMonitor** parses and processes data from `nvidia-smi`, allowing users to monitor GeForce GPU temperatures seamlessly.

With **GeforceTempMonitor**, you can track the temperature of your GPUs in real-time or as part of a monitoring script, making it easier to manage and optimize your system's performance.

---

## **Disclaimer**

This project is not affiliated with NVIDIA in any way.

**Adjusting GPU-related settings or running custom scripts can have unintended consequences, including hardware overheating or system instability.** Use this library at your own risk, and make sure you test it thoroughly in your environment before relying on it for critical applications.

---

## **Installation**

You can install the package using `pip`:

```bash
pip install geforce-temp-monitor
```

---

## **Usage**

### **Command-Line Interface**
To monitor GPU temperatures directly, run the following command:

```bash
geforce_temp_monitor
```

This will output the temperature of all available GPUs to the console in real-time.

#### **Custom Interval**
You can specify the interval (in seconds) for monitoring:

```bash
geforce_temp_monitor --interval <seconds>
```

Replace `<seconds>` with your desired interval.

---

### **Python Library**
The library can also be used programmatically within your own Python scripts:

```python
from geforce_temp_monitor import get_gpu_temperatures

# Get a dictionary of GPU temperatures
temperatures = get_gpu_temperatures()

# Print the temperature of each GPU
for gpu, temp in temperatures.items():
    print(f"GPU {gpu}: {temp}°C")
```

---

## **Setting Up on Linux**

To ensure `nvidia-smi` is available in your environment, follow these steps:

### **Install NVIDIA Drivers**
1. Install the latest NVIDIA drivers for your GeForce GPU from [NVIDIA's driver page](https://www.nvidia.com/Download/index.aspx).
2. Verify that `nvidia-smi` is working by running:

   ```bash
   nvidia-smi
   ```

   You should see a summary of your GPU(s) along with metrics like temperature and utilization.

---

## **Running as a Systemd Service**

To enable continuous monitoring, you can set up **GeforceTempMonitor** as a systemd daemon service.

### **Steps**
1. Create a file called `geforce_temp_monitor.service` with the following content:

   ```ini
   [Unit]
   Description=GPU Temperature Monitor
   After=multi-user.target

   [Service]
   Type=simple
   ExecStart=/usr/bin/python3 -m geforce_temp_monitor --interval 10
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

2. Copy the service file to the systemd folder:

   ```bash
   sudo cp geforce_temp_monitor.service /etc/systemd/system/
   ```

3. Reload the systemd configuration:

   ```bash
   sudo systemctl daemon-reload
   ```

4. Enable the service to start on boot:

   ```bash
   sudo systemctl enable geforce_temp_monitor
   ```

5. Start the service:

   ```bash
   sudo systemctl start geforce_temp_monitor
   ```

6. Check the service status:

   ```bash
   sudo systemctl status geforce_temp_monitor
   ```

---

## **Contributing**

Contributions to **GeforceTempMonitor** are welcome! To contribute:

1. Fork the repository on GitHub.
2. Make your changes and submit a pull request.
3. Open an issue to discuss any ideas.

---

## **License**

This project is licensed under the MIT License. See the LICENSE file for details.
