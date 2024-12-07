# moonai/tools.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from abc import ABC, abstractmethod
import inspect
import os

class BaseTool(ABC):
    """Base class for all tools"""
    @property
    def name(self):
        return self.__class__.__name__
    
    @property
    def description(self):
        """Returns the tool description from the docstring"""
        return self.__doc__ or "No description available."
    
    @property
    def parameters(self):
        """Returns the parameters that the tool accepts"""
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
        """Method that each tool must implement"""
        pass

class FileReadTool(BaseTool):
    """Tool to read content from text files."""
    def execute(self, file_path: str) -> str:
        """
        Reads and returns the contents of a file.
        
        Args:
            file_path (str): Path of the file to be read
            
        Returns:
            str: File contents
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"

class ScrapeWebsiteTool(BaseTool):
    """Tool to extract content from websites"""
    def execute(self, url: str) -> str:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove tags irrelevantes
            for tag in soup(['script', 'style', 'header', 'footer', 'nav', 'iframe', 'img']):
                tag.decompose()
            
            # Extrai texto apenas das divs principais
            content = []
            main_containers = soup.find_all(['article', 'main', 'div'])
            for container in main_containers:
                text = container.get_text(separator=' ', strip=True)
                if len(text) > 100:  # Textos longos
                    paragraphs = text.split('. ')
                    content.extend(paragraphs)
            
            # Remove duplicatas e linhas vazias
            cleaned_content = []
            seen = set()
            for text in content:
                text = text.strip()
                if text and text not in seen and len(text) > 20:
                    cleaned_content.append(text + '.')
                    seen.add(text)
            
            return '\n'.join(cleaned_content) if cleaned_content else "No content found."
            
        except Exception as e:
            return f"Error extracting content: {str(e)}"
        
class TXTSearchTool(BaseTool):
    """Tool to search text in files."""
    def execute(self, file_path: str, query: str) -> bool:
        """
        Searches for specific text in a file.
        
        Args:
            file_path (str): File path
            query (str): Text to be searched
            
        Returns:
            bool: True if the text was found, False otherwise
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return query in file.read()
        except Exception as e:
            return f"Search error: {str(e)}"


class FileWriteTool(BaseTool):
    """Tool to save content to text files."""
    def execute(self, file_path: str, content: str) -> str:
        """
        Saves content to a file.
        
        Args:
            file_path (str): File path to save
            content (str): Content to be saved
            
        Returns:
            str: Confirmation or error message
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            return f"Content successfully saved to {file_path}"
        except Exception as e:
            return f"Error saving file: {str(e)}"
        

class ScrapeByTermUrlsTool(BaseTool):
    """Tool to extract content from all pages on a website that contain a specific word."""
    def execute(self, base_url: str, term: str) -> str:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
            }
            
            if not base_url.startswith(('http://', 'https://')):
                base_url = 'https://' + base_url

            # Coleta URLs e faz scraping em uma única etapa
            response = requests.get(base_url, headers=headers, timeout=30)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            
            soup = BeautifulSoup(response.text, 'html.parser')
            urls = [
                urljoin(base_url, link['href'])
                for link in soup.find_all('a', href=True)
                if term.lower() in urljoin(base_url, link['href']).lower()
            ]

            if not urls:
                return f"no content found containing '{term}'"

            # Extrai e formata o conteúdo
            conteudo_final = []
            for url in urls:
                try:
                    response = requests.get(url, headers=headers, timeout=30)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Remove elementos desnecessários
                    for tag in soup(['script', 'style', 'header', 'footer', 'nav', 'iframe', 'img']):
                        tag.decompose()

                    # Coleta título e conteúdo principal
                    title = soup.find('h1') or soup.find('title')
                    title = title.get_text(strip=True) if title else "Untitled"

                    main = soup.find(['main', 'article', 'div[class*="content"]', 'div[class*="product"]'])
                    if main:
                        text = main.get_text(separator='\n', strip=True)
                    else:
                        text = soup.get_text(separator='\n', strip=True)

                    if text:
                        conteudo_final.append(f"{title}\n{text}\n{'='*50}")

                except Exception:
                    continue

            return '\n'.join(conteudo_final) if conteudo_final else "It was not possible to extract the content of the pages"

        except Exception as e:
            return f"Error when accessing {base_url}: {str(e)}"


class MetaMetricsToolLasts7Days(BaseTool):
    """Tool to view data from active Facebook Ads campaigns."""
    def execute(self, dummy: str = "") -> str:
        try:
            from facebook_business.adobjects.adaccount import AdAccount
            from facebook_business.adobjects.adsinsights import AdsInsights
            from facebook_business.api import FacebookAdsApi
            from datetime import datetime, timedelta
            
            # Inicialização
            access_token = os.getenv("my_access_token")
            app_secret = os.getenv("my_app_secret")
            app_id = os.getenv("my_app_id")
            ad_account_id = os.getenv("ad_account_id")

            if not all([access_token, app_secret, app_id, ad_account_id]):
                return "Error: Facebook Ads credentials not found"

            FacebookAdsApi.init(app_id=app_id, app_secret=app_secret, access_token=access_token)
            account = AdAccount(f'act_{ad_account_id}')

            # Período
            hoje = datetime.now().strftime('%Y-%m-%d')
            ha_7_dias = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            periodo = {'since': ha_7_dias, 'until': hoje}

            # Busca campanhas ativas
            campanhas = account.get_campaigns(
                fields=['id', 'name', 'objective', 'daily_budget'],
                params={'effective_status': ['ACTIVE']}
            )

            if not campanhas:
                print("I found no active campaigns.")
                return "I found no active campaigns."

            metricas = [
                AdsInsights.Field.spend,
                AdsInsights.Field.cpc,
                AdsInsights.Field.ctr,
                AdsInsights.Field.cpm,
                AdsInsights.Field.cost_per_unique_outbound_click,
                AdsInsights.Field.frequency,
                AdsInsights.Field.reach,
                AdsInsights.Field.impressions
            ]

            relatorio = f"\n=== FACEBOOK ADS METRICS ({ha_7_dias} a {hoje}) ===\n\n"
            dados_analise = []

            def get_float_value(value, divisor=1):
                """Helper function to convert values"""
                if isinstance(value, list):
                    value = value[0] if value else 0
                try:
                    return float(value) / divisor
                except (ValueError, TypeError):
                    return 0.0

            def get_int_value(value):
                """Helper function to convert integer values"""
                if isinstance(value, list):
                    value = value[0] if value else 0
                try:
                    return int(value)
                except (ValueError, TypeError):
                    return 0

            for campanha in campanhas:
                insights = campanha.get_insights(fields=metricas, params={'time_range': periodo})
                
                if insights:
                    metrica = insights[0]
                    
                    # Processa dados com segurança
                    daily_budget = get_float_value(campanha.get('daily_budget', 0), 100)
                    amount_spent = get_float_value(metrica.get('spend', 0))
                    
                    dados = {
                        'name': campanha['name'],
                        'id': campanha.get('id', 'N/A'),
                        'objective': campanha.get('objective', 'Não informado'),
                        'budget': daily_budget,
                        'spent': amount_spent,
                        'cpc': get_float_value(metrica.get('cpc', 0)),
                        'ctr': get_float_value(metrica.get('ctr', 0)) * 100,
                        'cpm': get_float_value(metrica.get('cpm', 0)),
                        'cpa': get_float_value(metrica.get('cost_per_unique_outbound_click', 0)),
                        'frequency': get_float_value(metrica.get('frequency', 0)),
                        'range': get_int_value(metrica.get('reach', 0)),
                        'impressions': get_int_value(metrica.get('impressions', 0))
                    }
                    
                    dados_analise.append(dados)
                    
                    # Formata relatório
                    relatorio += f"📊 Campaign: {dados['campaign']}\n"
                    relatorio += f"🆔 ID: {dados['id']}\n"
                    relatorio += f"🎯 Objective: {dados['objective']}\n"
                    relatorio += f"💰 Daily Budget: R$ {dados['budget']:.2f}\n"
                    relatorio += f"💸 Total Spend: R$ {dados['spent']:.2f}\n"
                    relatorio += f"🎯 CPC: R$ {dados['cpc']:.2f}\n"
                    relatorio += f"📈 CTR: {dados['ctr']:.2f}%\n"
                    relatorio += f"📊 CPM: R$ {dados['cpm']:.2f}\n"
                    relatorio += f"💲 CPA: R$ {dados['cpa']:.2f}\n"
                    relatorio += f"🔄 Frequency: {dados['frequency']:.1f}\n"
                    relatorio += f"👥 Range: {dados['range']:,}\n"
                    relatorio += f"👀 Impressions: {dados['impressions']:,}\n"
                    relatorio += "-" * 50 + "\n"

            print(relatorio)

            # Calcula totais
            if dados_analise:
                totais = {
                    'campaign': len(dados_analise),
                    'budget_total': sum(d['budget'] for d in dados_analise),
                    'total_spend': sum(d['spend'] for d in dados_analise),
                    'total_range': sum(d['range'] for d in dados_analise),
                    'total_impressions': sum(d['impressions'] for d in dados_analise),
                    'ctr_average': sum(d['ctr'] for d in dados_analise) / len(dados_analise),
                    'cpc_average': sum(d['cpc'] for d in dados_analise) / len(dados_analise),
                    'cpa_average': sum(d['cpa'] for d in dados_analise) / len(dados_analise)
                }

                # Adiciona resumo
                relatorio += f"\n=== GENERAL SUMMARY ===\n"
                relatorio += f"Total Campaigns: {totais['campaigns']}\n"
                relatorio += f"Total Daily Budget: R$ {totais['budget_total']:.2f}\n"
                relatorio += f"Total Spend: R$ {totais['total_spend']:.2f}\n"
                relatorio += f"Total Range: {totais['total_range']:,}\n"
                relatorio += f"Total Impressions: {totais['total_impressions']:,}\n"
                relatorio += f"Average CTR: {totais['ctr_average']:.2f}%\n"
                relatorio += f"Average CTR R$ {totais['cpc_average']:.2f}\n"
                relatorio += f"Average CTR: R$ {totais['cpa_average']:.2f}\n"

            # Retorna dados estruturados
            return str({
                'report': relatorio,
                'data': dados_analise,
                'totals': totais if dados_analise else {}
            })

        except Exception as e:
            erro = f"Error collecting metrics: {str(e)}"
            print(erro)
            return erro