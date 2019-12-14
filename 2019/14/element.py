class Element:
    def __init__(self, name):
        self.name = name
        self.__producted_by = {}
        self.__qty_producted = 0
        self.__distance_to = {self: 0}

    def be_product_by(self, source_elements, qty_produced):
        self.__qty_producted = qty_produced
        for qty, element in source_elements:
            self.__producted_by[element] = qty

    def get_distance_to(self, target_element):
        if target_element not in self.__distance_to:
            value = 1
            if target_element not in self.__producted_by:
                value = 1 + max(
                    [
                        e.get_distance_to(target_element)
                        for e in self.__producted_by.keys()
                    ]
                )

            self.__distance_to[target_element] = value
        return self.__distance_to[target_element]

    def qty_produced(self):
        return self.__qty_producted

    def __repr__(self):
        return self.name

    def producted_by(self):
        return self.__producted_by

    def can_product_with(self, stock):
        for element, qty in self.producted_by().items():
            if element not in stock:
                return False
            if stock[element] < qty:
                return False
        return True
