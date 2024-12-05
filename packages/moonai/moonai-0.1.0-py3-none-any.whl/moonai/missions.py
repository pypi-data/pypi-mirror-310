# moonai/missions.py

from .tools import FileReadTool, ScrapeWebsiteTool, TXTSearchTool, FileWriteTool
from colorama import init, Fore, Style

class Mission:
    def __init__(self, description, expected_output, agent, tools=None, output_file=None):
        self.description = description
        self.expected_output = expected_output
        self.agent = agent
        self.tools = tools or []
        self.completed = False
        self.output_file = output_file
        
        # Se temos um arquivo de saída, adiciona a ferramenta de escrita
        if output_file:
            self.tools.append(FileWriteTool())
        
    def is_complete(self, output):
        """
        Verifica se a missão foi concluída baseado na saída do agente
        """
        # Verifica se há palavras que indicam conclusão na resposta
        completion_indicators = [
            "concluído", "finalizado", "pronto", "feito", "completado",
            "realizado", "enviado", "recebido", "confirmado"
        ]
        
        return any(indicator in output.lower() for indicator in completion_indicators)

    def run(self, squad):
        if self.completed:
            return None
            
        messages = squad.receive_messages(self.agent.role)
        if messages:
            self.agent.process_messages(messages)
        
        output = self.agent.execute_goal()
        
        # Se temos um arquivo de saída, salva o resultado
        if self.output_file and output:
            write_tool = next((tool for tool in self.tools if isinstance(tool, FileWriteTool)), None)
            if write_tool:
                result = write_tool.execute(self.output_file, output)
                if "Erro" not in result:
                    print(f"\n{Fore.GREEN}Resultado salvo em: {self.output_file}{Style.RESET_ALL}")
        
        # Processa mensagens
        if "SEND_MESSAGE:" in output:
            lines = output.split("\n")
            for line in lines:
                if line.startswith("SEND_MESSAGE:"):
                    _, content = line.split(":", 1)
                    receiver, message = content.split(":", 1)
                    squad.send_message(self.agent.role, receiver.strip(), message.strip())
        
        if self.is_complete(output):
            self.completed = True
            
        return output