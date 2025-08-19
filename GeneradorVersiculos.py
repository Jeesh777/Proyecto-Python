# -*- coding: utf-8 -*-
"""
Generador de Versículos Bíblicos
================================

Un programa interactivo para generar versículos bíblicos aleatorios
con funcionalidades avanzadas como historial, favoritos, y búsqueda por categorías.

Autor: Jeshua Salazar
Fecha: 2025
Version: 2.0
"""

import random
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import re

class GeneradorVersiculos:
    """Clase principal para manejar la generación y gestión de versículos bíblicos."""
    
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
        """Carga el historial de versículos desde un archivo JSON."""
        try:
            if os.path.exists(self.historial_archivo):
                with open(self.historial_archivo, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error al cargar historial: {e}")
        return []
    
    def _cargar_favoritos(self) -> List[Dict]:
        """Carga la lista de versículos favoritos desde un archivo JSON."""
        try:
            if os.path.exists(self.favoritos_archivo):
                with open(self.favoritos_archivo, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error al cargar favoritos: {e}")
        return []
    
    def _guardar_historial(self) -> None:
        """Guarda el historial en un archivo JSON."""
        try:
            with open(self.historial_archivo, 'w', encoding='utf-8') as f:
                json.dump(self.historial, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error al guardar historial: {e}")
    
    def _guardar_favoritos(self) -> None:
        """Guarda los favoritos en un archivo JSON."""
        try:
            with open(self.favoritos_archivo, 'w', encoding='utf-8') as f:
                json.dump(self.favoritos, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error al guardar favoritos: {e}")
    
    def obtener_versiculo_aleatorio(self, categoria: Optional[str] = None) -> Dict:
        """
        Obtiene un versículo aleatorio de una categoría específica o de todas.
        
        Args:
            categoria: Categoría específica o None para cualquier categoría
            
        Returns:
            Diccionario con el versículo, referencia y categoría
        """
        if categoria and categoria in self.versiculos:
            versiculo = random.choice(self.versiculos[categoria])
            versiculo['categoria'] = categoria
        else:
            categoria_elegida = random.choice(list(self.versiculos.keys()))
            versiculo = random.choice(self.versiculos[categoria_elegida])
            versiculo['categoria'] = categoria_elegida
        
        # Agregar TimeStamp
        versiculo['fecha'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Agrega al historial
        self.historial.append(versiculo.copy())
        if len(self.historial) > 100:  # Mantener solo los últimos 100
            self.historial = self.historial[-100:]
        self._guardar_historial()
        
        return versiculo
    
    def buscar_versiculos(self, termino: str) -> List[Dict]:
        """
        Busca versículos que contengan un término específico.
        
        Args:
            termino: Término a buscar en el texto del versículo
            
        Returns:
            Lista de versículos que contienen el término
        """
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
        """
        Agrega un versículo a la lista de favoritos.
        
        Args:
            versiculo: Diccionario con el versículo a agregar
            
        Returns:
            True si se agregó exitosamente, False si ya existía
        """
        # Verificar si ya existe
        for fav in self.favoritos:
            if (fav['texto'] == versiculo['texto'] and 
                fav['referencia'] == versiculo['referencia']):
                return False
        
        self.favoritos.append(versiculo)
        self._guardar_favoritos()
        return True
    
    def eliminar_favorito(self, indice: int) -> bool:
        """
        Elimina un versículo de la lista de favoritos.
        
        Args:
            indice: Índice del versículo a eliminar
            
        Returns:
            True si se eliminó exitosamente, False si el índice es inválido
        """
        if 0 <= indice < len(self.favoritos):
            self.favoritos.pop(indice)
            self._guardar_favoritos()
            return True
        return False
    
    def obtener_estadisticas(self) -> Dict:
        """
        Obtiene estadísticas sobre el uso del generador.
        
        Returns:
            Diccionario con estadísticas de uso
        """
        stats = {
            'total_versiculos_vistos': len(self.historial),
            'favoritos_guardados': len(self.favoritos),
            'categorias_disponibles': len(self.versiculos),
            'categoria_mas_vista': None,
            'ultimo_versiculo_visto': None
        }
        
        if self.historial:
            # Categoría más vista
            categorias_conteo = {}
            for item in self.historial:
                cat = item.get('categoria', 'desconocida')
                categorias_conteo[cat] = categorias_conteo.get(cat, 0) + 1
            
            if categorias_conteo:
                stats['categoria_mas_vista'] = max(categorias_conteo, key=categorias_conteo.get)
            
            stats['ultimo_versiculo_visto'] = self.historial[-1]['fecha']
        
        return stats

def mostrar_menu() -> None:
    """Muestra el menú principal de opciones."""
    print("\n" + "="*60)
    print("           🙏 GENERADOR DE VERSÍCULOS BÍBLICOS 🙏")
    print("="*60)
    print("1. 📖 Versículo aleatorio")
    print("2. 🎯 Versículo por categoría")
    print("3. 🔍 Buscar versículos")
    print("4. ⭐ Ver favoritos")
    print("5. 📚 Ver historial")
    print("6. 📊 Estadísticas")
    print("7. ❓ Ayuda")
    print("0. 🚪 Salir")
    print("="*60)

def mostrar_versiculo(versiculo: Dict) -> None:
    """
    Muestra un versículo de forma elegante.
    
    Args:
        versiculo: Diccionario con la información del versículo
    """
    print("\n" + "─"*50)
    print(f"📖 {versiculo['texto']}")
    print(f"   — {versiculo['referencia']} —")
    print(f"🏷️  Categoría: {versiculo.get('categoria', 'N/A').title()}")
    if 'fecha' in versiculo:
        print(f"🕐 Fecha: {versiculo['fecha']}")
    print("─"*50)

def mostrar_ayuda() -> None:
    """Muestra información de ayuda sobre el programa."""
    print("\n" + "="*60)
    print("                        📋 AYUDA")
    print("="*60)
    print("🔹 Versículo aleatorio: Obtiene un versículo al azar")
    print("🔹 Por categoría: Elige entre fortaleza, esperanza, consuelo, amor")
    print("🔹 Buscar: Encuentra versículos que contengan palabras específicas")
    print("🔹 Favoritos: Guarda y administra tus versículos preferidos")
    print("🔹 Historial: Ve los últimos versículos que has consultado")
    print("🔹 Estadísticas: Información sobre tu uso del programa")
    print("\n💡 Tip: Todos los datos se guardan automáticamente")
    print("="*60)

def main():
    """Función principal del programa."""
    generador = GeneradorVersiculos()
    
    print("🌟 ¡Bienvenido al Generador de Versículos Bíblicos! 🌟")
    
    while True:
        mostrar_menu()
        
        try:
            opcion = input("\n👉 Selecciona una opción: ").strip()
            
            if opcion == "0":
                print("\n🙏 ¡Que Dios te bendiga! Hasta luego.")
                break
            
            elif opcion == "1":
                versiculo = generador.obtener_versiculo_aleatorio()
                mostrar_versiculo(versiculo)
                
                # Opción de agregar a favoritos
                agregar = input("\n⭐ ¿Agregar a favoritos? (s/n): ").strip().lower()
                if agregar == 's':
                    if generador.agregar_favorito(versiculo):
                        print("✅ Agregado a favoritos!")
                    else:
                        print("ℹ️  Ya está en favoritos.")
            
            elif opcion == "2":
                print("\n🎯 Categorías disponibles:")
                categorias = list(generador.versiculos.keys())
                for i, cat in enumerate(categorias, 1):
                    print(f"{i}. {cat.title()}")
                
                try:
                    cat_opcion = int(input("\nSelecciona categoría (número): ")) - 1
                    if 0 <= cat_opcion < len(categorias):
                        categoria = categorias[cat_opcion]
                        versiculo = generador.obtener_versiculo_aleatorio(categoria)
                        mostrar_versiculo(versiculo)
                        
                        agregar = input("\n⭐ ¿Agregar a favoritos? (s/n): ").strip().lower()
                        if agregar == 's':
                            if generador.agregar_favorito(versiculo):
                                print("✅ Agregado a favoritos!")
                            else:
                                print("ℹ️  Ya está en favoritos.")
                    else:
                        print("❌ Opción inválida.")
                except ValueError:
                    print("❌ Por favor, ingresa un número válido.")
            
            elif opcion == "3":
                termino = input("\n🔍 Ingresa el término a buscar: ").strip()
                if termino:
                    resultados = generador.buscar_versiculos(termino)
                    if resultados:
                        print(f"\n🎯 Se encontraron {len(resultados)} resultados:")
                        for i, versiculo in enumerate(resultados, 1):
                            print(f"\n{i}.")
                            mostrar_versiculo(versiculo)
                    else:
                        print("❌ No se encontraron versículos con ese término.")
                else:
                    print("❌ Por favor, ingresa un término de búsqueda.")
            
            elif opcion == "4":
                if generador.favoritos:
                    print(f"\n⭐ Tus favoritos ({len(generador.favoritos)}):")
                    for i, versiculo in enumerate(generador.favoritos, 1):
                        print(f"\n{i}.")
                        mostrar_versiculo(versiculo)
                    
                    # Opción de eliminar favorito
                    eliminar = input("\n🗑️  ¿Eliminar algún favorito? (número o 'n'): ").strip()
                    if eliminar.isdigit():
                        indice = int(eliminar) - 1
                        if generador.eliminar_favorito(indice):
                            print("✅ Favorito eliminado.")
                        else:
                            print("❌ Número inválido.")
                else:
                    print("\n💭 No tienes favoritos guardados aún.")
            
            elif opcion == "5":
                if generador.historial:
                    print(f"\n📚 Historial (últimos 10):")
                    for i, versiculo in enumerate(generador.historial[-10:], 1):
                        print(f"\n{i}.")
                        mostrar_versiculo(versiculo)
                else:
                    print("\n💭 No hay historial disponible.")
            
            elif opcion == "6":
                stats = generador.obtener_estadisticas()
                print("\n📊 ESTADÍSTICAS")
                print("="*40)
                print(f"📖 Total de versículos vistos: {stats['total_versiculos_vistos']}")
                print(f"⭐ Favoritos guardados: {stats['favoritos_guardados']}")
                print(f"🏷️  Categorías disponibles: {stats['categorias_disponibles']}")
                if stats['categoria_mas_vista']:
                    print(f"🎯 Categoría más vista: {stats['categoria_mas_vista'].title()}")
                if stats['ultimo_versiculo_visto']:
                    print(f"🕐 Último versículo visto: {stats['ultimo_versiculo_visto']}")
                print("="*40)
            
            elif opcion == "7":
                mostrar_ayuda()
            
            else:
                print("❌ Opción no válida. Por favor, selecciona un número del menú.")
        
        except KeyboardInterrupt:
            print("\n\n🙏 ¡Que Dios te bendiga! Hasta luego.")
            break
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
        
        input("\n📱 Presiona Enter para continuar...")

if __name__ == "__main__":
    main()