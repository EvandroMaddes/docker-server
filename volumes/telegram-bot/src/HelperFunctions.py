import re
import subprocess


def get_server_temperature_string() -> str:
    return subprocess.check_output("vcgencmd measure_temp | awk -F = '{print $2}'", shell=True).decode("utf-8").strip()


def get_server_temperature_float() -> float:
    return float(re.findall(r"[-+]?\d*\.*\d+", get_server_temperature_string())[0])


def commands_tuple_to_md(data_tuple):
    list_items = [f" *** /{command}***: {command_description}\n" for command, command_description in data_tuple]
    return "".join(list_items)
