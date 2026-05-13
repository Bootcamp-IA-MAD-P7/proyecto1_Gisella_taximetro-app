from flask import Flask, render_template, request, jsonify
import time
import logging # Para el Nivel Medio

app = Flask(__name__)

# CONFIGURACIÓN DE LOGS (Nivel Medio)
logging.basicConfig(filename='taximetro.log', level=logging.INFO, 
                    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

# CONFIGURACIÓN DE PRECIOS (Nivel Medio - Permite cambiarlos aquí)
PRECIO_PARADO = 0.02
PRECIO_MOVIMIENTO = 0.05

taxi_data = {
    "activo": False,
    "estado": "parado",
    "tiempo_parado": 0,
    "tiempo_movimiento": 0,
    "ultima_marca_tiempo": 0
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/comando', methods=['POST'])
def comando():
    accion = request.json.get('accion')
    ahora = time.time()
    
    if accion == 'start':
        taxi_data.update({"activo": True, "estado": "parado", "tiempo_parado": 0, "tiempo_movimiento": 0, "ultima_marca_tiempo": ahora})
        logging.info("Viaje iniciado")
        return jsonify({"status": "viaje_iniciado"})

    if taxi_data["activo"]:
        duracion = ahora - taxi_data["ultima_marca_tiempo"]
        if taxi_data["estado"] == "parado":
            taxi_data["tiempo_parado"] += duracion
        else:
            taxi_data["tiempo_movimiento"] += duracion
        
        taxi_data["ultima_marca_tiempo"] = ahora

        if accion == 'stop':
            taxi_data["estado"] = "parado"
            logging.info("Taxi parado")
        elif accion == 'move':
            taxi_data["estado"] = "movimiento"
            logging.info("Taxi en movimiento")
        elif accion == 'finish':
            total = (taxi_data["tiempo_parado"] * PRECIO_PARADO) + (taxi_data["tiempo_movimiento"] * PRECIO_MOVIMIENTO)
            taxi_data["activo"] = False
            
            # GUARDAR EN HISTORIAL (Nivel Medio)
            resultado = f"Total: {round(total, 2)}€ | Parado: {round(taxi_data['tiempo_parado'], 1)}s | Movimiento: {round(taxi_data['tiempo_movimiento'], 1)}s"
            with open("historial_trayectos.txt", "a") as f:
                f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {resultado}\n")
            
            logging.info(f"Viaje finalizado. {resultado}")

            return jsonify({
                "total": round(total, 2),
                "parado": round(taxi_data["tiempo_parado"], 1),
                "movimiento": round(taxi_data["tiempo_movimiento"], 1)
            })

    return jsonify({"estado_actual": taxi_data["estado"]})

if __name__ == '__main__':
    app.run(debug=True)