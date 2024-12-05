"""
# Moon AI Framework

Um framework poderoso para criar e gerenciar equipes de agentes de IA com missões específicas.

## Instalação

```bash
pip install moonai
```

## Exemplo rápido de uso

```python
from moonai import Agent, Mission, Squad
from moonai.tools import FileReadTool

# Criar agentes
gerente = Agent(
    role="Gerente de Marketing",
    goal="Coordenar a equipe de marketing",
    backstory="Especialista em gestão de equipes",
    llm="openai",
    model="gpt-4",
    verbose=True
)

# ... restante do exemplo
```

## Documentação

Para mais informações, visite [https://github.com/brunobracaioli/moonai](https://github.com/brunobracaioli/moonai)

## Contribuindo

Contribuições são bem-vindas! Por favor, leia nosso guia de contribuição.

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.
"""