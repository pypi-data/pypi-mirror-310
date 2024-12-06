# my_library/utils.py
def validate_input(data):
    if data is None:
        raise ValueError("Data cannot be None")
    return True
