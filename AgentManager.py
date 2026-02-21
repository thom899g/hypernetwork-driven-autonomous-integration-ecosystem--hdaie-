from typing import Dict, List, Optional
import logging
from .KnowledgeBaseAdapter import KnowledgeBaseAdapter
from .HypernetworkController import HypernetworkController
from .ComponentLoader import ComponentLoader

class AgentManager:
    def __init__(self, knowledge_base: KnowledgeBaseAdapter, hypernetwork_controller: HypernetworkController):
        self.knowledge_base = knowledge_base
        self.hypernetwork_controller = hypernetwork_controller
        self.agents = {}  # Maps agent_id to Agent instance
        self.logger = logging.getLogger(__name__)

    def register_agent(self, agent_id: str, agent_type: str) -> None:
        """Register a new agent with the system."""
        if agent_id in self.agents:
            raise ValueError(f"Agent {agent_id} already exists.")
        
        # Initialize different types of agents
        if agent_type == "research":
            from .ResearchAgent import ResearchAgent
            self.agents[agent_id] = ResearchAgent(agent_id, self.knowledge_base)
        elif agent_type == "design":
            from .DesignAgent import DesignAgent
            self.agents[agent_id] = DesignAgent(agent_id, self.hypernetwork_controller)
        elif agent_type == "deployment":
            from .DeploymentAgent import DeploymentAgent
            self.agents[agent_id] = DeploymentAgent(agent_id, self.knowledge_base)
        else:
            raise ValueError(f"Invalid agent type: {agent_type}")

        self.logger.info(f"Agent {agent_id} registered successfully.")

    def deregister_agent(self, agent_id: str) -> None:
        """Remove an agent from the system."""
        if agent_id not in self.agents:
            raise ValueError(f"Agent {agent_id} does not exist.")
        
        del self.agents[agent_id]
        self.logger.info(f"Agent {agent_id} deregistered successfully.")

    def get_agent(self, agent_id: str) -> Optional['BaseAgent']:
        """Retrieve an agent by ID."""
        return self.agents.get(agent_id)

    def execute_task(self, task: Dict[str, str]) -> None:
        """Execute a task using the appropriate agent."""
        if "agent_id" not in task or "task_type" not in task:
            raise ValueError("Task must contain 'agent_id' and 'task_type'.")
        
        agent = self.get_agent(task["agent_id"])
        if not agent:
            raise ValueError(f"Agent {task['agent_id']} is not registered.")
        
        try:
            agent.execute_task(task)
            self.logger.info(f"Task executed successfully by agent {agent.agent_id}.")
        except Exception as e:
            self.logger.error(f"Failed to execute task: {str(e)}")