from flask import Flask, render_template, request, jsonify
import time

app = Flask(__name__)

# --- ESTADO DEL TAXÍMETRO (Sustituye la lógica del input) ---
taxi_data = {
    "activo": False,
    "estado": "parado", # 'parado' o 'movimiento'
    "tiempo_parado": 0,
    "tiempo_movimiento": 0,
    "ultima_marca_tiempo": 0
}

@app.route('/')
def index():
    # Esta función busca el archivo index.html en la carpeta 'templates'
    return render_template('index.html')

@app.route('/comando', methods=['POST'])
def comando():
    accion = request.json.get('accion')
    ahora = time.time()
    
    # 1. INICIAR TRAYECTO (Nivel Esencial)
    if accion == 'start':
        taxi_data["activo"] = True
        taxi_data["estado"] = "parado"
        taxi_data["tiempo_parado"] = 0
        taxi_data["tiempo_movimiento"] = 0
        taxi_data["ultima_marca_tiempo"] = ahora
        return jsonify({"status": "viaje_iniciado", "estado": "parado"})

    if taxi_data["activo"]:
        # Calcular cuánto tiempo pasó desde el último botón pulsado
        duracion = ahora - taxi_data["ultima_marca_tiempo"]
        
        if taxi_data["estado"] == "parado":
            taxi_data["tiempo_parado"] += duracion
        else:
            taxi_data["tiempo_movimiento"] += duracion
        
        taxi_data["ultima_marca_tiempo"] = ahora

        # 2. CAMBIAR ESTADOS (Stop / Move)
        if accion == 'stop':
            taxi_data["estado"] = "parado"
        elif accion == 'move':
            taxi_data["estado"] = "movimiento"
            
        # 3. FINALIZAR (Cálculo de tarifa Nivel Esencial)
        elif accion == 'finish':
            # 2 céntimos parado, 5 céntimos movimiento
            total = (taxi_data["tiempo_parado"] * 0.02) + (taxi_data["tiempo_movimiento"] * 0.05)
            taxi_data["activo"] = False
            
            resumen = {
                "total": round(total, 2),
                "parado": round(taxi_data["tiempo_parado"], 1),
                "movimiento": round(taxi_data["tiempo_movimiento"], 1)
            }
            return jsonify(resumen)

    return jsonify({"estado_actual": taxi_data["estado"]})

if __name__ == '__main__':
    # Esto arranca el servidor web
    app.run(debug=True)