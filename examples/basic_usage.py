"""
Exemplo básico de uso do sistema de otimização de entrega de refeições
"""

import sys
from pathlib import Path

# Adicionar diretório raiz ao path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from src.optimization import OptimizationSolver, School


def main():
    """
    Exemplo de uso do sistema com dados simulados de escolas de São Paulo
    """
    
    # Criar dados de exemplo para escolas na região de São Paulo
    schools = [
        School(
            id=1,
            name="EMEF Prof. João Silva",
            latitude=-23.550520,
            longitude=-46.633308,
            num_students=450,
            education_level="fundamental_ii"
        ),
        School(
            id=2,
            name="EE Maria Santos",
            latitude=-23.561684,
            longitude=-46.656139,
            num_students=520,
            education_level="medio"
        ),
        School(
            id=3,
            name="EMEF Antonio Carlos",
            latitude=-23.533773,
            longitude=-46.625290,
            num_students=380,
            education_level="fundamental_ii"
        ),
        School(
            id=4,
            name="EE Pedro Alvares",
            latitude=-23.574234,
            longitude=-46.640165,
            num_students=490,
            education_level="medio"
        ),
        School(
            id=5,
            name="EMEF Ana Paula",
            latitude=-23.545123,
            longitude=-46.618745,
            num_students=410,
            education_level="fundamental_ii"
        ),
    ]
    
    print("=" * 70)
    print("Sistema de Otimização de Entrega de Refeições")
    print("Escolas Públicas do Estado de São Paulo")
    print("=" * 70)
    print()
    
    print(f"📚 Total de escolas: {len(schools)}")
    print(f"👨‍🎓 Total de alunos: {sum(s.num_students for s in schools)}")
    print()
    
    # Criar e configurar o solver
    solver = OptimizationSolver()
    solver.configure(
        max_distance=50.0,  # km
        vehicle_capacity=1000,  # refeições por veículo
        time_window=(7, 12)  # janela de entrega: 7h às 12h
    )
    
    print("⚙️  Configuração do Solver:")
    print(f"   - Distância máxima por rota: {solver.config.max_distance} km")
    print(f"   - Capacidade do veículo: {solver.config.vehicle_capacity} refeições")
    print(f"   - Janela de entrega: {solver.config.time_window[0]}h às {solver.config.time_window[1]}h")
    print()
    
    # Executar otimização
    print("🔄 Executando otimização...")
    results = solver.optimize(schools)
    print("✅ Otimização concluída!")
    print()
    
    # Exibir resultados
    print("=" * 70)
    print("RESULTADOS DA OTIMIZAÇÃO")
    print("=" * 70)
    print()
    print(f"📊 Estatísticas Gerais:")
    print(f"   - Número de rotas: {results['num_routes']}")
    print(f"   - Distância total: {results['total_distance']:.2f} km")
    print(f"   - Distância média por rota: {results['average_route_distance']:.2f} km")
    print(f"   - Total de refeições: {results['total_meals']}")
    print(f"   - Escolas atendidas: {results['schools_served']}")
    print(f"   - Custo estimado: R$ {results['estimated_cost']:.2f}")
    print()
    
    # Detalhar cada rota
    print("=" * 70)
    print("DETALHAMENTO DAS ROTAS")
    print("=" * 70)
    
    for route in results['routes']:
        print()
        print(f"🚚 Rota {route.route_id}:")
        print(f"   - Escolas: {len(route.schools)}")
        print(f"   - Distância: {route.total_distance:.2f} km")
        print(f"   - Refeições: {route.total_meals}")
        print(f"   - Tempo estimado: {route.estimated_time} minutos")
        print(f"   - Escolas na rota:")
        for school in route.schools:
            print(f"      • {school.name} ({school.num_students} alunos)")
    
    print()
    print("=" * 70)
    print("Otimização concluída com sucesso!")
    print("=" * 70)


if __name__ == "__main__":
    main()
