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
        extra_elements = {}
        while len(needed) > 1 or base not in needed:
            selected_element = max(needed.keys(), key=lambda e: e.get_distance_to(base))
            ratio = math.ceil(
                needed[selected_element] / selected_element.qty_produced()
            )
            extra_qty = (
                ratio * selected_element.qty_produced() - needed[selected_element]
            )
            if extra_qty != 0:
                if selected_element not in extra_elements:
                    extra_elements[selected_element] = 0
                extra_elements[selected_element] += extra_qty

            for element, qty in selected_element.producted_by().items():
                if element not in needed:
                    needed[element] = 0
                needed[element] += ratio * qty
            del needed[selected_element]

        return needed[base], extra_elements

    def purge_stock(self, base_name, stock, keep_elements):
        print(stock)
        base = self.__elements[base_name]

        elements = list(stock.keys())
        elements.sort(key=lambda e: e.get_distance_to(base))
        print(elements)
        for element in elements:
            if element in keep_elements:
                continue
            ratio_to_reverse = stock[element] // element.qty_produced()
            print(element, ratio_to_reverse)
            for producer_element, qty in element.producted_by().items():
                if producer_element not in stock:
                    stock[producer_element] = 0
                stock[producer_element] += ratio_to_reverse * qty
            stock[element] -= ratio_to_reverse * element.qty_produced()
        # for element, qty in new_stock.items():
        #    if element not in stock:
        #        stock[element] = 0
        #    stock[element] += qty
        print(stock)
        return stock

    def get_from(self, qty, base_name, target_name):
        assert target_name in self.__elements
        assert base_name in self.__elements

        basic_base_ratio, extra_elements = self.get(target_name, base_name)
        print(basic_base_ratio, extra_elements)

        target = self.__elements[target_name]
        base = self.__elements[base_name]

        stock = {base: qty, target: 0}

        for i in range(200):
            print("Loop", i)
            basic_production = stock[base] // basic_base_ratio
            base_comsomption = basic_production * basic_base_ratio

            stock[base] -= base_comsomption
            stock[target] += basic_production

            for extra_element, qty in extra_elements.items():
                if extra_element not in stock:
                    stock[extra_element] = 0
                stock[extra_element] += basic_production * qty
            print("Revese extra element")
            stock = self.purge_stock(base_name, stock, [base, target])

        # needed = {target: None}
        # for i in range(0):
        #    # while stock[base] > 0:
        #    selected_element = min(
        #        [element for element, qty in needed.items() if qty is None or qty > 0],
        #        key=lambda e: e.get_distance_to(base),
        #    )

        #    print("==============")
        #    print("needed :", needed)
        #    print("stock :", stock)
        #    print("selected element:", selected_element)

        #    if selected_element.can_product_with(stock):
        #        print("Product :", selected_element)
        #        for element, qty in selected_element.producted_by().items():
        #            stock[element] -= qty
        #        if selected_element not in stock:
        #            stock[selected_element] = 0
        #        stock[selected_element] += selected_element.qty_produced()
        #        if needed[selected_element] is not None:
        #            needed[selected_element] -= selected_element.qty_produced()
        #    else:
        #        for element, qty in selected_element.producted_by().items():
        #            if element not in needed:
        #                needed[element] = 0
        #            needed[element] += qty

        # return 0
