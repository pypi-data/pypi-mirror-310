# moonai/missions.py

from .tools import FileReadTool, FileWriteTool
from colorama import init, Fore, Style
import asyncio
from typing import Any, List, Dict, Optional, Type, Callable
from pydantic import BaseModel
import json
import time


class TaskOutput:
    def __init__(self, raw_output: str, json_output: dict = None, pydantic_output: BaseModel = None):
        self.raw = raw_output
        self.json = json_output
        self.pydantic = pydantic_output
        self.timestamp = None
        self.execution_time = None

class Mission:
    def __init__(self, 
                 description: str,
                 expected_output: str,
                 agent: Any,
                 tools: Optional[List[Any]] = None,
                 async_execution: bool = False,
                 context: Optional[List["Mission"]] = None,
                 config: Optional[Dict[str, Any]] = None,
                 output_json: Optional[Type[BaseModel]] = None,
                 output_pydantic: Optional[Type[BaseModel]] = None,
                 output_file: Optional[str] = None,
                 callback: Optional[Callable] = None,
                 human_input: bool = False,
                 converter_cls: Optional[Type] = None):
        
        self.description = description
        self.expected_output = expected_output
        self.agent = agent
        self.tools = tools or []
        self.async_execution = async_execution
        self.context = context or []
        self.config = config or {}
        self.output_json = output_json
        self.output_pydantic = output_pydantic
        self.output_file = output_file
        self.callback = callback
        self.human_input = human_input
        self.converter_cls = converter_cls
        self.completed = False
        self.output = None

        if output_file and not any(isinstance(tool, FileWriteTool) for tool in self.tools):
            self.tools.append(FileWriteTool())

    def _save_output_to_file(self, content: str) -> None:
        """Helper method to save content to the specified output file"""
        write_tool = next((tool for tool in self.tools if isinstance(tool, FileWriteTool)), None)
        if write_tool:
            result = write_tool.execute(file_path=self.output_file, content=content)
            if "Error" not in result:
                print(f"\n{Fore.GREEN}Result saved in: {self.output_file}{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.RED}Error saving to file: {result}{Style.RESET_ALL}")

    def _extract_content_from_response(self, raw_output: str) -> str:
        """
        Extracts actual content from agent response, removing tool commands and other metadata.
        """
        # Primeiro, divide por linhas e remove comandos de ferramentas e mensagens
        lines = []
        content = None
        tool_result = None
        
        for line in raw_output.split('\n'):
            line = line.strip()
            # Ignora linhas vazias e comandos
            if not line or line.startswith(('USE_TOOL:', 'SEND_MESSAGE:', '## Final Answer:')):
                continue
            
            # Captura resultado da ferramenta
            if line.startswith('Tool result'):
                tool_result = line.split(':', 1)[1].strip() if ':' in line else None
                continue
            
            # Captura conteúdo que não são comandos ou resultados
            if not line.startswith(('Error:', 'Saved content')):
                lines.append(line)
        
        # Se temos um resultado de ferramenta, use-o
        if tool_result:
            content = tool_result
        # Caso contrário, use as linhas filtradas
        elif lines:
            content = '\n'.join(lines)
        
        return content.strip() if content else ''

    def run(self, squad):
        if self.async_execution:
            return asyncio.run(self._run_async(squad))
        return self._run_sync(squad)

    async def _run_async(self, squad):
        return await asyncio.create_task(self._execute(squad))

    def _run_sync(self, squad):
        start_time = time.time()
        
        if self.completed:
            return None

        self._process_context()
            
        messages = squad.receive_messages(self.agent.role)
        if messages:
            self.agent.process_messages(messages)
        
        raw_output = self.agent.execute_goal()

        # Create TaskOutput instance and store it
        self.output = TaskOutput(raw_output)
        self.output.execution_time = time.time() - start_time

        # Handle errors
        if "Error:" in raw_output or "Failure:" in raw_output:
            print(f"\n[!] Agent {self.agent.role} found an error. Trying again...\n")
            return self.retry(squad)

        # Process structured outputs
        if self.output_json:
            try:
                self.output.json = json.loads(raw_output)
            except json.JSONDecodeError as e:
                print(f"Error processing JSON: {e}")

        if self.output_pydantic:
            try:
                self.output.pydantic = self.output_pydantic.parse_raw(raw_output)
            except ValueError as e:
                print(f"Error processing Pydantic: {e}")

        # Process messages for delegation
        if "SEND_MESSAGE:" in raw_output:
            self._process_messages(raw_output, squad)

        # Extract and save content if output_file is specified
        if self.output_file:
            actual_content = self._extract_content_from_response(raw_output)
            if actual_content:
                write_tool = next((tool for tool in self.tools if isinstance(tool, FileWriteTool)), None)
                if write_tool:
                    try:
                        result = write_tool.execute(file_path=self.output_file, content=actual_content)
                        if "Error" not in result:
                            print(f"\n{Fore.GREEN}Result saved in: {self.output_file}{Style.RESET_ALL}")
                        else:
                            print(f"\n{Fore.RED}Error saving to file: {result}{Style.RESET_ALL}")
                    except Exception as e:
                        print(f"\n{Fore.RED}Error saving to file: {str(e)}{Style.RESET_ALL}")

        # Human review if required
        if self.human_input:
            if not self._get_human_approval():
                return self.retry(squad)

        # Execute callback if provided
        if self.callback:
            self.callback(self.output)

        self.completed = True

        # Reset the agent's goal to avoid context carryover
        self.agent.goal = self.agent.original_goal
        self.agent.has_sent_message = False

        return self.output


    def _process_context(self):
        """Process context from dependent tasks"""
        context_outputs = [task.output.raw for task in self.context if task.output]
        if context_outputs:
            self.agent.goal = f"{self.agent.goal}\n\nAdditional context:\n" + "\n".join(context_outputs)

    def _save_output(self, output):
        """Save output to file"""
        write_tool = next((tool for tool in self.tools if isinstance(tool, FileWriteTool)), None)
        if write_tool:
            result = write_tool.execute(self.output_file, output)
            if "Error" not in result:
                print(f"\n{Fore.GREEN}Result saved in: {self.output_file}{Style.RESET_ALL}")

    def _process_messages(self, output, squad):
        """Process delegation messages"""
        for line in output.split("\n"):
            if line.startswith("SEND_MESSAGE:"):
                _, content = line.split(":", 1)
                receiver, message = content.split(":", 1)
                squad.send_message(self.agent.role, receiver.strip(), message.strip())

    def _get_human_approval(self):
        """Get human approval for the task output"""
        print(f"\n{Fore.YELLOW}=== Human Mission Review ===")
        print(f"Description: {self.description}")
        print(f"Output obtained:\n{Fore.WHITE}{self.output.raw if self.output else 'No exit available'}{Style.RESET_ALL}\n")
        
        approval = input(f"{Fore.YELLOW}Approve this departure? (y/n): {Style.RESET_ALL}")
        approved = approval.lower() == 'y'
        
        print(f"\n{Fore.GREEN if approved else Fore.RED}")
        print("✓ Exit approved!" if approved else "✗ Output rejected - Starting retry...")
        print(f"{Style.RESET_ALL}")

        # Se não foi aprovado, limpa a saída atual para forçar uma nova geração
        if not approved:
            self.output = None
            # Reset do estado do agente para garantir uma nova resposta
            self.agent.message_history = []
            self.agent.has_sent_message = False
        
        return approved

    def retry(self, squad):
        """Retry the mission execution with a fresh state"""
        start_time = time.time()
        
        # Reset do estado do agente para garantir uma nova resposta
        self.agent.message_history = []
        self.agent.has_sent_message = False
        
        # Processa o contexto novamente para manter as dependências
        self._process_context()
        
        # Reprocessa mensagens do squad
        messages = squad.receive_messages(self.agent.role)
        if messages:
            self.agent.process_messages(messages)
        
        # Gera nova resposta
        raw_output = self.agent.execute_goal()
        
        output = TaskOutput(raw_output)
        output.execution_time = time.time() - start_time

        # Process structured outputs again
        if self.output_json:
            try:
                output.json = json.loads(raw_output)
            except json.JSONDecodeError as e:
                print(f"Error processing JSON: {e}")

        if self.output_pydantic:
            try:
                output.pydantic = self.output_pydantic.parse_raw(raw_output)
            except ValueError as e:
                print(f"Error processing Pydantic: {e}")

        # Extract and save content if output_file is specified
        if self.output_file:
            actual_content = self._extract_content_from_response(raw_output)
            if actual_content:
                write_tool = next((tool for tool in self.tools if isinstance(tool, FileWriteTool)), None)
                if write_tool:
                    try:
                        result = write_tool.execute(file_path=self.output_file, content=actual_content)
                        if "Error" not in result:
                            print(f"\n{Fore.GREEN}Result saved in: {self.output_file}{Style.RESET_ALL}")
                        else:
                            print(f"\n{Fore.RED}Error saving to file: {result}{Style.RESET_ALL}")
                    except Exception as e:
                        print(f"\n{Fore.RED}Error saving to file: {str(e)}{Style.RESET_ALL}")

        # Process any new messages
        if "SEND_MESSAGE:" in raw_output:
            self._process_messages(raw_output, squad)

        # Atualiza o output da missão com a nova resposta
        self.output = output

        # Check for human approval again if required
        if self.human_input:
            if not self._get_human_approval():
                return self.retry(squad)  # Recursive retry if not approved

        if "Error:" in raw_output or "Failure:" in raw_output:
            print(f"\n[✘] Agent {self.agent.role} failed again. Output: {raw_output}\n")
            self.completed = False
        else:
            self.completed = True
            print(f"\n[✔] Agent {self.agent.role} completed the mission successfully after the attempt.")
        
        return output