# -*- coding: utf-8 -*-
"""
Aliento para vivir un dia más
================================

Un programa interactivo para generar versículos bíblicos aleatorios
con funcionalidades avanzadas como historial, favoritos, y búsqueda por categorías.
Usado no solo como un proyecto más, sino también como un alivio o respiro en momentos
dificiles, ansiedad durante el trabajo o depresión. 

Autor: Jeshua Salazar
Fecha: 2025
Version: 1.5
"""

import random
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import re



class GeneradorVersiculos:

    def __init__(self):
        self.versiculos = {
            "fortaleza": [
                {"texto": "Todo lo puedo en Cristo que me fortalece.", "referencia": "Filipenses 4:13"},
                {"texto": "Esfuérzate y sé valiente; no temas ni desmayes, porque Jehová tu Dios estará contigo.", "referencia": "Josué 1:9"},
                {"texto": "Jehová es mi fortaleza y mi cántico, y ha sido mi salvación.", "referencia": "Éxodo 15:2"}
            ],
            "esperanza": [
                {"texto": "Porque yo sé los pensamientos que tengo acerca de vosotros, pensamientos de paz, y no de mal.", "referencia": "Jeremías 29:11"},
                {"texto": "Mas a Jehová esperaré, al Dios de mi salvación; el Dios mío me oirá.", "referencia": "Miqueas 7:7"},
                {"texto": "La esperanza que se demora es tormento del corazón; pero árbol de vida es el deseo cumplido.", "referencia": "Proverbios 13:12"}
            ],
            "consuelo": [
                {"texto": "No temas, porque yo estoy contigo; no desmayes, porque yo soy tu Dios que te fortalezco.", "referencia": "Isaías 41:10"},
                {"texto": "Venid a mí todos los que estáis trabajados y cargados, y yo os haré descansar.", "referencia": "Mateo 11:28"},
                {"texto": "Jehová está cerca de los quebrantados de corazón; y salva a los contritos de espíritu.", "referencia": "Salmos 34:18"}
            ],
            "amor": [
                {"texto": "Porque de tal manera amó Dios al mundo, que ha dado a su Hijo unigénito.", "referencia": "Juan 3:16"},
                {"texto": "Y sabemos que a los que aman a Dios, todas las cosas les ayudan a bien.", "referencia": "Romanos 8:28"},
                {"texto": "El amor es sufrido, es benigno; el amor no tiene envidia.", "referencia": "1 Corintios 13:4"}
            ]
        }
        
        self.historial_archivo = "historial_versiculos.json"
        self.favoritos_archivo = "favoritos_versiculos.json"
        self.historial = self._cargar_historial()
        self.favoritos = self._cargar_favoritos()
    
    def _cargar_historial(self) -> List[Dict]:
        try:
            if os.path.exists(self.historial_archivo):
                with open(self.historial_archivo, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error al cargar historial: {e}")
        return []
    
    def _cargar_favoritos(self) -> List[Dict]:
        try:
            if os.path.exists(self.favoritos_archivo):
                with open(self.favoritos_archivo, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error al cargar favoritos: {e}")
        return []
    
    def _guardar_historial(self) -> None:
        try:
            with open(self.historial_archivo, 'w', encoding='utf-8') as f:
                json.dump(self.historial, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error al guardar historial: {e}")
    
    def _guardar_favoritos(self) -> None:
        try:
            with open(self.favoritos_archivo, 'w', encoding='utf-8') as f:
                json.dump(self.favoritos, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error al guardar favoritos: {e}")
    
    def obtener_versiculo_aleatorio(self, categoria: Optional[str] = None) -> Dict:
        if categoria and categoria in self.versiculos:
            versiculo = random.choice(self.versiculos[categoria])
            versiculo['categoria'] = categoria
        else:
            categoria_elegida = random.choice(list(self.versiculos.keys()))
            versiculo = random.choice(self.versiculos[categoria_elegida])
            versiculo['categoria'] = categoria_elegida
        
        versiculo['fecha'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.historial.append(versiculo.copy())
        if len(self.historial) > 100:
            self.historial = self.historial[-100:]
        self._guardar_historial()
        
        return versiculo
    
    def buscar_versiculos(self, termino: str) -> List[Dict]:
        resultados = []
        termino_lower = termino.lower()
        
        for categoria, versiculos in self.versiculos.items():
            for versiculo in versiculos:
                if (termino_lower in versiculo['texto'].lower() or 
                    termino_lower in versiculo['referencia'].lower()):
                    resultado = versiculo.copy()
                    resultado['categoria'] = categoria
                    resultados.append(resultado)
        
        return resultados
    
    def agregar_favorito(self, versiculo: Dict) -> bool:
        for fav in self.favoritos:
            if (fav['texto'] == versiculo['texto'] and 
                fav['referencia'] == versiculo['referencia']):
                return False
        
        self.favoritos.append(versiculo)
        self._guardar_favoritos()
        return True
    
    def eliminar_favorito(self, indice: int) -> bool:
        if 0 <= indice < len(self.favoritos):
            self.favoritos.pop(indice)
            self._guardar_favoritos()
            return True
        return False
    
    def obtener_estadisticas(self) -> Dict:
        stats = {
            'total_versiculos_vistos': len(self.historial),
            'favoritos_guardados': len(self.favoritos),
            'categorias_disponibles': len(self.versiculos),
            'categoria_mas_vista': None,
            'ultimo_versiculo_visto': None
        }
        
        if self.historial:
            categorias_conteo = {}
            for item in self.historial:
                cat = item.get('categoria', 'desconocida')
                categorias_conteo[cat] = categorias_conteo.get(cat, 0) + 1
            
            if categorias_conteo:
                stats['categoria_mas_vista'] = max(categorias_conteo, key=categorias_conteo.get)
            
            stats['ultimo_versiculo_visto'] = self.historial[-1]['fecha']
        
        return stats

