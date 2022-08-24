class TagValueCheck():
    def __init__(self, param_tag_value, plc_tag):
        self.param_tag_value = param_tag_value
        self.plc_tag_value = plc_tag.value
        self.plc_data_type = plc_tag.type

    def update_plc_tag(self, plc_tag):
        self.plc_tag_value = plc_tag.value
        self.plc_tag_type = plc_tag.type

    def compare_str(self):
        return self.param_tag_value.lower() == self.plc_tag_value.lower()

    def compare_bool(self):
        # import q; q.q(self.param_tag_value)
        # if not isinstance(self.param_tag_value, bool):
        #     raise Exception('%s expects type to be %s' % (tag_name, plc_tag.type))
        return self.param_tag_value == self.plc_tag_value

    # can support precision in the future
    def compare_float(self):
        return str(self.param_tag_value) in str(self.plc_tag_value)

    # can support ranges in the future
    def compare_int(self):
        return self.param_tag_value == self.plc_tag_value

    def compare(self):
        if self.plc_data_type == 'BOOL':
            return self.compare_bool()
        elif self.plc_data_type == 'REAL' or self.plc_data_type == 'FLOAT':
            return self.compare_float()
        elif self.plc_data_type == 'DINT' or self.plc_data_type == 'INT':
            return self.compare_int()
        return False
