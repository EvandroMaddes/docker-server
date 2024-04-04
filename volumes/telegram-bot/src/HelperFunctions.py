import subprocess

CELSIUS_DEGREE = " °C"


def get_server_temperature_string() -> str:
    current_temp = get_server_temperature_float()
    return str(current_temp) + CELSIUS_DEGREE


def get_server_temperature_float() -> float:
    current_temp_str = subprocess.check_output("cat /sys/class/thermal/thermal_zone0/temp", shell=True)
    current_temp_float = float(current_temp_str)
    return current_temp_float / 1000


def commands_tuple_to_md(data_tuple):
    list_items = [f" *** /{command}***: {command_description}\n" for command, command_description in data_tuple]
    return "".join(list_items)
