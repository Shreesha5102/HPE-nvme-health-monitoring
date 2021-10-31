# HPE-nvme-health-monitoring
This repository contains a Python based-solution to find if a given NVME drive can fail. The proposed solution is as follows:

1. Using a JSON file that stores the threshold values of a given drive.
2. Then, using a linux-based OS, an NVME drive's SMART log parameters are obtained and stored in a CSV file.
3. A Python script is run that routinely monitors the NVME SMART-log and predicts if a specific parameter will increase chances of failure.

The Python scripts makes use of a simple infinite loop and checks the NVME drive every 10 seconds. The temperature parameter has been used as the deciding factor to check the health of the drive. Once the device stops overheating, a printed table summarises the start-time, end-time and the total duration during which the drive has overheated. 

This data can be used to figure out what sort of workload is causing the NVME drive to overheat, among other deductions.

Future work may include using an AI model to automise the process and collecting data from various devices with different uptimes.
