def clean_config_paths(path):
    # replace all keys at start with substitution
    for key, value in path.items():
        seen_keys = set(key)
        toks = value.split('/')
        while toks[0][0:2] == '__' and toks[0][-2:] == '__':
            new_key = toks[0][2:-2].lower()
            if new_key in seen_keys:
                raise Exception("Circular reference found when processing "
                                "{}, found {} twice".format(key, new_key))
            seen_keys.add(new_key)
            toks[0] = path[new_key]
            toks = '/'.join(toks).split('/')
        path[key] = '/'.join(toks)

    # iterate again checking for inner variables
    for key, value in path.items():
        toks = value.split('/')
        for i in range(len(toks)):
            if toks[i][0:2] == '__' and toks[i][-2:] == '__':
                toks[i] = path[toks[i][2:-2].lower()]
        path[key] = '/'.join(toks)

    return path


def join_config_paths(base_path, new_paths):
    # add new paths to base. Values already in base are ignored.
    # can't selectively load those paths so all old values are also included
    # after merge, clean new dict paths
    for key, value in new_paths.items():
        if key not in base_path:
            base_path[key] = value

    return clean_config_paths(base_path)
