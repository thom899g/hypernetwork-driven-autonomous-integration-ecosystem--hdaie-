from typing import Dict, List
import logging
from .KnowledgeBaseAdapter import KnowledgeBaseAdapter

class HypernetworkController:
    def __init__(self, knowledge_base: KnowledgeBaseAdapter):
        self.knowledge_base = knowledge_base
        self.hypernetworks = {}  # Maps hypernet_id to Hypernetwork instance
        self.logger = logging.getLogger(__name__)

    def create_hypernetwork(self, hypernet_id: str) -> None:
        """Create a new hypernetwork."""
        if hypernet_id in self.hypernetworks:
            raise ValueError(f"Hypernetwork {hypernet_id} already exists.")
        
        from .Hypernetwork import Hypernetwork
        self.hypernetworks[hypernet_id] = Hypernetwork(hypernet_id, self.knowledge_base)
        self.logger.info(f"Hypernetwork {hypernet_id} created successfully.")

    def delete_hypernetwork(self, hypernet_id: str) -> None:
        """Delete an existing hypernetwork."""
        if hypernet_id not in self.hypernetworks:
            raise ValueError(f"Hypernetwork {hypernet_id} does not exist.")
        
        del self.hypernetworks[hypernet_id]
        self.logger.info(f"Hypernetwork {hypernet_id} deleted successfully.")

    def get_hypernetwork(self, hypernet_id: str) -> Optional['Hypernetwork']:
        """Retrieve a hypernetwork by ID."""
        return self.hypernetworks.get(hypernet_id)

    def train_hypernetwork(self