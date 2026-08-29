import os


class ConfigError(Exception):
    pass


def read_config(config_file: str) -> dict[str,
                                          str | tuple[int, int]
                                          | None | bool] | None:
    """
    read and validate the maze config file
    args:
            config_file: path to the config file
    returns:
            a dic containing the coonfig values
    raises:
         ConfigError: if the configuration file is invalid or cannot
         be read
    """
    config_dict: dict[str, str | tuple[int, int] | None | bool] = {}
    try:
        with open(config_file) as configurations:
            lines = configurations.readlines()
            for i in lines:
                line = i.strip()
                if not line or line.startswith("#"):
                    continue
                key, value = line.split("=", 1)
                key = key.strip().upper()
                if key == "EXIT" or key == "ENTRY":
                    if value == "":
                        raise ConfigError("Missing Coordinates")
                if key == "PERFECT":
                    value = value.strip().upper()
                    if value == "":
                        raise ConfigError("Missing PERFECT Value")
                    elif value == "TRUE":
                        config_dict["PERFECT"] = True
                    elif value == "FALSE":
                        config_dict["PERFECT"] = False
                elif key.strip() == "SEED":
                    value = value.strip().upper()
                    if value.strip() == "NONE":
                        config_dict["SEED"] = None
                    else:
                        config_dict["SEED"] = value.strip()
                elif key == "OUTPUT_FILE":
                    if value == "":
                        raise ConfigError("Missing output file")
                    else:
                        config_dict[key.strip()] = value.strip()
                else:
                    config_dict[key.strip()] = value.strip()
        if "PERFECT" not in config_dict.keys():
            config_dict["PERFECT"] = False
        if "SEED" not in config_dict.keys():
            config_dict["SEED"] = None
        if not isinstance(config_dict["ENTRY"], str) or not isinstance(
            config_dict["EXIT"], str
        ):
            raise ConfigError("Invalid ENTRY or EXIT")
        if not isinstance(config_dict["SEED"], str | None):
            raise ConfigError("Invalid SEED")
        if not isinstance(config_dict["PERFECT"], bool):
            raise ConfigError("Invalid PERFECT value")
        config_dict["ENTRY"] = parse_coordinate(config_dict["ENTRY"])
        config_dict["EXIT"] = parse_coordinate(config_dict["EXIT"])
        if not check_dim(config_dict):
            raise ConfigError("Invalid dimensions or coordinates")
        size = os.get_terminal_size()
        if (
            (not isinstance(config_dict["HEIGHT"], str)) or
            (not isinstance(config_dict["WIDTH"], str))
        ):
            raise ConfigError("Invalid dim")
        if size.columns <= int(config_dict["WIDTH"]):
            raise ConfigError("Width too large")
        if size.lines <= int(config_dict["HEIGHT"]):
            raise ConfigError("Height too large")
        if "PERFECT" not in config_dict.keys():
            config_dict["PERFECT"] = False
        return config_dict

    except FileNotFoundError:
        raise ConfigError(
            f"Configuration file '{config_file}' was not found."
        )
    except PermissionError:
        raise ConfigError(
            "Cannot read configuration file"
            f"'{config_file}': permission denied."
        )
    except ValueError as e:
        raise ConfigError(f"Invalid configuration value: {e}")
    except KeyError as e:
        raise ConfigError(f"Missing configuration key: {e}")
    except NameError:
        raise ConfigError("Missing coordinates")


def parse_coordinate(value: str) -> tuple[int, int]:
    """
    converts a coordinate string into tuple of integers

    """
    row, col = value.split(",", 1)
    return int(row.strip()), int(col.strip())


def check_dim(config: dict[str, str | tuple[int, int] | None | bool]) -> bool:
    """
    check whether the maze coordinates are within its dimensions
    also verifies that the entry and exit coordinates are different
    """
    if (
            (not isinstance(config["ENTRY"], tuple)) or
            (not isinstance(config["EXIT"], tuple))
            ):
        return False
    if (
            (not isinstance(config["HEIGHT"], str)) or
            (not isinstance(config["WIDTH"], str))
            ):
        return False
    xs, ys = config["ENTRY"]
    xe, ye = config["EXIT"]
    if not (xs >= 0 and xs < int(config["HEIGHT"])):
        return False
    if not (xe >= 0 and xe < int(config["HEIGHT"])):
        return False
    if not (ys >= 0 and ys < int(config["WIDTH"])):
        return False
    if not (ye >= 0 and ye < int(config["WIDTH"])):
        return False
    if config["ENTRY"] == config["EXIT"]:
        return False

    return True
