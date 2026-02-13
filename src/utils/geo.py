"""
Funções utilitárias geoespaciais
"""

import math
from typing import List, Tuple


def calculate_distance(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    """
    Calcula a distância entre duas coordenadas geográficas usando a fórmula de Haversine
    
    Args:
        coord1: Tupla (latitude, longitude) do ponto 1
        coord2: Tupla (latitude, longitude) do ponto 2
    
    Returns:
        Distância em quilômetros
    
    Example:
        >>> coord1 = (-23.550520, -46.633308)  # São Paulo
        >>> coord2 = (-22.906847, -43.172896)  # Rio de Janeiro
        >>> distance = calculate_distance(coord1, coord2)
        >>> print(f"{distance:.2f} km")
    """
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    # Raio da Terra em km
    R = 6371.0
    
    # Converter para radianos
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    # Fórmula de Haversine
    a = (math.sin(delta_lat / 2)**2 + 
         math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c
    return distance


def calculate_centroid(coordinates: List[Tuple[float, float]]) -> Tuple[float, float]:
    """
    Calcula o centroide (ponto médio) de um conjunto de coordenadas
    
    Args:
        coordinates: Lista de tuplas (latitude, longitude)
    
    Returns:
        Tupla (latitude, longitude) do centroide
    
    Raises:
        ValueError: Se a lista de coordenadas estiver vazia
    
    Example:
        >>> coords = [(-23.5, -46.6), (-23.6, -46.7), (-23.4, -46.5)]
        >>> centroid = calculate_centroid(coords)
        >>> print(f"Centroide: {centroid}")
    """
    if not coordinates:
        raise ValueError("Lista de coordenadas não pode estar vazia")
    
    lat_sum = sum(lat for lat, _ in coordinates)
    lon_sum = sum(lon for _, lon in coordinates)
    
    n = len(coordinates)
    centroid = (lat_sum / n, lon_sum / n)
    
    return centroid


def is_valid_coordinate(latitude: float, longitude: float, 
                       region: str = 'sao_paulo') -> bool:
    """
    Verifica se uma coordenada é válida para uma região específica
    
    Args:
        latitude: Latitude da coordenada
        longitude: Longitude da coordenada
        region: Região para validação ('sao_paulo', 'brazil', 'world')
    
    Returns:
        True se a coordenada é válida, False caso contrário
    
    Example:
        >>> is_valid_coordinate(-23.550520, -46.633308, 'sao_paulo')
        True
        >>> is_valid_coordinate(0, 0, 'sao_paulo')
        False
    """
    # Limites gerais de coordenadas
    if not (-90 <= latitude <= 90):
        return False
    if not (-180 <= longitude <= 180):
        return False
    
    # Limites específicos por região
    if region == 'sao_paulo':
        # Aproximação dos limites do estado de São Paulo
        if not (-25.5 <= latitude <= -19.8):
            return False
        if not (-53.2 <= longitude <= -44.2):
            return False
    elif region == 'brazil':
        # Limites aproximados do Brasil
        if not (-34.0 <= latitude <= 5.3):
            return False
        if not (-74.0 <= longitude <= -28.8):
            return False
    # 'world' já foi validado acima
    
    return True


def calculate_bearing(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    """
    Calcula o rumo (bearing) de coord1 para coord2
    
    Args:
        coord1: Tupla (latitude, longitude) do ponto inicial
        coord2: Tupla (latitude, longitude) do ponto final
    
    Returns:
        Rumo em graus (0-360), onde 0° é Norte, 90° é Leste, etc.
    
    Example:
        >>> coord1 = (-23.550520, -46.633308)
        >>> coord2 = (-23.551520, -46.633308)
        >>> bearing = calculate_bearing(coord1, coord2)
        >>> print(f"Rumo: {bearing:.2f}°")
    """
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    # Converter para radianos
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lon = math.radians(lon2 - lon1)
    
    # Calcular bearing
    x = math.sin(delta_lon) * math.cos(lat2_rad)
    y = (math.cos(lat1_rad) * math.sin(lat2_rad) - 
         math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(delta_lon))
    
    bearing_rad = math.atan2(x, y)
    bearing_deg = math.degrees(bearing_rad)
    
    # Normalizar para 0-360
    bearing_deg = (bearing_deg + 360) % 360
    
    return bearing_deg
