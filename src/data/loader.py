"""
Carregador de dados para o sistema de otimização
"""

import csv
from typing import List, Dict, Any
from pathlib import Path
from ..optimization.models import School


class DataLoader:
    """
    Classe para carregar dados de escolas de diferentes fontes
    """
    
    @staticmethod
    def load_schools_from_csv(filepath: str) -> List[School]:
        """
        Carrega dados de escolas de um arquivo CSV
        
        Args:
            filepath: Caminho para o arquivo CSV
        
        Returns:
            Lista de objetos School
        
        Raises:
            FileNotFoundError: Se o arquivo não for encontrado
            ValueError: Se o formato do arquivo for inválido
        """
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")
        
        schools = []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            required_fields = ['id', 'nome', 'latitude', 'longitude', 'num_alunos', 'nivel_ensino']
            
            for row_num, row in enumerate(reader, start=2):
                # Verificar campos obrigatórios
                missing_fields = [field for field in required_fields if field not in row]
                if missing_fields:
                    raise ValueError(
                        f"Linha {row_num}: Campos obrigatórios ausentes: {missing_fields}"
                    )
                
                try:
                    school = School(
                        id=int(row['id']),
                        name=row['nome'].strip(),
                        latitude=float(row['latitude']),
                        longitude=float(row['longitude']),
                        num_students=int(row['num_alunos']),
                        education_level=row['nivel_ensino'].strip()
                    )
                    
                    if not school.validate():
                        raise ValueError(f"Dados inválidos para escola ID {school.id}")
                    
                    schools.append(school)
                    
                except (ValueError, KeyError) as e:
                    raise ValueError(f"Linha {row_num}: Erro ao processar dados - {e}")
        
        return schools
    
    @staticmethod
    def load_schools_from_dict(data: List[Dict[str, Any]]) -> List[School]:
        """
        Carrega dados de escolas de uma lista de dicionários
        
        Args:
            data: Lista de dicionários com dados de escolas
        
        Returns:
            Lista de objetos School
        
        Raises:
            ValueError: Se os dados forem inválidos
        """
        schools = []
        
        for idx, item in enumerate(data):
            try:
                school = School(
                    id=item['id'],
                    name=item['name'],
                    latitude=item['latitude'],
                    longitude=item['longitude'],
                    num_students=item['num_students'],
                    education_level=item['education_level']
                )
                
                if not school.validate():
                    raise ValueError(f"Dados inválidos para escola ID {school.id}")
                
                schools.append(school)
                
            except (KeyError, TypeError) as e:
                raise ValueError(f"Item {idx}: Erro ao processar dados - {e}")
        
        return schools
    
    @staticmethod
    def export_schools_to_csv(schools: List[School], filepath: str) -> None:
        """
        Exporta dados de escolas para um arquivo CSV
        
        Args:
            schools: Lista de objetos School
            filepath: Caminho para o arquivo CSV de saída
        """
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            fieldnames = ['id', 'nome', 'latitude', 'longitude', 'num_alunos', 'nivel_ensino']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            writer.writeheader()
            
            for school in schools:
                writer.writerow({
                    'id': school.id,
                    'nome': school.name,
                    'latitude': school.latitude,
                    'longitude': school.longitude,
                    'num_alunos': school.num_students,
                    'nivel_ensino': school.education_level
                })
