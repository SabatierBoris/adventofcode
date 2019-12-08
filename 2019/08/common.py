def get_layers(data, wide, tall):
    for i in range(0, len(data), wide * tall):
        yield data[i : i + wide * tall]


def parse_infos(layer):
    infos = {}
    for data in layer:
        if data not in infos:
            infos[data] = 0
        infos[data] += 1
    return infos


def merge_layers(layers):
    tmp_layers = list(layers)
    layer = ["0"] * len(tmp_layers[0])
    tmp_layers.reverse()
    for current in tmp_layers:
        for i in range(len(layer)):
            layer[i] = current[i] if current[i] != "2" else layer[i]
    return "".join(layer)
