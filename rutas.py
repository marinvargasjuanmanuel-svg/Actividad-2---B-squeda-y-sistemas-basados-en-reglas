"""
Sistema Inteligente de Búsqueda de Rutas - TransMilenio
Encuentra la ruta óptima entre dos puntos
"""

import networkx as nx
import matplotlib.pyplot as plt

# ----------------------------------------------------------
# 1. CREAR GRAFO 
# ----------------------------------------------------------

G = nx.Graph()

# Agregar nodos (estaciones A-F)
G.add_nodes_from(["A", "B", "C", "D", "E", "F"])

# Agregar conexiones con pesos (tiempos en minutos)
G.add_edge("A", "C", weight=3)
G.add_edge("A", "E", weight=3)
G.add_edge("A", "B", weight=2)
G.add_edge("C", "E", weight=2)
G.add_edge("C", "D", weight=2)
G.add_edge("D", "E", weight=2)
G.add_edge("D", "F", weight=1)
G.add_edge("E", "F", weight=3)

# ----------------------------------------------------------
# 2. REGLAS DEL SISTEMA EXPERTO
# ----------------------------------------------------------

def regla_ruta_larga(costo):
    """Si el costo es mayor a 5, advertir"""
    return costo > 5

def regla_muchos_saltos(num_paradas):
    """Si hay más de 3 paradas, sugerir alternativa"""
    return num_paradas > 3

# ----------------------------------------------------------
# 3. MOTOR DE INFERENCIA
# ----------------------------------------------------------

def motor_inferencia(ruta, costo):
    """Evalúa las reglas y da recomendaciones"""
    mensajes = []
    
    num_paradas = len(ruta) - 1
    
    if regla_ruta_larga(costo):
        mensajes.append("⚠️ Ruta con tiempo alto. Verificar alternativas.")
    
    if regla_muchos_saltos(num_paradas):
        mensajes.append("ℹ️ Ruta con muchas paradas. Puede haber ruta más directa.")
    
    if not mensajes:
        mensajes.append("✅ Ruta óptima encontrada.")
    
    return mensajes

# ----------------------------------------------------------
# 4. CALCULAR MEJOR RUTA
# ----------------------------------------------------------

def calcular_ruta(origen, destino):
    """
    Encuentra la ruta con menor tiempo entre origen y destino
    """
    print("=" * 60)
    print(f"🚍 Buscando ruta: {origen} → {destino}")
    print("=" * 60)
    
    try:
        # Usar Dijkstra para encontrar ruta más corta
        ruta = nx.shortest_path(G, origen, destino, weight="weight")
        costo = nx.shortest_path_length(G, origen, destino, weight="weight")
        
        # Mostrar resultados
        print(f"\n✅ Ruta encontrada: {' → '.join(ruta)}")
        print(f"⏱️  Tiempo total: {costo} minutos")
        
        # Aplicar motor de inferencia
        print(f"\n🧠 Evaluando reglas del sistema experto...")
        recomendaciones = motor_inferencia(ruta, costo)
        
        for rec in recomendaciones:
            print(f"   {rec}")
        
        print("=" * 60 + "\n")
        
        return ruta, costo
        
    except nx.NodeNotFound:
        print("❌ ERROR: Estación no existe\n")
        return None, None
    except nx.NetworkXNoPath:
        print("❌ ERROR: No hay ruta entre estas estaciones\n")
        return None, None

# ----------------------------------------------------------
# 5. VISUALIZAR GRAFO
# ----------------------------------------------------------

def visualizar_grafo(ruta_destacada=None):
    """Dibuja el grafo del sistema"""
    plt.figure(figsize=(10, 8))
    
    # Posiciones de los nodos (según tu imagen)
    pos = {
        'C': (2, 4),
        'A': (0, 2),
        'D': (4, 2),
        'E': (2, 1),
        'B': (0, 0),
        'F': (4, 0)
    }
    
    # Dibujar todas las aristas
    nx.draw_networkx_edges(G, pos, width=2, alpha=0.5)
    
    # Destacar ruta si existe
    if ruta_destacada:
        aristas_ruta = [(ruta_destacada[i], ruta_destacada[i+1]) 
                       for i in range(len(ruta_destacada)-1)]
        nx.draw_networkx_edges(G, pos, aristas_ruta, 
                              edge_color='green', width=5)
    
    # Dibujar nodos
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
                          node_size=2000, edgecolors='black', linewidths=2)
    
    # Etiquetas de nodos
    nx.draw_networkx_labels(G, pos, font_size=16, font_weight='bold')
    
    # Etiquetas de pesos (tiempos)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=12)
    
    plt.title("Sistema TransMilenio - Red de Estaciones", 
              fontsize=14, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.show()

# ----------------------------------------------------------
# 6. EJECUTAR
# ----------------------------------------------------------

if __name__ == "__main__":
    
    print("\n🚍 SISTEMA TRANSMILENIO")
    print("Estaciones disponibles: A, B, C, D, E, F\n")
    
    # Prueba 1: A → F
    print("\n📍 PRUEBA 1:")
    ruta1, _ = calcular_ruta("A", "F")
    
    # Prueba 2: A → C
    print("\n📍 PRUEBA 2:")
    ruta2, _ = calcular_ruta("A", "C")
    
    # Prueba 3: B → D
    print("\n📍 PRUEBA 3:")
    ruta3, _ = calcular_ruta("B", "D")
    
    # Mostrar grafo
    print("🎨 Generando visualización...")
    visualizar_grafo()
    
    # Mostrar grafo con ruta A → F destacada
    if ruta1:
        print("🎨 Mostrando ruta A → F destacada...")
        visualizar_grafo(ruta_destacada=ruta1)
    
    print("✅ Fin de ejecución\n")