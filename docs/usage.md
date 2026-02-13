# Guia de Uso - Sistema de Mapeamento de Entrega de Refeições

## Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/Cataldir/teste-criacao-copilot.git
cd teste-criacao-copilot
```

2. Crie um ambiente virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Estrutura do Projeto

```
teste-criacao-copilot/
├── src/                    # Código fonte
│   ├── __init__.py
│   ├── optimization/       # Módulo de otimização espacial
│   │   ├── __init__.py
│   │   ├── solver.py       # Algoritmos de otimização
│   │   └── models.py       # Modelos de dados
│   ├── data/              # Processamento de dados
│   │   ├── __init__.py
│   │   └── loader.py       # Carregamento de dados
│   └── utils/             # Utilitários
│       ├── __init__.py
│       └── geo.py          # Funções geoespaciais
├── docs/                  # Documentação
│   ├── architecture.md    # Arquitetura do sistema
│   └── usage.md          # Este arquivo
├── tests/                # Testes (futuro)
├── examples/             # Exemplos de uso (futuro)
├── requirements.txt      # Dependências Python
└── README.md            # Visão geral do projeto
```

## Uso Básico

### 1. Preparação dos Dados

Prepare seus dados de entrada no formato esperado:

```python
from src.data.loader import DataLoader

# Carregar dados de escolas
loader = DataLoader()
schools = loader.load_schools_from_csv('path/to/schools.csv')
```

### 2. Configurar o Modelo de Otimização

```python
from src.optimization.solver import OptimizationSolver

# Criar instância do solver
solver = OptimizationSolver()

# Configurar parâmetros
solver.configure(
    max_distance=50,  # km
    vehicle_capacity=100,  # refeições por veículo
    time_window=(7, 12)  # janela de entrega (7h-12h)
)
```

### 3. Executar a Otimização

```python
# Executar otimização
results = solver.optimize(schools)

# Visualizar resultados
print(f"Rotas otimizadas: {results['num_routes']}")
print(f"Distância total: {results['total_distance']} km")
print(f"Custo estimado: R$ {results['estimated_cost']}")
```

### 4. Exportar Resultados

```python
# Exportar resultados
import json

# Obter resultados em formato serializável
export_data = solver.export_results()

# Salvar em arquivo JSON
with open('output/routes.json', 'w', encoding='utf-8') as f:
    json.dump(export_data, f, indent=2, ensure_ascii=False)

# Imprimir informações das rotas
for route in results['routes']:
    print(f"Rota {route.route_id}: {len(route.schools)} escolas, {route.total_distance:.2f}km")
```

## Formato de Dados de Entrada

### Arquivo de Escolas (CSV)

```csv
id,nome,latitude,longitude,num_alunos,nivel_ensino
1,Escola A,-23.550520,-46.633308,500,fundamental_ii
2,Escola B,-23.561684,-46.656139,450,medio
3,Escola C,-23.533773,-46.625290,600,fundamental_ii
```

Campos obrigatórios:
- `id`: Identificador único da escola
- `nome`: Nome da escola
- `latitude`: Latitude da localização
- `longitude`: Longitude da localização
- `num_alunos`: Número de alunos
- `nivel_ensino`: Nível de ensino (fundamental_ii, medio)

## Exemplos Avançados

Para exemplos mais avançados e casos de uso específicos, consulte a pasta `examples/` (a ser desenvolvida).

## Solução de Problemas

### Erro: "No solution found"

Possíveis causas:
- Restrições muito rígidas
- Dados de entrada inválidos
- Capacidade insuficiente

Solução: Ajuste os parâmetros de configuração ou verifique os dados de entrada.

### Erro: "Invalid coordinates"

Certifique-se de que as coordenadas estão no formato correto (decimal) e dentro dos limites geográficos do estado de São Paulo.

## Suporte

Para dúvidas ou problemas, abra uma issue no repositório GitHub.
