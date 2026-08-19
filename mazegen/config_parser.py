class ConfigError(Exception):
    pass


def read_config(config_file: str) -> dict[str, str | tuple[int, int]] | None:
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
    config_dict: dict[str, str | tuple[int, int]] = {}
    try:
        with open(config_file) as configurations:
            lines = configurations.readlines()
            for i in lines:
                line = i.strip()
                if not line or line.startswith("#"):
                    continue
                key, value = line.split("=", 1)
                config_dict[key.strip()] = value.strip()
        if not isinstance(config_dict["ENTRY"], str) or not isinstance(
            config_dict["EXIT"], str
        ):
            raise ConfigError("Invalid ENTRY or EXIT")
        config_dict["ENTRY"] = parse_coordinate(config_dict["ENTRY"])
        config_dict["EXIT"] = parse_coordinate(config_dict["EXIT"])
        if not check_dim(config_dict):
            raise ConfigError("Invalid dimensions")
        return config_dict

    except Exception as e:
        print(e)
        return None


def parse_coordinate(value: str) -> tuple[int, int]:
    """
    converts a coordinate string into tuple of integers

    """

    row, col = value.split(",", 1)

    return int(row.strip()), int(col.strip())


def check_dim(config: dict[str, str | tuple[int, int]]) -> bool:
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
