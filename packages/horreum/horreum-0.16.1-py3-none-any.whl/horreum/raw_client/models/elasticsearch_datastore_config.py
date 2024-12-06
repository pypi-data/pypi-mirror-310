from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

@dataclass
class ElasticsearchDatastoreConfig(AdditionalDataHolder, Parsable):
    """
    Type of backend datastore
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: Dict[str, Any] = field(default_factory=dict)

    # Elasticsearch API KEY
    api_key: Optional[str] = None
    # Built In
    built_in: Optional[bool] = None
    # Elasticsearch password
    password: Optional[str] = None
    # Elasticsearch url
    url: Optional[str] = None
    # Elasticsearch username
    username: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> ElasticsearchDatastoreConfig:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: ElasticsearchDatastoreConfig
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return ElasticsearchDatastoreConfig()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        fields: Dict[str, Callable[[Any], None]] = {
            "apiKey": lambda n : setattr(self, 'api_key', n.get_str_value()),
            "builtIn": lambda n : setattr(self, 'built_in', n.get_bool_value()),
            "password": lambda n : setattr(self, 'password', n.get_str_value()),
            "url": lambda n : setattr(self, 'url', n.get_str_value()),
            "username": lambda n : setattr(self, 'username', n.get_str_value()),
        }
        return fields
    
    def serialize(self,writer: SerializationWriter) -> None:
        """
        Serializes information the current object
        param writer: Serialization writer to use to serialize this model
        Returns: None
        """
        if writer is None:
            raise TypeError("writer cannot be null.")
        writer.write_str_value("apiKey", self.api_key)
        writer.write_bool_value("builtIn", self.built_in)
        writer.write_str_value("password", self.password)
        writer.write_str_value("url", self.url)
        writer.write_str_value("username", self.username)
        writer.write_additional_data_value(self.additional_data)
    

