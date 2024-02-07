# Proceso de Optimización

El proceso de optimización consiste en asignar vehículos de manera óptima a pedidos específicos, considerando una serie de criterios y restricciones. El flujo de trabajo se describe a continuación:

1. **Integración de Servicios de Localización de Here:**

    - Se integran los servicios de localización de Here para gestionar direcciones como parte del proceso de asignación de vehículo óptimo.

2. **Limpieza y Normalización de Datos:**

    - Se realiza la limpieza y normalización de los datos necesarios para la ejecución del algoritmo.

3. **Ejecución del Algoritmo:**

    - Se ejecuta el algoritmo, que sigue el siguiente flujo de decisión en función de los parámetros definidos por el cliente:
        - Tipo de Viaje (Internacional/Nacional).
        - Limitaciones del Vehículo/Condiciones del Conductor (Sinex).
        - Características del Envasado del Pedido.
        - Coincidencia de Material con Pedidos Anteriores.
        - Necesidad de Limpieza del Vehículo para Asignación de Nuevo Porte.
        - Características del Punto de Origen (Sinex).
        - Características del Punto de Destino (Sinex).
        - Perfil de Ruta/Diferencia de Cota (Validación con Here).
        - Selección de Vehículos Candidatos.
        - Validación de Fecha y Hora de Entrega del Pedido.
        - Cálculo Estimado del Tiempo de Recorrido y Pausas del Conductor.
        - Asignación del Pedido al Transportista con Menor Coste.

4. **Asignación del Viaje:**
    - La asignación del viaje puede ser manual o automática, considerando la cantidad de pedido y validando el peso del camión.
