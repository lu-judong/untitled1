class Method7:
    # 全变为*
    def all_change(self,x):
        if x is not None:
            a = len(x) * '*'
            return a
        else:
            return x

    # 保留第一位
    def reserve_one(self,x):
        if x is not None and len(x) > 1:
            a = x[0] + (len(x) - 1) * '*'
            return a
        else:
            return x

    # 保留最后一位
    def reserve_lastone(self,x):
        if x is not None and len(x) > 1:
            a = (len(x) - 1) * '*'  + x[-1]
            return a
        else:
            return x

    # 头尾各留一位汉字
    def reserve_one_lastone(self,x):
        if x is not None and len(x) > 2:
            a = x[0] + (len(x) -2) * '*' + x[-1]
            return a
        else:
            return x

    #保留最后两位
    def reserve_last_two(self,x):
        if len(x) > 2:
            a = (len(x) - 2) * '*' + x[-2:]
            return a
        else:
            return x
