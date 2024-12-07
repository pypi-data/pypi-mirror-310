# moonai/squad.py

from colorama import init, Fore, Style
import time
from typing import List, Dict, Any, Optional, Callable
import json
import logging
from .process import ProcessType

init()



class Squad:
    def __init__(self,
                 agents: Optional[List[Any]] = None,
                 missions: Optional[List[Any]] = None,
                 process: ProcessType = ProcessType.SEQUENTIAL,
                 verbose: bool = False,
                 manager_llm: Optional[str] = None,
                 function_calling_llm: Optional[str] = None,
                 config: Optional[Dict[str, Any]] = None,
                 max_rpm: Optional[int] = None,
                 language: str = "en",
                 language_file: Optional[str] = None,
                 memory_config: Optional[Dict[str, Any]] = None,
                 cache: bool = True,
                 embedder: Dict[str, str] = {"provider": "openai"},
                 full_output: bool = False,
                 step_callback: Optional[Callable] = None,
                 task_callback: Optional[Callable] = None,
                 output_log_file: Optional[str] = None,
                 manager_agent: Optional[Any] = None,
                 manager_callbacks: Optional[List[Callable]] = None,
                 prompt_file: Optional[str] = None,
                 planning: bool = False,
                 planning_llm: Optional[str] = None):

        # Core attributes
        self.agents = {self._normalize_role(agent.role): agent for agent in (agents or [])}
        self.missions = missions or []
        self.verbose = verbose
        self.manager_llm = manager_llm
        self.process_type = process  # Adicione esta linha
        self.manager_agent = None

        # Manager configuration
        if self.process_type == ProcessType.HIERARCHICAL:
            if not self.manager_llm:
                raise ValueError("Hierarchical process requires manager_llm")
            if self.verbose:
                print(f"Initializing manager agent with LLM: {self.manager_llm}")
            from .process import ManagerAgent
            self.manager_agent = ManagerAgent(self.manager_llm)
            
        # Create process
        self.process = self._create_process()
        if not self.process:
            raise ValueError("Failed to create process")
        
        for agent in self.agents.values():
            agent.squad = self
        

        # LLM configuration
        self.manager_llm = manager_llm
        self.function_calling_llm = function_calling_llm
        
        # General configuration
        self.config = config or {}
        self.max_rpm = max_rpm
        self.last_request_time = 0
        
        # Language and localization
        self.language = language
        self._load_language_file(language_file)
        
        # Memory and caching
        self.memory_config = memory_config
        self.cache = cache
        self.embedder = embedder
        
        # Output configuration
        self.full_output = full_output
        self.output_log_file = output_log_file
        self._setup_logging()
        
        # Callbacks
        self.step_callback = step_callback
        self.task_callback = task_callback
        
        # Management
        self.manager_callbacks = manager_callbacks or []
        
        # Planning
        self.planning = planning
        self.planning_llm = planning_llm
        self._load_prompts(prompt_file)
        
        # Internal state
        self.context = {}
        self.message_history = []
        self.max_iterations = 3


    def _create_process(self):
        from .process import SequentialProcess, HierarchicalProcess
        
        if self.process_type == ProcessType.SEQUENTIAL:
            return SequentialProcess()
        elif self.process_type == ProcessType.HIERARCHICAL:
            if not self.manager_agent:
                raise ValueError("Manager agent not initialized for hierarchical process")
            return HierarchicalProcess(manager_agent=self.manager_agent)
        else:
            raise ValueError(f"Invalid process type: {self.process_type}")


    def _load_language_file(self, file_path: Optional[str]):
        """Load language configurations from file"""
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.lang_data = json.load(f)
            except Exception as e:
                print(f"Error loading language file: {e}")
                self.lang_data = {}

    def _load_prompts(self, file_path: Optional[str]):
        """Load custom prompts from file"""
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.custom_prompts = json.load(f)
            except Exception as e:
                print(f"Error loading prompts file: {e}")
                self.custom_prompts = {}

    def _setup_logging(self):
        """Configure logging if output_log_file is specified"""
        if self.output_log_file:
            logging.basicConfig(
                filename=self.output_log_file if isinstance(self.output_log_file, str) else "logs.txt",
                level=logging.INFO,
                format='%(asctime)s - %(message)s'
            )

    def _respect_rate_limit(self):
        """Enforce rate limiting if max_rpm is set"""
        if self.max_rpm:
            current_time = time.time()
            elapsed = current_time - self.last_request_time
            min_interval = 60.0 / self.max_rpm
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            self.last_request_time = time.time()


    def _normalize_role(self, role):
        """Normalizes the role for consistent comparisons"""
        return role.lower().strip()

    def all_missions_complete(self):
        """
        Checks if all missions have been completed
        """
        return all(mission.completed for mission in self.missions)

    def send_message(self, sender_role, receiver_role, message):
        # Normaliza os roles para a comparação
        normalized_receiver = self._normalize_role(receiver_role)
        
        # Encontra o agente com o role mais próximo
        receiver = None
        for role in self.agents:
            if normalized_receiver in role:
                receiver = self.agents[role]
                break
        
        if receiver:
            if receiver.role not in self.context:
                self.context[receiver.role] = []
                
            msg = {"from": sender_role, "to": receiver.role, "message": message}
            self.context[receiver.role].append(msg)
            self.message_history.append(msg)
            
            if self.verbose:
                print(f"\n{Fore.CYAN}Message: {sender_role} -> {receiver.role}: {message}{Style.RESET_ALL}")
        else:
            print(f"Warning: Unable to find an agent with the role '{receiver_role}'")


    def receive_messages(self, receiver_role):
        messages = self.context.get(receiver_role, [])
        self.context[receiver_role] = []  # Limpa as mensagens após leitura
        return messages

    def kickoff(self):
        if self.verbose:
            print(f"{Fore.YELLOW}Starting Squad... Let's go to the moon!{Style.RESET_ALL}")
        
        if self.planning:
            self._plan_missions()
        
        results = []
        iteration = 0
        max_iterations = 5  # Adicionar iterações máximas para evitar loops infinitos
        
        while not self.all_missions_complete() and iteration < max_iterations:
            iteration += 1
            
            # Obter missões do manipulador de processos
            for mission in self.process.execute(self.missions, self):
                self._respect_rate_limit()
                
                messages = self.receive_messages(mission.agent.role)
                if messages:
                    mission.agent.process_messages(messages)
                
                result = mission.run(self)
                if self.task_callback:
                    self.task_callback(mission, result)
                
                results.append(result)
            
            if self.verbose:
                completed = sum(1 for m in self.missions if m.completed)
                total = len(self.missions)
                print(f"\n{Fore.CYAN}Progress: {completed}/{total} missions completed{Style.RESET_ALL}")
        
        if not self.all_missions_complete():
            print(f"\n{Fore.RED}Warning: Not all missions were completed after {max_iterations} iterations{Style.RESET_ALL}")
            incomplete = [m.description for m in self.missions if not m.completed]
            print(f"Incomplete missions: {incomplete}")
        else:
            if self.verbose:
                print(f"\n{Fore.GREEN}All missions have been completed!{Style.RESET_ALL}")
        
        self._log_completion()
        
        # Limpar o cache de todos os agentes após a execução
        if self.verbose:
            print(f"{Fore.YELLOW}Clearing cache of all agents.{Style.RESET_ALL}")
        for agent in self.agents.values():
            agent.clear_cache()
        
        return results if self.full_output else results[-1] if results else None

    def _log_completion(self):
        """Log completion details if logging is enabled"""
        if self.output_log_file:
            logging.info("Squad execution completed")
            if self.message_history:
                logging.info("Communication history:")
                for msg in self.message_history:
                    logging.info(f"{msg['from']} -> {msg['to']}: {msg['message']}")

    def _plan_missions(self):
        """Plan mission execution sequence if planning is enabled"""
        if not self.planning_llm:
            print("Warning: Planning enabled but no planning_llm specified")
            return
            
        # Here you would implement mission planning logic
        # This could involve reordering missions or modifying their descriptions
        pass


def main():
    """
    Entrada principal para a CLI do MoonAI Framework.
    """
    print("Welcome to the MoonAI!")
    print("Use this framework to create AI agents, missions and squads")
    print("\nUsage example:")
    print("1. Configure your agents and missions in code.")
    print("2. Use Squad to organize your workflow.")
    print("\nFor more information, see the documentation at:: https://github.com/brunobracaioli/moonai")