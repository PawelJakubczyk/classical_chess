def type_validator(arg, type_to_val: str, unique: str) -> None:
    """ Check arg(argument) have correct type data(type_to_val). if not return error with unique key(unique) """
    for val_arg in [type_to_val, unique]:
        if not isinstance(val_arg, str):
            raise TypeError(f'{val_arg} must by type str')
    try:
        eval(type_to_val)
    except:
        raise ValueError('function: type_validator - type_to_val must be an name of data'
                         'tape of arg and eval(type_to_val) must return data type')
    if not isinstance(arg, eval(type_to_val)):
        raise TypeError(f'function:{unique} - {arg} must by type {type_to_val}')
