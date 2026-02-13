"""
Solver de otimização espacial para roteamento de entrega de refeições
"""

from typing import List, Dict, Any, Optional
from .models import School, DeliveryRoute, OptimizationConfig
from ..utils.geo import calculate_distance


class OptimizationSolver:
    """
    Classe principal para resolver problemas de otimização de roteamento
    de entrega de refeições para escolas
    """
    
    def __init__(self, config: Optional[OptimizationConfig] = None):
        """
        Inicializa o solver com uma configuração
        
        Args:
            config: Configuração de otimização (usa padrão se não fornecida)
        """
        self.config = config or OptimizationConfig()
        self.schools: List[School] = []
        self.routes: List[DeliveryRoute] = []
    
    def configure(self, **kwargs) -> None:
        """
        Atualiza a configuração do solver
        
        Args:
            **kwargs: Parâmetros de configuração a serem atualizados
        """
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
    
    def load_schools(self, schools: List[School]) -> None:
        """
        Carrega a lista de escolas a serem atendidas
        
        Args:
            schools: Lista de objetos School
        
        Raises:
            ValueError: Se alguma escola tiver dados inválidos
        """
        invalid_schools = [s for s in schools if not s.validate()]
        if invalid_schools:
            raise ValueError(f"Escolas com dados inválidos: {[s.id for s in invalid_schools]}")
        
        self.schools = schools
    
    
    def _cluster_schools(self) -> List[List[School]]:
        """
        Agrupa escolas próximas usando clustering simples baseado em distância
        
        Returns:
            Lista de clusters (cada cluster é uma lista de escolas)
        """
        if not self.schools:
            return []
        
        # Implementação simples de clustering para demonstração
        # Em produção, usar algoritmos mais sofisticados (K-means, DBSCAN, etc.)
        clusters = []
        remaining_schools = self.schools.copy()
        
        while remaining_schools:
            # Iniciar novo cluster com primeira escola restante
            current_cluster = [remaining_schools.pop(0)]
            current_meals = current_cluster[0].num_students
            
            # Adicionar escolas próximas ao cluster
            i = 0
            while i < len(remaining_schools):
                school = remaining_schools[i]
                
                # Verificar se escola pode ser adicionada ao cluster
                if current_meals + school.num_students <= self.config.vehicle_capacity:
                    # Verificar distância ao cluster
                    cluster_center = current_cluster[0]
                    distance = calculate_distance(
                        cluster_center.coordinates(),
                        school.coordinates()
                    )
                    
                    if distance <= self.config.max_distance / 2:
                        current_cluster.append(school)
                        current_meals += school.num_students
                        remaining_schools.pop(i)
                        continue
                
                i += 1
            
            clusters.append(current_cluster)
        
        return clusters
    
    def optimize(self, schools: Optional[List[School]] = None) -> Dict[str, Any]:
        """
        Executa a otimização de rotas para as escolas fornecidas
        
        Args:
            schools: Lista de escolas (usa escolas já carregadas se não fornecida)
        
        Returns:
            Dicionário com resultados da otimização
        
        Raises:
            ValueError: Se não houver escolas para otimizar
        """
        if schools is not None:
            self.load_schools(schools)
        
        if not self.schools:
            raise ValueError("Nenhuma escola carregada para otimização")
        
        # Validar configuração
        if not self.config.validate():
            raise ValueError("Configuração inválida")
        
        # Agrupar escolas em clusters
        clusters = self._cluster_schools()
        
        # Criar rotas otimizadas para cada cluster
        self.routes = []
        total_distance = 0.0
        total_meals = 0
        
        for idx, cluster in enumerate(clusters, 1):
            # Calcular distância total do cluster (simplificado)
            cluster_distance = 0.0
            cluster_meals = sum(s.num_students for s in cluster)
            
            for i in range(len(cluster) - 1):
                distance = calculate_distance(
                    cluster[i].coordinates(),
                    cluster[i + 1].coordinates()
                )
                cluster_distance += distance
            
            # Estimar tempo de entrega (média de 15 min por escola + tempo de viagem)
            estimated_time = len(cluster) * 15 + int(cluster_distance * 2)  # 2 min por km
            
            route = DeliveryRoute(
                route_id=idx,
                schools=cluster,
                total_distance=cluster_distance,
                total_meals=cluster_meals,
                estimated_time=estimated_time
            )
            
            self.routes.append(route)
            total_distance += cluster_distance
            total_meals += cluster_meals
        
        # Calcular métricas
        results = {
            'num_routes': len(self.routes),
            'total_distance': total_distance,
            'total_meals': total_meals,
            'estimated_cost': total_distance * 5.0,  # R$ 5 por km (estimativa)
            'routes': self.routes,
            'average_route_distance': total_distance / len(self.routes) if self.routes else 0,
            'schools_served': len(self.schools)
        }
        
        return results
    
    def get_routes(self) -> List[DeliveryRoute]:
        """
        Retorna as rotas otimizadas
        
        Returns:
            Lista de rotas
        """
        return self.routes
    
    def export_results(self) -> Dict[str, Any]:
        """
        Exporta os resultados em formato serializável
        
        Returns:
            Dicionário com resultados exportáveis
        """
        return {
            'config': {
                'max_distance': self.config.max_distance,
                'vehicle_capacity': self.config.vehicle_capacity,
                'time_window': self.config.time_window
            },
            'routes': [
                {
                    'route_id': route.route_id,
                    'schools': [
                        {
                            'id': s.id,
                            'name': s.name,
                            'num_students': s.num_students
                        }
                        for s in route.schools
                    ],
                    'total_distance': route.total_distance,
                    'total_meals': route.total_meals,
                    'estimated_time': route.estimated_time
                }
                for route in self.routes
            ]
        }
