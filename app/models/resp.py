

class JsonResponse(object):

    def __init__(self, status, messge, data):
        self.status = status
        self.messge = messge
        self.data = data

    # 指定一个类的方法为类方法，通常用self来传递当前类的实例--对象，cls传递当前类。
    @classmethod
    def success(cls, status=1, messge='success', data=None):
        return cls(status, messge, data)

    @classmethod
    def fail(cls, status=0, messge='fail', data=None):
        return cls(status, messge, data)

    def to_dict(self):
        return {
            "status": self.status,
            "messge": self.messge,
            "data": self.data
        }