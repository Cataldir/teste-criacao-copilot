# Sistema de Mapeamento de Entrega de Refeições

Um sistema de otimização espacial para mapear e otimizar a entrega de refeições para alunos de escolas públicas do estado de São Paulo, cobrindo do segundo nível do ensino fundamental até o ensino médio.

## 📋 Descrição

Este projeto implementa um modelo de otimização espacial que:
- Determina rotas eficientes de entrega de refeições
- Minimiza distâncias e custos de transporte
- Maximiza a cobertura de atendimento às escolas
- Agrupa escolas próximas para otimizar recursos

## 🚀 Início Rápido

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

```bash
# Clone o repositório
git clone https://github.com/Cataldir/teste-criacao-copilot.git
cd teste-criacao-copilot

# Crie um ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt
```

### Uso Básico

```python
from src.optimization import OptimizationSolver, School
from src.data import DataLoader

# Carregar dados de escolas
loader = DataLoader()
schools = loader.load_schools_from_csv('data/schools.csv')

# Criar e configurar o solver
solver = OptimizationSolver()
solver.configure(
    max_distance=50,  # km
    vehicle_capacity=100  # refeições por veículo
)

# Executar otimização
results = solver.optimize(schools)

# Visualizar resultados
print(f"Rotas otimizadas: {results['num_routes']}")
print(f"Distância total: {results['total_distance']:.2f} km")
print(f"Custo estimado: R$ {results['estimated_cost']:.2f}")
```

## 📁 Estrutura do Projeto

```
teste-criacao-copilot/
├── src/                    # Código fonte
│   ├── optimization/       # Módulo de otimização espacial
│   ├── data/              # Processamento de dados
│   └── utils/             # Utilitários geoespaciais
├── docs/                  # Documentação
│   ├── architecture.md    # Arquitetura do sistema
│   └── usage.md          # Guia de uso detalhado
├── requirements.txt       # Dependências Python
└── README.md             # Este arquivo
```

## 📚 Documentação

Para mais informações, consulte:
- [Arquitetura do Sistema](docs/architecture.md)
- [Guia de Uso Detalhado](docs/usage.md)

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor, abra uma issue ou pull request.

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## ✍️ Autor

Ricardo Cataldi

## 🙏 Agradecimentos

Desenvolvido para otimizar a entrega de refeições nas escolas públicas do estado de São Paulo.
