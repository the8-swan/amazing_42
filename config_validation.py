class ErrorInConfigFile(Exception):
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return f"Error in your configuration file: {self.message}"


def data_validation(data_dict: dict) -> None:
    # PERFECT validation
    if data_dict["PERFECT"].upper() not in ("TRUE", "FALSE"):
        raise ErrorInConfigFile("'PERFECT' value should be TRUE or FALSE")

    if data_dict["PERFECT"].upper() == "TRUE":
        data_dict["PERFECT"] = True
    elif data_dict["PERFECT"].upper() == "FALSE":
        data_dict["PERFECT"] = False

    # WIDTH AND HEIGHT validation
    if (data_dict["WIDTH"].isdigit()) is False:
        raise ErrorInConfigFile(
            f"Invalid WIDTH: {data_dict['WIDTH']}."
            " WIDTH must be a number greater than 0."
        )
    if (data_dict["HEIGHT"].isdigit()) is False:
        raise ErrorInConfigFile(
            f"Invalid HEIGHT: {data_dict['HEIGHT']}."
            " HEIGHT must be a number greater than 0."
        )

    # WIDTH AND HEIGHT Greater than 0
    data_dict["WIDTH"] = int(data_dict["WIDTH"])
    data_dict["HEIGHT"] = int(data_dict["HEIGHT"])
    if data_dict["WIDTH"] == 0:
        raise ErrorInConfigFile(
            f"Invalid WIDTH: {data_dict['WIDTH']}."
            f" WIDTH must be greater than 0."
        )
    if data_dict["HEIGHT"] == 0:
        raise ErrorInConfigFile(
            f"Invalid HEIGHT: {data_dict['HEIGHT']}."
            " HEIGHT must be greater than 0."
        )

    # ENTRY and EXIT validation
    if ("," in data_dict["ENTRY"] and "," in data_dict["EXIT"]) is False:
        raise ErrorInConfigFile("ENTRY and EXIT  should be with this format: "
                                "'X,Y'")
    data_dict["ENTRY"] = data_dict["ENTRY"].split(",")
    data_dict["EXIT"] = data_dict["EXIT"].split(",")

    if (data_dict["ENTRY"][0].isdigit() and
            data_dict["ENTRY"][1].isdigit()) is False:
        raise ErrorInConfigFile(
            f"Invalid ENTRY coordinates: {data_dict['ENTRY']}."
            " Coordinates must be valid numbers."
        )
    if (data_dict["EXIT"][0].isdigit() and
            data_dict["EXIT"][1].isdigit()) is False:
        raise ErrorInConfigFile(
            f"Invalid EXIT coordinates: {data_dict['EXIT']}."
            " Coordinates must be valid numbers."
        )
    data_dict["ENTRY"] = tuple(map(int, data_dict["ENTRY"]))
    data_dict["EXIT"] = tuple(map(int, data_dict["EXIT"]))
    if data_dict["ENTRY"].__len__() != 2:
        raise ErrorInConfigFile("ENTRY coordinates should be at this format: "
                                "'X,Y'")
    if data_dict["EXIT"].__len__() != 2:
        raise ErrorInConfigFile("EXIT coordinates should be at this format:"
                                " 'X,Y'")
    if (
        data_dict["ENTRY"][0] >= data_dict["WIDTH"]
        or data_dict["ENTRY"][1] >= data_dict["HEIGHT"]
    ):
        raise ErrorInConfigFile(
            "ENTRY X should be strictly greather than 0"
            f' and lower than {data_dict["WIDTH"]}.\n'
            "Y should be strictly greather than 0 and "
            f'lower than {data_dict["HEIGHT"]}'
        )
    if (
        data_dict["EXIT"][0] >= data_dict["WIDTH"]
        or data_dict["EXIT"][1] >= data_dict["HEIGHT"]
    ):
        raise ErrorInConfigFile(
            "EXIT X should be strictly greather than 0"
            f' and lower than {data_dict["WIDTH"]}.\n'
            "Y should be strictly greather than 0 and "
            f'lower than {data_dict["HEIGHT"]}'
        )
    if (
        data_dict["ENTRY"][0] == data_dict["EXIT"][0]
        and data_dict["ENTRY"][1] == data_dict["EXIT"][1]
    ):
        raise ErrorInConfigFile("EXIT and ENTRY coordinates should be "
                                "different")

    if data_dict["OUTPUT_FILE"].strip() == "":
        raise ErrorInConfigFile("OUTPUT_FILE is empty !!")


def validation(text: str) -> dict:
    mandatory = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
    valid_keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT",
                  "SEED"]
    keys = 0
    lines = text.strip().split("\n")
    line_wcommants = [line for line in lines if line[0] != "#"]
    lines_w = [line.strip().split("=") for line in line_wcommants]
    for line in lines_w:
        if line.__len__() != 2:
            raise ErrorInConfigFile(
                f"Invalid line: '{line}.'"
                " Each line must be a 'KEY=VALUE' pair."
            )
        if line[0].strip().upper() not in valid_keys:
            raise ErrorInConfigFile(
                f"Invalid key: '{line[0]}'." " Please enter a valid key."
            )
        if line[0].strip().upper() in mandatory:
            keys += 1
    if keys != mandatory.__len__():
        raise ErrorInConfigFile(
            "A mandatory key is missing, "
            f"verify your file again. {mandatory}"
        )
    data_dict = {key.strip(): value.strip() for key, value in lines_w}
    data_validation(data_dict)
    return data_dict
