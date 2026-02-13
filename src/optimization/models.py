"""
Modelos de dados para o sistema de otimização
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass
class School:
    """
    Representa uma escola no sistema de entrega de refeições
    
    Attributes:
        id: Identificador único da escola
        name: Nome da escola
        latitude: Latitude da localização
        longitude: Longitude da localização
        num_students: Número de alunos
        education_level: Nível de ensino (fundamental_ii, medio)
    """
    id: int
    name: str
    latitude: float
    longitude: float
    num_students: int
    education_level: str
    
    def coordinates(self) -> Tuple[float, float]:
        """Retorna as coordenadas como tupla (latitude, longitude)"""
        return (self.latitude, self.longitude)
    
    def validate(self) -> bool:
        """Valida os dados da escola"""
        # Validar coordenadas de São Paulo (aproximadamente)
        if not (-25.0 <= self.latitude <= -20.0):
            return False
        if not (-54.0 <= self.longitude <= -44.0):
            return False
        if self.num_students <= 0:
            return False
        if self.education_level not in ['fundamental_ii', 'medio']:
            return False
        return True


@dataclass
class DeliveryRoute:
    """
    Representa uma rota de entrega otimizada
    
    Attributes:
        route_id: Identificador da rota
        schools: Lista de escolas na rota
        total_distance: Distância total em km
        total_meals: Total de refeições a entregar
        estimated_time: Tempo estimado de entrega em minutos
    """
    route_id: int
    schools: List[School]
    total_distance: float
    total_meals: int
    estimated_time: int
    
    def __str__(self) -> str:
        return f"Rota {self.route_id}: {len(self.schools)} escolas, {self.total_distance:.2f}km, {self.total_meals} refeições"


@dataclass
class OptimizationConfig:
    """
    Configuração para o algoritmo de otimização
    
    Attributes:
        max_distance: Distância máxima por rota em km
        vehicle_capacity: Capacidade máxima de refeições por veículo
        time_window: Janela de tempo para entrega (início, fim) em horas
        depot_location: Localização do depósito/centro de distribuição (lat, lon)
    """
    max_distance: float = 100.0
    vehicle_capacity: int = 500
    time_window: Tuple[int, int] = (7, 12)
    depot_location: Optional[Tuple[float, float]] = None
    
    def validate(self) -> bool:
        """Valida a configuração"""
        if self.max_distance <= 0:
            return False
        if self.vehicle_capacity <= 0:
            return False
        if self.time_window[0] >= self.time_window[1]:
            return False
        return True
