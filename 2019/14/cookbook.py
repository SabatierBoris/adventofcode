import math
from element import Element


class CookBook:
    def __init__(self, datas):
        self.__elements = {}
        self.__reciepes = []
        for data in datas:
            self.__parse_one_reciepe(data)

    def __parse_one_reciepe(self, data):
        needed_infos, product_infos = data.split("=>")

        target = self.__parse_element(product_infos)

        needed = []
        for infos in needed_infos.strip().split(","):
            needed.append(self.__parse_element(infos))

        target[1].be_product_by(set(needed), target[0])

    def __parse_element(self, data):
        raw_qty, name = data.strip().split(" ")
        if name not in self.__elements:
            self.__elements[name] = Element(name)

        return (int(raw_qty), self.__elements[name])

    def get(self, target_name, base_name):
        assert target_name in self.__elements
        assert base_name in self.__elements

        target = self.__elements[target_name]
        base = self.__elements[base_name]

        needed = {target: 1}
        while len(needed) > 1 or base not in needed:
            selected_element = max(needed.keys(), key=lambda e: e.get_distance_to(base))
            ratio = math.ceil(
                needed[selected_element] / selected_element.qty_produced()
            )
            for element, qty in selected_element.producted_by().items():
                if element not in needed:
                    needed[element] = 0
                needed[element] += ratio * qty
            del needed[selected_element]

        return needed[base]
