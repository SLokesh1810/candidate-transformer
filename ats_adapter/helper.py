def get_value(data, possible_keys):

    for key in possible_keys:

        if key in data:
            return data[key]

    return None