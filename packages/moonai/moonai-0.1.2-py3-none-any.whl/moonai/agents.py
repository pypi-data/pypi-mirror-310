# moonai/agents.py

import os
from dotenv import load_dotenv
from openai import OpenAI
from colorama import init, Fore, Style
from anthropic import Anthropic
import time

load_dotenv()
init()

class Agent:
    LLM_PROVIDERS = {
        'gpt-3.5-turbo': ('openai', 'OPENAI_API_KEY'),
        'gpt-4': ('openai', 'OPENAI_API_KEY'),
        'gpt-4-turbo': ('openai', 'OPENAI_API_KEY'),
        'gpt-4o': ('openai', 'OPENAI_API_KEY'),
        'gpt-4o-mini': ('openai', 'OPENAI_API_KEY'),
        'claude-3-5-sonnet-20241022': ('anthropic', 'ANTHROPIC_API_KEY'),
        'claude-3-5-haiku-20241022': ('anthropic', 'ANTHROPIC_API_KEY'),
        'anthropic.claude-3-5-sonnet-20241022-v2:0': ('anthropic', 'ANTHROPIC_API_KEY'),
        'anthropic.claude-3-5-haiku-20241022-v1:0': ('anthropic', 'ANTHROPIC_API_KEY'),
        'claude-3-opus-20240229': ('anthropic', 'ANTHROPIC_API_KEY'),
        'claude-3-sonnet-20240229': ('anthropic', 'ANTHROPIC_API_KEY'),
        'claude-3-haiku-20240307': ('anthropic', 'ANTHROPIC_API_KEY'),
        'anthropic.claude-3-opus-20240229-v1:0': ('anthropic', 'ANTHROPIC_API_KEY'),
        'anthropic.claude-3-sonnet-20240229-v1:0': ('anthropic', 'ANTHROPIC_API_KEY'),
        'anthropic.claude-3-haiku-20240307-v1:0': ('anthropic', 'ANTHROPIC_API_KEY'),
        'gemini-pro': ('google', 'GEMINI_API_KEY'),
    }
    def __init__(self, 
                 role, 
                 goal, 
                 backstory, 
                 llm,
                 max_iter=3,
                 max_rpm=None,
                 max_execution_time=None,
                 verbose=False,
                 tools=None,
                 allow_delegation=False,
                 function_calling_llm=None,
                 step_callback=None,
                 cache=True,
                 system_template=None,
                 prompt_template=None,
                 response_template=None,
                 allow_code_execution=False,
                 max_retry_limit=15,
                 use_system_prompt=True,
                 respect_context_window=True,
                 temperature=0.2,
                 max_tokens=4000,
                 code_execution_mode='safe'):
        
        self.role = role
        self.goal = goal
        self.original_goal = goal
        self.backstory = backstory
        self.max_iter = max_iter
        self.max_rpm = max_rpm
        self.max_execution_time = max_execution_time
        self.verbose = verbose
        self.tools = tools or []
        self.allow_delegation = allow_delegation
        self.function_calling_llm = function_calling_llm
        self.step_callback = step_callback
        self.cache_enabled = cache
        self.cache = [] if self.cache_enabled else None
        self.system_template = system_template
        self.prompt_template = prompt_template
        self.response_template = response_template
        self.allow_code_execution = allow_code_execution
        self.max_retry_limit = max_retry_limit
        self.use_system_prompt = use_system_prompt
        self.respect_context_window = respect_context_window
        self.code_execution_mode = code_execution_mode
        self.message_history = []
        self.last_request_time = 0
        self.has_sent_message = False
        self.temperature = temperature
        self.max_tokens = max_tokens

        # Get provider and model from the llm parameter
        self.llm, self.model = self._get_provider_and_model(llm)
        self.api_key = self._get_api_key()

        # Initialize clients based on provider
        if self.llm.lower() == "openai":
            self.client = OpenAI(api_key=self.api_key)
        elif self.llm.lower() == "anthropic":
            self.client = Anthropic(api_key=self.api_key)

    def _get_provider_and_model(self, llm):
        """
        Determines the provider and model based on the llm parameter.
        """
        if llm in self.LLM_PROVIDERS:
            return self.LLM_PROVIDERS[llm][0], llm
        raise ValueError(f"Model '{llm}' not supported. Available models: {', '.join(self.LLM_PROVIDERS.keys())}")

    def _get_api_key(self):
        """
        Gets the API key for the current provider.
        """
        _, env_var = self.LLM_PROVIDERS[self.model]
        api_key = os.getenv(env_var)
        if not api_key:
            raise ValueError(f"API Key not configured. Configure the environment variable {env_var}.")
        return api_key
    
    def extract_final_response(self, output: str) -> str:
        """
        Extracts the final response from the agent output, delimited by '## Final Response:'.
        
        Args:
            output (str): Complete agent exit.
        
        Returns:
            str: Just the final answer.
        """
        marker = "## Final answer:"
        if marker in output:
            final_response = output.split(marker)[-1].strip()
            return final_response
        return output  # Return all output if marker is not found


    def process_messages(self, messages):
        """
        Processes incoming messages and updates the agent context
        """
        if messages:
            self.message_history.extend(messages)
            
            # Adiciona mensagens ao cache se o cache estiver habilitado
            if self.cache_enabled and self.cache is not None:
                self.cache.extend(messages)
            
            # Formata as mensagens de uma maneira mais clara para o agente
            context = "\n".join([
                f"Last message received: {msg['message']} (From: {msg['from']})" 
                for msg in messages
            ])
            self.goal = f"{self.original_goal}\n\nCurrent context:\n{context}"

    def execute_goal(self):
        """
        Executes the agent's goal and guarantees a single response.
        """
        if self.verbose:
            print(f"\n{Fore.MAGENTA}# Agent: {self.role}{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}## Mission: {self.goal}{Style.RESET_ALL}")

        # Incluir o cache como contexto adicional se estiver habilitado
        if self.cache_enabled and self.cache:
            cache_context = "\n".join([
                f"Message from {msg['from']} to {msg['to']}: {msg['message']}" 
                for msg in self.cache
            ])
            self.goal = f"{self.original_goal}\n\nMessage History (This is just the current context of the Squad to use as additional information to be more efficient):\n{cache_context}"

        # Execute based on provider
        if self.llm.lower() == "openai":
            output = self._execute_openai()
        elif self.llm.lower() == "anthropic":
            output = self._execute_anthropic()
        else:
            output = "Erro: LLM not supported"

        if self.verbose:
            print(f"{Fore.MAGENTA}## Final answer:{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{output}{Style.RESET_ALL}")

        return output
    

    def clear_cache(self):
        """Clears the agent cache"""
        if self.cache_enabled and self.cache is not None:
            self.cache.clear()
            if self.verbose:
                print(f"\n{Fore.YELLOW}Agent cache '{self.role}' was cleaned.{Style.RESET_ALL}")
    

    def _execute_anthropic(self):
        try:
            # Prepare tools information
            tools_info = []
            for tool in self.tools:
                tools_info.append(
                    f"""Tool: {tool.name}
                    Description: {tool.description}
                    Parameters: {tool.parameters}
                    """
                )
            
            tools_instruction = "\n".join(tools_info) if tools_info else "No tools available."
            
            system_content = f"""Você é um {self.role}.
                        Backstory: {self.backstory}

                        Important instructions:
                        1. When generating your response, return exactly what was asked of you.

                        2. When referring to yourself, use your title: {self.role}

                        3. If the user asks you to return only the requested content in your response, without any other message or text, comply.

                        Available tools:
                        {tools_instruction}

                        To use tools:
                        USE_TOOL:tool_name:param1=value1,param2=value2

                        To send messages to other agents:v
                        SEND_MESSAGE:agent_name:message

                        Example of using the FileReadTool tool:
                        USE_TOOL:FileReadTool:file_path=C:/path/to/file.txt

                        Example of sending a message:
                        SEND_MESSAGE:Agent-name: Here is the message.

                        Notes:
                        - Do not use quotes around parameter values
                        - Use full paths for files
                        - After receiving the result from the tool, continue your mission
                        - Use SEND_MESSAGE to communicate relevant information to other agents when necessary
                        """

            # Respect rate limits if configured
            self._respect_rate_limit()

            messages = [
                {
                    "role": "user",
                    "content": self.goal
                }
            ]

            last_response = None
            output = None

            while True:
                try:
                    response = self.client.messages.create(
                        model=self.model,
                        max_tokens=self.max_tokens,
                        system=system_content,
                        temperature=self.temperature,
                        messages=messages
                    )

                    if not response.content or len(response.content) == 0:
                        raise ValueError("Empty API response")

                    output = response.content[0].text
                    
                    # Append the assistant's response to maintain context
                    messages.append({"role": "assistant", "content": output})
                    last_response = output

                    # Process commands
                    if "USE_TOOL:" in output or ("SEND_MESSAGE:" in output and not self.has_sent_message):
                        commands = [line.strip() for line in output.split('\n') 
                                if line.strip().startswith(("USE_TOOL:", "SEND_MESSAGE:"))
                                and len(line.split(':')) >= 3]  # Ensure proper format

                        if not commands:
                            break

                        for command in commands:
                            try:
                                if command.startswith("USE_TOOL:"):
                                    parts = command.split(':', 2)
                                    if len(parts) != 3:
                                        continue
                                    
                                    tool_name = parts[1].strip()
                                    params_str = parts[2].strip()
                                    
                                    tool = next((t for t in self.tools if t.name == tool_name), None)
                                    if not tool:
                                        continue

                                    # Parse parameters
                                    params = {}
                                    if 'content=' in params_str:
                                        pre_content, content = params_str.split('content=', 1)
                                        # Process other parameters
                                        for param in pre_content.split(','):
                                            if '=' in param:
                                                key, value = param.split('=', 1)
                                                params[key.strip()] = value.strip()
                                        # Add content
                                        params['content'] = content.strip()
                                    else:
                                        for param in params_str.split(','):
                                            if '=' in param:
                                                key, value = param.split('=', 1)
                                                params[key.strip()] = value.strip()

                                    # Execute tool and handle result
                                    result = tool.execute(**params)
                                    messages.append({"role": "user", "content": f"Tool result {tool_name}:\n{result}"})

                                elif command.startswith("SEND_MESSAGE:") and not self.has_sent_message:
                                    _, receiver, message = command.split(":", 2)
                                    if hasattr(self, 'squad'):
                                        self.squad.send_message(self.role, receiver.strip(), message.strip())
                                        self.has_sent_message = True

                            except Exception as e:
                                messages.append({"role": "user", "content": f"Command error: {str(e)}"})
                    else:
                        break

                except Exception as e:
                    print(f"Execution error: {str(e)}")
                    return f"Error: {str(e)}"

            # Extract and return final response
            if last_response:
                return self.extract_final_response(last_response)
            elif output:
                return self.extract_final_response(output)
            return "Error: Unable to generate a response"

        except Exception as e:
            print(f"General execution error: {str(e)}")
            return ""
    
    def _respect_rate_limit(self):
        if self.max_rpm:
            current_time = time.time()
            elapsed = current_time - self.last_request_time
            min_interval = 60.0 / self.max_rpm
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            self.last_request_time = time.time()

    def _execute_openai(self):
        try:
            # Prepare information about available tools
            tools_info = []
            for tool in self.tools:
                tools_info.append(
                    f"""Tool: {tool.name}
                    Description: {tool.description}
                    Parameters: {tool.parameters}
                    """
                )
            
            tools_instruction = "\n".join(tools_info) if tools_info else "No tools available."
            
            system_content = f"""Você é um {self.role}.
    Backstory: {self.backstory}

    Important instructions:
    1. When generating your response, return exactly what was asked of you.

    2. When referring to yourself, use your title: {self.role}

    3. If the user asks you to return only the requested content in your response, without any other message or text, comply.

    Available tools:
    {tools_instruction}

    To use tools:
    USE_TOOL:tool_name:param1=value1,param2=value2

    To send messages to other agents:v
    SEND_MESSAGE:agent_name:message

    Example of using the FileReadTool tool:
    USE_TOOL:FileReadTool:file_path=C:/path/to/file.txt

    Example of sending a message:
    SEND_MESSAGE:Agent-name: Here is the message.

    Notes:
    - Do not use quotes around parameter values
    - Use full paths for files
    - After receiving the result from the tool, continue your mission
    - Use SEND_MESSAGE to communicate relevant information to other agents when necessary
    """
            
            messages = [
                {"role": "system", "content": system_content},
                {"role": "user", "content": self.goal}
            ]

            while True:
                try:
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=messages,
                        max_tokens=self.max_tokens,
                        n=1,
                        stop=None,
                        temperature=self.temperature
                    )
                    
                    output = response.choices[0].message.content.strip()
                    final_response = self.extract_final_response(output)
                    
                    if self.verbose:
                        print(f"{Fore.MAGENTA}## Final Answer:{Style.RESET_ALL}")
                        print(f"{Fore.GREEN}{final_response}{Style.RESET_ALL}")
                    
                    # Check for tool commands or messages in the response
                    if "USE_TOOL:" in output or ("SEND_MESSAGE:" in output and not self.has_sent_message):
                        # Find all commands USE_TOOL: and SEND_MESSAGE:
                        tool_commands = [line for line in output.split('\n') if line.startswith("USE_TOOL:") or line.startswith("SEND_MESSAGE:")]
                        
                        if not tool_commands:
                            break  # No commands to process
                        
                        for command in tool_commands:
                            try:
                                if command.startswith("USE_TOOL:"):
                                    _, tool_name, params_str = command.split(":", 2)
                                    tool_name = tool_name.strip()
                                    
                                    # Find the corresponding tool
                                    tool = next((t for t in self.tools if t.name == tool_name), None)
                                    
                                    if tool:
                                        params = {}
                                        
                                        # Check if 'content=' is present to avoid comma problems
                                        if 'content=' in params_str:
                                            pre_content, content_part = params_str.split('content=', 1)
                                            
                                            # Process parameters before 'content='
                                            if pre_content:
                                                for param in pre_content.split(','):
                                                    if '=' in param:
                                                        key, value = param.split('=', 1)
                                                        params[key.strip()] = value.strip().strip("'").strip('"')
                                                    else:
                                                        print(f"Invalid parameter: {param}")
                                            
                                            # Assign everything else to 'content'
                                            params['content'] = content_part.strip()
                                        else:
                                            # Process parameters normally
                                            for param in params_str.split(','):
                                                if '=' in param:
                                                    key, value = param.split('=', 1)
                                                    params[key.strip()] = value.strip().strip("'").strip('"')
                                                else:
                                                    print(f"Invalid parameter: {param}")
                                        
                                        # Run the tool
                                        result = tool.execute(**params)
                                        
                                        # Add result to context and clearly inform if there was an error
                                        if "Erro" in result:
                                            error_message = f"The tool {tool_name} returned an error: {result}\nCheck the file path and try again."
                                            messages.append({"role": "user", "content": error_message})
                                        else:
                                            success_message = f"Tool result {tool_name}:\n{result}"
                                            messages.append({"role": "user", "content": success_message})
                                
                                elif command.startswith("SEND_MESSAGE:") and not self.has_sent_message:
                                    _, receiver, message = command.split(":", 2)
                                    receiver = receiver.strip()
                                    message = message.strip()
                                    
                                    # Send message via Squad
                                    self.squad.send_message(self.role, receiver, message)
                                    
                                    if self.verbose:
                                        print(f"{Fore.CYAN}Message sent to {receiver}: {message}{Style.RESET_ALL}")
                                    
                                    # Set the flag to prevent resending
                                    self.has_sent_message = True
                                
                            except ValueError:
                                print(f"Badly formatted command: {command}")
                                continue
                    else:
                        # No more tool commands or messages to process
                        break

                except Exception as e:
                    print(f"Execution error: {e}")
                    return f"Error: {e}"
            
            # Retornar a resposta final
            return final_response


        except Exception as e:
            print(f"General execution error: {e}")
            return ""

