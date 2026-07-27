import sys


class ConfigError(Exception):
    pass


def read_config(config_file: str) -> dict[str, str]:
    config_dict: dict[str, str] = {}
    try:
        with open(config_file) as configurations:
            lines = configurations.readlines()
            for i in lines:
                line = i.strip()
                if not line or line.startswith("#"):
                    continue
                key, value = line.split("=", 1)
                config_dict[key.strip()] = value.strip()
            print(config_dict)
        if not check_dim(config_dict):
            raise ConfigError("Invalid dimensions")
        return config_dict

    except Exception as e:
        raise ConfigError(e)


def check_dim(config: dict[str,str]) -> bool:
    xs, ys = config["ENTRY"].split(',', 1)
    xe, ye = config["EXIT"].split(',', 1)
    xs = int(xs)
    ys = int(ys)
    xe = int(xe)
    ye = int(ye)
    if not (xs >= 0 and xs < int(config["WIDTH"])):
        return False
    if not (xe >= 0 and xe < int(config["WIDTH"])):
        return False
    if not (ys >= 0 and ys < int(config["HEIGHT"])):
        return False
    if not (ye >= 0 and ye < int(config["HEIGHT"])):
        return False
    if config["ENTRY"] == config["EXIT"]:
        return False

    return True
