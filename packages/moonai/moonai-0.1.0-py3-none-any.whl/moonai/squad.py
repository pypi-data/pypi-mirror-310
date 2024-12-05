# moonai/squad.py

from colorama import init, Fore, Style

init()

class Squad:
    def __init__(self, agents=None, missions=None, verbose=False):
        # Armazena os agentes usando o role como chave, mas normaliza o texto
        self.agents = {self._normalize_role(agent.role): agent for agent in (agents or [])}
        self.missions = missions or []
        self.verbose = verbose
        self.context = {}
        self.message_history = []
        self.max_iterations = 3

    def _normalize_role(self, role):
        """Normaliza o role para comparações consistentes"""
        return role.lower().strip()

    def all_missions_complete(self):
        """
        Verifica se todas as missões foram concluídas
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
            print(f"Aviso: Não foi possível encontrar um agente com o cargo '{receiver_role}'")


    def receive_messages(self, receiver_role):
        messages = self.context.get(receiver_role, [])
        self.context[receiver_role] = []  # Limpa as mensagens após leitura
        return messages

    def kickoff(self):
        if self.verbose:
            print(f"{Fore.YELLOW}Iniciando Squad... Let's go to the moon!{Style.RESET_ALL}")
        
        results = []
        iteration = 0
        
        while iteration < self.max_iterations:
            iteration += 1
            has_messages = False
            
            for mission in self.missions:
                if mission.completed:
                    continue
                    
                # Processar mensagens pendentes
                messages = self.receive_messages(mission.agent.role)
                if messages:
                    has_messages = True
                    mission.agent.process_messages(messages)
                
                result = mission.run(self)
                
                if iteration == 1:  # Guardar apenas os resultados iniciais
                    results.append(result)
            
            # Verifica se todas as missões foram concluídas
            if self.all_missions_complete():
                if self.verbose:
                    print(f"\n{Fore.GREEN}Todas as missões foram concluídas!{Style.RESET_ALL}")
                break
                
            # Se não houver mais mensagens e passamos por todas as missões
            if not has_messages:
                break
        
        if self.verbose and self.message_history:
            print(f"\n{Fore.YELLOW}Histórico de comunicação:{Style.RESET_ALL}")
            for msg in self.message_history:
                print(f"{Fore.CYAN}{msg['from']} -> {msg['to']}: {msg['message']}{Style.RESET_ALL}")
        
        return results


def main():
    """
    Entrada principal para a CLI do MoonAI Framework.
    """
    print("Bem-vindo ao MoonAI Framework!")
    print("Use este framework para criar agentes, missões e squads de IA.")
    print("\nExemplo de uso:")
    print("1. Configure seus agentes e missões no código.")
    print("2. Use o Squad para organizar o fluxo de trabalho.")
    print("\nPara mais informações, consulte a documentação em: https://github.com/brunobracaioli/moonai")
