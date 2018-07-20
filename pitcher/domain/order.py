

class Order(object):
    def __init__(self, code, action, shares, price, total, date_time, trade_fee):
        self.code = code
        self.action = action
        self.shares = shares
        self.price =price
        self.total = total
        self.date_time = date_time
        self.trade_fee = trade_fee


    def __repr__(self):
        # Override to print a readable string presentation of your object
        # below is a dynamic way of doing this without explicity constructing the string manually
        return ', '.join(['{key}={value}'.format(key=key, value=self.__dict__.get(key)) for key in self.__dict__])