import pickle
from sqlite3 import Blob

def Serialize(value: any, serializer = pickle) -> Blob:
    """_summary_
    
    Serialize an object to a Binary object

    Args:
        value (any): Value to serialize
        serializer (_type_, optional): Module serializer. Defaults to pickle.

    Returns:
        Blob: Return a Binary
    """
    return serializer.dumps(value)

def Deserialize(value: any, deserializer = pickle) -> any:
    """_summary_
    
    Deserialize an object

    Args:
        value (any): Value to deserialize
        deserializer (_type_, optional): Module serializer. Defaults to pickle.

    Returns:
        any: Return a object, but deserialized
    """
    return deserializer.loads(value)

class Serializer():
    
    def __init__(self, serializer = pickle):
        self.__serializer = serializer
        
    def Serialize(self, value: any):
        """_summary_
    
        Serialize an object to a Binary object

        Args:
            value (any): Value to serialize
            serializer (_type_, optional): Module serializer. Defaults to pickle.

        Returns:
            Blob: Return a Binary
        """
        Serialize(value, self.__serializer)
    
    def Deserialize(self, value: any):
        """_summary_
    
        Deserialize an object

        Args:
            value (any): Value to deserialize
            deserializer (_type_, optional): Module serializer. Defaults to pickle.

        Returns:
            any: Return a object, but deserialized
        """
        Deserialize(value, self.__serializer)