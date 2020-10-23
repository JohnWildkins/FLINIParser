import re
from collections import defaultdict

def read_ini(ini_path, v_name='nickname', filter_str=None):
    with open(ini_path, 'r') as ini:
        ini_lines = list(filter(None, [ln.strip() for ln in re.split(r'^(\[[A-Za-z]*\])', ini.read(), flags=re.M)]))
        ds = next(i for i, string in enumerate(ini_lines) if '[' in string)
        i_comments = ini_lines[:ds]
        i_keys = ini_lines[ds::2]
        i_values = ini_lines[ds+1::2]
        ini_dict = dict()

        for i in range(len(i_keys)):
            if filter_str and filter_str.lower() not in i_keys[i].lower():
                continue

            value_name = i_keys[i]
            i_tuples = list()

            try:
                i_props = list(filter(None, [ip for ip in i_values[i].split('\n') if ';' not in ip]))
            except IndexError:
                continue

            if not i_props:
                continue

            for ip in i_props:
                i_tuples.append(tuple([i_tup.strip() for i_tup in ip.split('=')]))

            if not i_tuples:
                continue

            partial_dict = defaultdict(list)
            try:
                for k, v in i_tuples:
                    if v_name in k:
                        value_name = v
                    partial_dict[k].append(v)
            except ValueError:
                print('ERR: Invalid INI entry in file {0}'.format(ini_path))

            ini_dict[value_name] = partial_dict

    return ini_dict
