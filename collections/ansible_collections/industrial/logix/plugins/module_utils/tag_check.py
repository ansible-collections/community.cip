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
