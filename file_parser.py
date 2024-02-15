def config_parser(txt_file):
    config_dict = {}
    for line in txt_file:
        line = line.rstrip('\n')
        key, value = line.split('=')
        config_dict[key] = value
    
    return config_dict