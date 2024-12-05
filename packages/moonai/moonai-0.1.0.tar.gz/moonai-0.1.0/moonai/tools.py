# moonai/tools.py

import requests
from bs4 import BeautifulSoup

from abc import ABC, abstractmethod
import inspect

class BaseTool(ABC):
    """Classe base para todas as ferramentas"""
    @property
    def name(self):
        return self.__class__.__name__
    
    @property
    def description(self):
        """Retorna a descrição da ferramenta do docstring"""
        return self.__doc__ or "No description available."
    
    @property
    def parameters(self):
        """Retorna os parâmetros que a ferramenta aceita"""
        sig = inspect.signature(self.execute)
        params = {}
        for name, param in sig.parameters.items():
            if name != 'self':
                params[name] = {
                    'type': str(param.annotation) if param.annotation != inspect.Parameter.empty else 'any',
                    'default': None if param.default == inspect.Parameter.empty else param.default
                }
        return params
    
    @abstractmethod
    def execute(self, *args, **kwargs):
        """Método que cada ferramenta deve implementar"""
        pass

class FileReadTool(BaseTool):
    """Ferramenta para ler conteúdo de arquivos de texto."""
    def execute(self, file_path: str) -> str:
        """
        Lê e retorna o conteúdo de um arquivo.
        
        Args:
            file_path (str): Caminho do arquivo a ser lido
            
        Returns:
            str: Conteúdo do arquivo
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            return f"Erro ao ler arquivo: {str(e)}"

class ScrapeWebsiteTool(BaseTool):
    """Ferramenta para extrair conteúdo de websites."""
    def execute(self, url: str) -> str:
        """
        Extrai conteúdo de uma página web.
        
        Args:
            url (str): URL do site para fazer scraping
            
        Returns:
            str: Conteúdo extraído do site
        """
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs = soup.find_all('p')
            return '\n'.join([p.get_text().strip() for p in paragraphs])
        except Exception as e:
            return f"Erro no scraping: {str(e)}"

class TXTSearchTool(BaseTool):
    """Ferramenta para buscar texto em arquivos."""
    def execute(self, file_path: str, query: str) -> bool:
        """
        Busca um texto específico em um arquivo.
        
        Args:
            file_path (str): Caminho do arquivo
            query (str): Texto a ser buscado
            
        Returns:
            bool: True se encontrou o texto, False caso contrário
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return query in file.read()
        except Exception as e:
            return f"Erro na busca: {str(e)}"


class FileWriteTool(BaseTool):
    """Ferramenta para salvar conteúdo em arquivos de texto."""
    def execute(self, file_path: str, content: str) -> str:
        """
        Salva conteúdo em um arquivo.
        
        Args:
            file_path (str): Caminho do arquivo para salvar
            content (str): Conteúdo a ser salvo
            
        Returns:
            str: Mensagem de confirmação ou erro
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            return f"Conteúdo salvo com sucesso em {file_path}"
        except Exception as e:
            return f"Erro ao salvar arquivo: {str(e)}"