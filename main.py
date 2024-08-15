# Copyright (c) 2024, AmD
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
# Author: Ryan Tischer ryan.tischer@amd.com

import subprocess
import csv

def get_pci_devices():
    # Get the list of PCI devices
    result = subprocess.run(['lspci'], stdout=subprocess.PIPE)
    devices = result.stdout.decode('utf-8').splitlines()
    return [line.split()[0] for line in devices]

def get_device_details(device):
    # Run the lspci command with the -vvv option to get detailed info
    cmd = f'sudo lspci -s {device} -vvv'
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    
    # Extract Speed, Max Payload, and Max Read Request
    speed_info = None
    max_payload = None
    max_read_req = None
    
    for line in output.splitlines():
        if 'LnkSta:' in line:
            speed_info = line.strip()
        if 'DevCap:' in line and 'MaxPayload' in line:
            max_payload = line.strip()
        if 'DevCtl:' in line and 'MaxReadReq' in line:
            max_read_req = line.strip()
    
    return speed_info, max_payload, max_read_req

def main():
    devices = get_pci_devices()
    data = []
    
    for device in devices:
        speed_info, max_payload, max_read_req = get_device_details(device)
        if speed_info or max_payload or max_read_req:
            data.append([device, speed_info, max_payload, max_read_req])

    # Write data to CSV
    with open('pci_device_details.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Device', 'Speed Information', 'Max Payload', 'Max Read Request'])
        writer.writerows(data)
    
    print(f'saved to pci_device_details.csv')

if __name__ == "__main__":
    main()