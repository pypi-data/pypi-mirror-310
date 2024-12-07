# esse arquivo está em moonai/process

from enum import Enum
from typing import List, Dict, Optional, Any, Tuple
from .missions import Mission
from .agents import Agent
from colorama import init, Fore, Style

class ProcessType(Enum):
    SEQUENTIAL = "sequential"
    HIERARCHICAL = "hierarchical"

class ManagerAgent(Agent):
    """Special agent class for managing hierarchical processes"""
    def __init__(self, llm):
        super().__init__(
            role="Process Manager",
            goal="Efficiently manage and coordinate mission execution through delegation and oversight",
            backstory="Expert in task management, delegation, and team coordination with deep understanding of each team member's capabilities",
            llm=llm,
            verbose=True
        )
        self.mission_status = {}
        self.execution_plan = []
        self.squad = None  # Will be set by HierarchicalProcess

    def _format_mission_group_info(self, mission_group: List[Mission]) -> str:
        """Formats mission group information for coordination"""
        group_info = []
        for mission in mission_group:
            status = self.mission_status.get(mission, 'Pending')
            tools = [tool.name for tool in mission.tools] if mission.tools else []
            dependencies = [dep.description for dep in mission.context] if mission.context else []
            
            info = [
                f"Mission: {mission.description}",
                f"Agent: {mission.agent.role}",
                f"Status: {status}",
                f"Tools Available: {', '.join(tools) or 'None'}",
                f"Dependencies: {', '.join(dependencies) or 'None'}",
                f"Expected Output: {mission.expected_output}"
            ]
            group_info.append("\n".join(info))
            
        return "\n\n".join(group_info)

    def _process_validation_response(self, response: str, mission_group: List[Mission]) -> bool:
        """Processes validation response with enhanced validation logic"""
        # Primeiro, verifica se há outputs diretos ou mensagens que indicam conclusão
        for mission in mission_group:
            # Verifica output direto
            has_output = mission.output and mission.output.raw
            
            # Verifica mensagens enviadas
            has_messages = False
            if self.squad:
                messages = [msg for msg in self.squad.message_history 
                        if msg['from'] == mission.agent.role]
                has_messages = len(messages) > 0
            
            # Se tem output ou mensagens, considera como potencialmente válido
            if has_output or has_messages:
                # Verifica se o conteúdo corresponde ao esperado
                if mission.expected_output in (mission.output.raw if has_output else '') or \
                any(mission.expected_output in msg['message'] for msg in messages):
                    return True
        
        # Se não encontrou validação direta, processa a resposta do LLM
        is_valid = False
        if "STATUS:" in response:
            status_line = [line for line in response.split('\n') 
                        if "STATUS:" in line][0]
            is_valid = "VALID" in status_line.upper()
            
            # Se inválido, loga os problemas
            if not is_valid and "ISSUES:" in response:
                print("\nValidation Issues:")
                issues_section = response.split("ISSUES:")[1].split("RECOMMENDATIONS:")[0]
                for issue in issues_section.split("-"):
                    if issue.strip():
                        print(f"- {issue.strip()}")
                
                if "RECOMMENDATIONS:" in response:
                    print("\nRecommendations:")
                    recommendations = response.split("RECOMMENDATIONS:")[1]
                    for rec in recommendations.split("-"):
                        if rec.strip():
                            print(f"- {rec.strip()}")
        
        return is_valid
    
    def _format_results_info(self, mission_group: List[Mission]) -> str:
        """Formats the results of missions for validation."""
        formatted_results = []
        for mission in mission_group:
            # Captura o output direto
            result = mission.output.raw if mission.output else 'No output'
            
            # Captura mensagens do histórico do squad
            messages = []
            if self.squad:
                messages = [msg for msg in self.squad.message_history 
                        if msg['from'] == mission.agent.role]
            
            message_text = "\n".join([
                f"Sent Message: {msg['message']} (To: {msg['to']})" 
                for msg in messages
            ]) if messages else "No messages"
            
            info = [
                f"Mission: {mission.description}",
                f"Agent: {mission.agent.role}",
                f"Direct Result: {result}",
                f"Communications:\n{message_text}",
                f"Status: {self.mission_status.get(mission, 'Pending')}"
            ]
            formatted_results.append("\n".join(info))
        
        return "\n\n".join(formatted_results)


    def execute_goal(self) -> str:
        """Execute the manager's goal with a manager-specific system prompt."""
        if self.verbose:
            print(f"\n{Fore.MAGENTA}# Agente: {self.role}{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}## Tarefa: {self.goal}{Style.RESET_ALL}")

        # Prepare a manager-specific system prompt
        system_content = f"""Você é um {self.role}.
            Backstory: {self.backstory}
            
            Its role is to coordinate, plan and validate the agents' missions.
            You must not use tools or send messages to other agents.
            Focus on analyzing the information provided and providing feedback as needed.
            """

        try:
            messages = [
                {"role": "system", "content": system_content},
                {"role": "user", "content": self.goal}
            ]

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=500,
                n=1,
                stop=None,
                temperature=0.2
            )

            output = response.choices[0].message.content.strip()
        except Exception as e:
            output = f"Error: {e}"

        if self.verbose:
            print(f"{Fore.MAGENTA}## Final Answer:{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{output}{Style.RESET_ALL}")

        return output
        
    def create_execution_plan(self, missions: List[Mission]) -> List[List[Mission]]:
        """Creates a detailed execution plan considering dependencies and agent capabilities"""
        missions_info = self._format_missions_info(missions)
        
        # Enhanced planning prompt with focus on dynamic mission analysis
        planning_prompt = f"""As a Process Manager, analyze these specific missions and create a detailed execution plan:

    {missions_info}

    Analysis Requirements:
    1. Identify dependencies:
    - Which missions require output from others
    - Which missions can run in parallel
    - Which missions must be sequential

    2. Consider agent capabilities:
    - Available tools for each agent
    - Agent roles and their mission requirements
    - Communication needs between agents

    3. Create optimal groups based on:
    - Dependencies between missions
    - Efficiency of parallel execution
    - Resource utilization
    - Communication requirements

    Respond EXACTLY in this format:
    EXECUTION_PLAN:
    GROUP 1:
    - Missions: [exact mission descriptions from the list]
    - Rationale: [explain dependencies and grouping logic]
    - Coordination: [specific coordination needs]
    - Success Criteria: [measurable outcomes]

    [Additional groups as needed]

    COORDINATION_STRATEGY:
    [Overall execution strategy with specific steps]"""

        # Atualize o objetivo do manager com o prompt de planejamento
        self.goal = planning_prompt
        response = self.execute_goal()
        return self._parse_execution_plan(response, missions)

    def coordinate_mission_group(self, mission_group: List[Mission]) -> None:
        """Enhanced coordination of mission group execution"""
        group_info = self._format_mission_group_info(mission_group)
        tools_info = self._format_tools_info(mission_group)
        dependencies = self._analyze_dependencies(mission_group)
        
        coordination_prompt = f"""Coordinate this specific mission group based on current state:

    Current Missions State:
    {group_info}

    Available Tools:
    {tools_info}

    Dependencies:
    {dependencies}

    Requirements:
    1. Provide specific instructions for each agent
    2. Consider their available tools
    3. Ensure proper information flow
    4. Address dependency requirements
    5. Validate tool usage before proceeding
    6. Track message exchanges between agents
    7. Ensure sequential execution where needed

    Respond with coordination messages in format:
    SEND_MESSAGE:[exact agent role]:[specific instruction relevant to their mission and tools]"""

        self.goal = coordination_prompt
        coordination_response = self.execute_goal()
        self._process_coordination_instructions(coordination_response, mission_group)

    def validate_group_completion(self, mission_group: List[Mission]) -> bool:
        """Validates mission group results and provides feedback"""
        if not mission_group:
            return True
            
        results_info = self._format_results_info(mission_group)
        expected_outcomes = self._get_expected_outcomes(mission_group)
        
        validation_prompt = f"""Validate the completion of these specific missions:

        {results_info}

        Expected Outcomes:
        {expected_outcomes}

        Validity requirements:
        1. Verify that the responsible agent generates a response (either direct output or sent messages).
        2. Verify that the current mission objective has been achieved.
        3. Evaluate the quality of the results.
        4. Advance to the next stage to complete all missions.
        5. If an agent's mission was accomplished, don't ask him to redo it.
        6. Remember that agents are the experts. You are just there to help them achieve their goal

        Respond EXACTLY in this format:
        STATUS: VALID or INVALID

        If INVALID, provide:
        ISSUES:
        - [specific issue]
        - [specific issue]

        RECOMMENDATIONS:
        - [specific recommendation for each issue]"""

        self.goal = validation_prompt
        validation_response = self.execute_goal()
        is_valid = self._process_validation_response(validation_response, mission_group)
        
        # Atualiza o estado das missões baseado na validação
        for mission in mission_group:
            if is_valid:
                self.mission_status[mission] = "Completed"
                mission.completed = True
            else:
                # Só marca como falha se não houver progressos
                if not mission.output and not any(
                    msg['from'] == mission.agent.role 
                    for msg in (self.squad.message_history if self.squad else [])
                ):
                    self.mission_status[mission] = "Failed"
                    mission.completed = False
        
        return is_valid


    def _format_missions_info(self, missions: List[Mission]) -> str:
        """Enhanced mission information formatting"""
        return "\n\n".join([
            f"Mission Description: {mission.description}\n"
            f"Assigned Agent: {mission.agent.role}\n"
            f"Available Tools: {[tool.name for tool in mission.tools]}\n"
            f"Expected Output: {mission.expected_output}\n"
            f"Dependencies: {[dep.description for dep in mission.context] if mission.context else 'None'}\n"
            f"Current Status: {self.mission_status.get(mission, 'Pending')}"
            for mission in missions
        ])

    def _format_tools_info(self, mission_group: List[Mission]) -> str:
        """Formats information about available tools"""
        tools_by_agent = {}
        for mission in mission_group:
            tools_by_agent[mission.agent.role] = [
                f"{tool.name}: {tool.description}" 
                for tool in mission.tools
            ]
        
        return "\n\n".join([
            f"Agent: {role}\nTools: {', '.join(tools)}"
            for role, tools in tools_by_agent.items()
        ])

    def _analyze_dependencies(self, mission_group: List[Mission]) -> str:
        """Analyzes and formats mission dependencies"""
        dependency_map = {}
        for mission in mission_group:
            if mission.context:
                dependency_map[mission.description] = [
                    dep.description for dep in mission.context
                ]
        
        if not dependency_map:
            return "No dependencies found"
            
        return "\n".join([
            f"Mission '{mission}' depends on: {', '.join(deps)}"
            for mission, deps in dependency_map.items()
        ])

    def _get_expected_outcomes(self, mission_group: List[Mission]) -> str:
        """Formats expected outcomes for validation"""
        return "\n\n".join([
            f"Mission: {mission.description}\n"
            f"Agent: {mission.agent.role}\n"
            f"Expected: {mission.expected_output}\n"
            f"Required Tools: {[tool.name for tool in mission.tools]}\n"
            f"Dependencies Satisfied: {all(dep.completed for dep in mission.context) if mission.context else 'No dependencies'}"
            for mission in mission_group
        ])

    def _process_coordination_instructions(self, response: str, mission_group: List[Mission]) -> None:
        """Enhanced processing of coordination instructions"""
        if not self.squad:
            return
            
        valid_roles = {mission.agent.role for mission in mission_group}
        
        for line in response.split('\n'):
            if line.startswith("SEND_MESSAGE:"):
                try:
                    _, receiver, message = line.split(":", 2)
                    receiver = receiver.strip()
                    
                    if receiver in valid_roles:
                        self.squad.send_message(self.role, receiver, message.strip())
                except ValueError:
                    continue

    def _parse_execution_plan(self, response: str, missions: List[Mission]) -> List[List[Mission]]:
        """Enhanced parsing of execution plan response"""
        if "EXECUTION_PLAN:" not in response:
            print("No execution plan found in response")
            return self._create_default_groups(missions)
            
        try:
            groups = []
            sections = response.split("GROUP")[1:]  # Skip header
            
            print("\nParsing Execution Plan:")
            for i, section in enumerate(sections, 1):
                print(f"\nProcessing Group {i}:")
                if "Missions:" not in section:
                    continue
                    
                missions_text = section[section.find("Missions:"):section.find("Rationale:")]
                print(f"Raw missions text:\n{missions_text}")
                
                # Extract descriptions between dashes or bullet points
                mission_descriptions = []
                for line in missions_text.split('\n'):
                    line = line.strip()
                    if line.startswith('- Mission Description:') or line.startswith('Mission Description:'):
                        desc = line.replace('- Mission Description:', '').replace('Mission Description:', '').strip()
                        if desc:
                            mission_descriptions.append(desc)
                            print(f"Found mission description: {desc}")
                
                group_missions = []
                for desc in mission_descriptions:
                    matched_mission = None
                    # Try exact match first
                    for mission in missions:
                        if desc.strip() == mission.description.strip():
                            matched_mission = mission
                            break
                    
                    # If no exact match, try partial match
                    if not matched_mission:
                        for mission in missions:
                            if desc.lower() in mission.description.lower():
                                matched_mission = mission
                                break
                    
                    if matched_mission and matched_mission not in group_missions:
                        group_missions.append(matched_mission)
                        print(f"Added mission to group: {matched_mission.description}")
                
                if group_missions:
                    groups.append(group_missions)
                    print(f"Created Group {i} with {len(group_missions)} missions")
            
            # Validate created groups
            all_missions = set(missions)
            grouped_missions = set(mission for group in groups for mission in group)
            
            if grouped_missions != all_missions:
                print("\nWarning: Some missions were not included in groups")
                missing = all_missions - grouped_missions
                for mission in missing:
                    print(f"Missing: {mission.description}")
                return self._create_default_groups(missions)
            
            return groups
                
        except Exception as e:
            print(f"Error parsing execution plan: {e}")
            return self._create_default_groups(missions)

    def _find_matching_mission(self, description: str, missions: List[Mission]) -> Optional[Mission]:
        """Finds matching mission using flexible matching"""
        # Try exact match
        for mission in missions:
            if mission.description.strip() == description.strip():
                return mission
        
        # Try contained text
        for mission in missions:
            if description.lower() in mission.description.lower():
                return mission
        
        # Try partial word matching
        desc_words = set(description.lower().split())
        for mission in missions:
            mission_words = set(mission.description.lower().split())
            if desc_words & mission_words:  # If there's any word overlap
                return mission
        
        return None

    def _create_default_groups(self, missions: List[Mission]) -> List[List[Mission]]:
        """Creates mission groups based on dependencies"""
        processed = set()
        groups = []
        
        while len(processed) < len(missions):
            group = []
            
            for mission in missions:
                if mission in processed:
                    continue
                    
                # Check if all dependencies are processed
                if mission.context:
                    if all(dep in processed for dep in mission.context):
                        group.append(mission)
                else:
                    group.append(mission)
            
            # If no missions were added and there are still unprocessed missions,
            # add the first unprocessed mission (breaking circular dependencies)
            if not group:
                for mission in missions:
                    if mission not in processed:
                        group.append(mission)
                        break
            
            if group:
                groups.append(group)
                processed.update(group)
            else:
                break
                
        return groups
    
    

class BaseProcess:
    def execute(self, missions: List[Mission], squad: Any):
        raise NotImplementedError

class SequentialProcess(BaseProcess):
    def execute(self, missions: List[Mission], squad: Any):
        for mission in missions:
            yield mission

class HierarchicalProcess(BaseProcess):
    def __init__(self, manager_llm: Optional[str] = None, manager_agent: Optional[Agent] = None):
        if not manager_agent and not manager_llm:
            raise ValueError("HierarchicalProcess requires either manager_llm or manager_agent")
        self.manager = manager_agent or ManagerAgent(manager_llm)
        self.completed_missions = set()
        self.mission_results = {}
    
    def execute(self, missions: List[Mission], squad: Any):
        """Executes missions in a hierarchical manner with active management"""
        if not missions:
            return
        
        if not self.manager:
            raise ValueError("Manager not initialized")
        
        self.manager.squad = squad
        
        # Cria o plano apenas uma vez
        if not hasattr(self, 'execution_plan'):
            self.execution_plan = self.manager.create_execution_plan(missions)
            print(f"\n{Fore.YELLOW}Execution Plan Created:{Style.RESET_ALL}")
            for i, group in enumerate(self.execution_plan, 1):
                print(f"Group {i}: {[m.description for m in group]}")
        
        current_group_index = 0
        while current_group_index < len(self.execution_plan):
            print(f"\n{Fore.CYAN}Processing Group {current_group_index + 1}{Style.RESET_ALL}")
            
            mission_group = self.execution_plan[current_group_index]
            attempts = 0
            max_attempts = 5  # Reduzido para evitar loops muito longos
            group_completed = False
            
            # Verifica quais missões do grupo ainda não foram completadas
            pending_missions = [m for m in mission_group if not m.completed]
            
            if not pending_missions:
                print(f"Group {current_group_index + 1} already completed, moving to next group")
                current_group_index += 1
                continue
            
            while not group_completed and attempts < max_attempts:
                print(f"\nAttempt {attempts + 1} for group {current_group_index + 1}")
                
                self.manager.coordinate_mission_group(pending_missions)
                
                for mission in pending_missions:
                    if not mission.completed:
                        messages = squad.receive_messages(mission.agent.role)
                        if messages:
                            print(f"\nProcessing messages for {mission.agent.role}:")
                            for msg in messages:
                                print(f"- From: {msg['from']}, Message: {msg['message']}")
                            mission.agent.process_messages(messages)
                        
                        yield mission
                        
                        if mission.output:
                            self.mission_results[mission] = mission.output
                        
                # Valida o grupo atual
                group_completed = self.manager.validate_group_completion(pending_missions)
                
                if group_completed:
                    print(f"\n{Fore.GREEN}Group {current_group_index + 1} completed successfully{Style.RESET_ALL}")
                    current_group_index += 1
                    for mission in pending_missions:
                        mission.completed = True
                        self.completed_missions.add(mission)
                else:
                    print(f"\n{Fore.YELLOW}Group {current_group_index + 1} not completed yet{Style.RESET_ALL}")
                    attempts += 1
            
            if not group_completed:
                print(f"\n{Fore.RED}Failed to complete group {current_group_index + 1} after {max_attempts} attempts{Style.RESET_ALL}")
                break

        # Final validation
        incomplete = [m for m in missions if not m.completed]
        if incomplete:
            print(f"\n{Fore.RED}Warning: Some missions were not completed:{Style.RESET_ALL}")
            for m in incomplete:
                print(f"- {m.description}")
    
    def _coordinate_next_steps(self, completed: List[Mission], group: List[Mission]) -> None:
        """Coordinates transition between missions"""
        next_missions = [m for m in group if m not in completed]
        
        coordination_context = f"""Mission Status Update:
        Completed: {[m.description for m in completed]}
        Pending: {[m.description for m in next_missions]}
        
        Provide any necessary coordination instructions for the next mission(s)."""
        
        self.manager.goal = coordination_context
        self.manager.execute_goal()
    
    def _validate_group_with_retries(self, mission_group: List[Mission], max_attempts: int = 10) -> bool:
        """Validates group completion with multiple attempts"""
        attempts = 0
        
        while attempts < max_attempts:
            if self.manager.validate_group_completion(mission_group):
                return True
            
            attempts += 1
            if attempts < max_attempts:
                self._handle_validation_failure(mission_group, attempts, max_attempts)
        
        return False
    
    def _handle_validation_failure(self, mission_group: List[Mission], attempt: int, max_attempts: int) -> None:
        """Handles failed validation attempts"""
        feedback_context = f"""Group validation failed (attempt {attempt}/{max_attempts}).
        Provide specific feedback and improvement instructions for each mission."""
        
        self.manager.goal = feedback_context
        self.manager.execute_goal()