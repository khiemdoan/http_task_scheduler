class SerializableModel:

    def serialize(self):
        properties = {}
        for key, value in self.__dict__.items():
            if isinstance(value, (str, bool, list, dict, int, float)):
                properties[key] = value
        return properties
