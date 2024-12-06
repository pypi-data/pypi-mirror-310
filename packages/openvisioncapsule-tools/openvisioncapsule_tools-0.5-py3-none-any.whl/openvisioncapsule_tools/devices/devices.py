#
# Copyright (c) 2024 AOTU, Inc.  All rights reserved. Contains Proprietary Information. RESTRICTED COMPUTER SOFTWARE.  LIMITED RIGHTS DATA.
#
from openvisioncapsule_tools.command_utils import command
from vcap.device_mapping import DeviceMapper, get_all_devices

@command("devices")
def devices_main():
    all_devices = get_all_devices()

    all_gpus = DeviceMapper.map_to_all_gpus().filter_func(all_devices)
    single_gpu = DeviceMapper.map_to_single_cpu().filter_func(all_devices)
    openvino_devices = DeviceMapper.map_to_openvino_devices().filter_func(all_devices)

    print(f'All devices     : {all_devices}')
    print(f'All GPUs        : {all_gpus}')
    print(f'Single GPU      : {single_gpu}')
    print(f'Openvino devices: {openvino_devices}')

if __name__ == "__main__":
    by_name["devices"]()

