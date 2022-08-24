class TagCheck:
    def __init__(self, logix_util, tag_name):
        self.logix_util = logix_util
        self.tag_name = tag_name
        self.passed = False
        self.msg = ''

    def check_tag_exists(self):
        response = self.logix_util.plc.read(self.tag_name)
        if response.error:
            raise Exception('Tag %s not found' % self.tag_name)

    def check_tag_permissions(self):
        tag_info = self.logix_util.plc.get_tag_info(self.tag_name)
        if tag_info['external_access'] != 'Read/Write':
            raise Exception('Tag %s does not have correct permissions' % self.tag_name)

    def verify(self):
        try:
            self.check_tag_exists()
            self.check_tag_permissions()
            return (True, self.msg)
        except Exception as e:
            self.msg = e
            return (self.passed, self.msg)


# can add type validation for plc_tag for all compare statements
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
        return self.param_tag_value == self.plc_tag_value

    # can support precision in the future
    def compare_float(self):
        return str(self.param_tag_value) in str(self.plc_tag_value)

    # can support ranges in the future
    def compare_int(self):
        return self.param_tag_value == self.plc_tag_value

    def compare(self):
        if self.plc_data_type == 'STRING':
            return self.compare_string()
        elif self.plc_data_type == 'BOOL':
            return self.compare_bool()
        elif self.plc_data_type == 'REAL' or self.plc_data_type == 'FLOAT':
            return self.compare_float()
        elif self.plc_data_type == 'DINT' or self.plc_data_type == 'INT':
            return self.compare_int()
        return False
