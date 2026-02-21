from typing import Dict, List
import logging
from .KnowledgeBaseAdapter import KnowledgeBaseAdapter

class ComponentLoader:
    def __init__(self, knowledge_base: KnowledgeBaseAdapter):
        self.knowledge_base = knowledge_base
        self.components = {}  # Maps component_id to Component instance
        self.logger = logging.getLogger(__name__)

    def load_component(self, component_id: str, component_type: str) -> None:
        """Load a new component into the system."""
        if component_id in self.components:
            raise ValueError(f"Component {component_id} already exists.")
        
        # Dynamically import and initialize components
        from .components import ComponentFactory
        
        try:
            component = ComponentFactory.create_component(component_type, component_id)
            self.components[component_id] = component
            self.logger.info(f"Component {component_id} loaded successfully.")
        except Exception as e:
            self.logger.error(f"Failed to load component: {str(e)}")

    def unload_component(self, component_id: str) -> None:
        """Unload an existing component from the system."""
        if component_id not in self.components:
            raise ValueError(f"Component {component_id} does not exist.")
        
        del self.components[component_id]
        self.logger.info(f"Component {component_id} unloaded successfully.")

    def get_component(self, component_id: str) -> Optional['Component']:
        """Retrieve a component by ID."""
        return self.components.get(component_id)

    def get_components_by_type(self, component_type: str) -> List['Component']:
        """Retrieve all components of a specific type."""
        return [component for component in self.components.values() if component.type == component_type]