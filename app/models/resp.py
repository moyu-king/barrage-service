

class JsonResponse(object):

    def __init__(self, status, message, data):
        self.status = status
        self.message = message
        self.data = data

    # 指定一个类的方法为类方法，通常用self来传递当前类的实例--对象，cls传递当前类。
    @classmethod
    def success(cls, status=1, message='success', data=None):
        return cls(status, message, data)

    @classmethod
    def fail(cls, status=0, message='fail', data=None):
        return cls(status, message, data)

    def to_dict(self):
        return {
            "status": self.status,
            "message": self.message,
            "data": self.data
        }
