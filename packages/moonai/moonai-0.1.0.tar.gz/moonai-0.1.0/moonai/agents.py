# moonai/agents.py

import os
from dotenv import load_dotenv
from openai import OpenAI
from colorama import init, Fore, Style

load_dotenv()
init()

class Agent:
    def __init__(self, role, goal, backstory, llm, model, max_iter=3, verbose=False, tools=None, allow_delegation=False):
        self.role = role
        self.goal = goal
        self.original_goal = goal  # Mantém o objetivo original
        self.backstory = backstory
        self.llm = llm
        self.model = model
        self.max_iter = max_iter
        self.verbose = verbose
        self.tools = tools or []
        self.allow_delegation = allow_delegation
        self.message_history = []

        # Carregar a API Key com base no provedor da LLM
        self.api_key = self._get_api_key(llm)

        if self.llm.lower() == "openai":
            api_key = os.environ.get("OPENAI_API_KEY")
            self.client = OpenAI(api_key=api_key)

    def _get_api_key(self, llm):
        """
        Retorna a API Key correta com base no provedor da LLM.
        """
        keys = {
            "openai": "OPENAI_API_KEY",
            "claude": "CLAUDE_API_KEY",
            "gemini": "GEMINI_API_KEY"
        }

        llm_key = keys.get(llm.lower())
        if not llm_key:
            raise ValueError(f"LLM '{llm}' não suportada. Certifique-se de configurar um agente válido.")
        
        api_key = os.getenv(llm_key)
        if not api_key:
            raise ValueError(f"API Key para '{llm}' não configurada. Certifique-se de que '{llm_key}' está no arquivo .env.")
        
        return api_key
    

    def process_messages(self, messages):
        """
        Processa mensagens recebidas e atualiza o contexto do agente
        """
        if messages:
            self.message_history.extend(messages)
            # Formata as mensagens de uma maneira mais clara para o agente
            context = "\n".join([
                f"Última mensagem recebida: {msg['message']} (De: {msg['from']})" 
                for msg in messages
            ])
            self.goal = f"{self.original_goal}\n\nContexto atual:\n{context}"

    def execute_goal(self):
        if self.verbose:
            print(f"\n{Fore.MAGENTA}# Agent: {self.role}{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}## Task: {self.goal}{Style.RESET_ALL}")
        
        output = self._execute_openai() if self.llm.lower() == "openai" else "Unsupported LLM"
        
        if self.verbose:
            print(f"{Fore.MAGENTA}## Final Answer:{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{output}{Style.RESET_ALL}")
        
        return output

    def _execute_openai(self):
        try:
            # Preparar informações sobre as ferramentas disponíveis
            tools_info = []
            for tool in self.tools:
                tools_info.append(
                    f"""Tool: {tool.name}
                    Description: {tool.description}
                    Parameters: {tool.parameters}
                    """
                )
            
            tools_instruction = "\n".join(tools_info) if tools_info else "Sem ferramentas disponíveis."
            
            system_content = f"""Você é um {self.role}.
                Backstory: {self.backstory}
                
                Instruções importantes:
                1. Para enviar mensagem para outro agente, use o cargo/role dele
                Exemplo: SEND_MESSAGE:Estagiário de marketing:Esta é a sua tarefa para hoje
                
                2. Ao se referir a si mesmo, use seu cargo: {self.role}

                3. Quando finalizar sua tarefa, inclua palavras como 'pronto', 'concluído' e variações semelhantes.
                
                Ferramentas disponíveis:
                {tools_instruction}
                
                Para usar ferramentas:
                USE_TOOL:nome_da_ferramenta:param1=valor1,param2=valor2
                
                Exemplo de uso da ferramenta FileReadTool:
                USE_TOOL:FileReadTool:file_path=C:/caminho/do/arquivo.txt
                
                Observações:
                - Não use aspas nos valores dos parâmetros
                - Use caminhos completos para arquivos
                - Após receber o resultado da ferramenta, continue sua tarefa
                """

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
                temperature=0.7
            )
            
            output = response.choices[0].message.content.strip()
            
            # Processar uso de ferramentas
            if "USE_TOOL:" in output:
                for line in output.split('\n'):
                    if line.startswith("USE_TOOL:"):
                        # Extrair informações da ferramenta
                        _, tool_name, params_str = line.split(":", 2)
                        tool_name = tool_name.strip()
                        
                        # Encontrar a ferramenta correspondente
                        tool = next((t for t in self.tools if t.name == tool_name), None)
                        
                        if tool:
                            # Converter string de parâmetros em dicionário
                            params = {}
                            if params_str:
                                for param in params_str.split(','):
                                    key, value = param.split('=')
                                    # Remove aspas simples ou duplas dos valores
                                    value = value.strip().strip("'").strip('"')
                                    params[key.strip()] = value
                            
                            # Executar a ferramenta
                            result = tool.execute(**params)
                            
                            # Adicionar resultado ao contexto e informar claramente se houve erro
                            if "Erro" in result:
                                messages.extend([
                                    {"role": "assistant", "content": output},
                                    {"role": "user", "content": f"A ferramenta {tool_name} retornou um erro: {result}\nVerifique o caminho do arquivo e tente novamente."}
                                ])
                            else:
                                messages.extend([
                                    {"role": "assistant", "content": output},
                                    {"role": "user", "content": f"Resultado da ferramenta {tool_name}:\n{result}"}
                                ])
                            
                            # Obter nova resposta com o resultado
                            response = self.client.chat.completions.create(
                                model=self.model,
                                messages=messages,
                                max_tokens=500,
                                n=1,
                                stop=None,
                                temperature=0.7
                            )
                            
                            output = response.choices[0].message.content.strip()
            
            return output
        except Exception as e:
            print(f"Erro na execução: {e}")
            return ""