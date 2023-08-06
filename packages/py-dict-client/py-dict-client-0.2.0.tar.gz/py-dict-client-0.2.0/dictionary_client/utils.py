class ReadOnlyDescriptor:
    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = f"_{name}"

    def raise_read_only(self, obj):
        raise AttributeError(
            f"{obj.__class__.__name__}.{self.public_name} is a read-only attribute"
        )

    def __set__(self, obj, value):
        self.raise_read_only(obj)

    def __delete__(self, obj):
        self.raise_read_only(obj)
