

class AxesdnError(Exception):

    def __init__(self, fault_string, *args):
        Exception.__init__(self, fault_string, *args)
        self.faultString = fault_string

    def __repr__(self):
        return '<%s>' % self.faultString

    def __str__(self):
        return '%s' % self.faultString

