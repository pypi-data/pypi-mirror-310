from google.protobuf.json_format import MessageToDict
from google._upb._message import RepeatedCompositeContainer, Message


class ProtoSerializer:
    """
    Utility class for converting protobuf messages to JSON-serializable dictionaries.
    """

    def __init__(self, instance):
        """
        Initializes the serializer and converts the instance to its representation.

        Args:
            instance: Protobuf message instance or repeated container.

        Raises:
            TypeError: If the instance is not a valid protobuf message or repeated container.
        """
        self.data = self.to_representation(instance)

    def to_representation(self, instance):
        """
        Converts protobuf to dict, handling both single instances and lists/repeated fields.

        Args:
            instance: Protobuf message instance or repeated container.

        Returns:
            A JSON-serializable dict or list of dicts.

        Raises:
            TypeError: If the instance is not a valid protobuf message or repeated container.
        """
        if isinstance(instance, (RepeatedCompositeContainer, list)):
            return [MessageToDict(obj, preserving_proto_field_name=True) for obj in instance]
        if isinstance(instance, Message):
            return MessageToDict(instance, preserving_proto_field_name=True)
        raise TypeError("Instance must be a protobuf Message or RepeatedCompositeContainer")
