"""
Módulo de otimização espacial para roteamento de entrega de refeições
"""

from .solver import OptimizationSolver
from .models import School, DeliveryRoute, OptimizationConfig

__all__ = ['OptimizationSolver', 'School', 'DeliveryRoute', 'OptimizationConfig']
