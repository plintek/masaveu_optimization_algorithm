# Documentación de la fase 1 del proyecto de optimización de rutas de transporte

El proyecto de optimización de rutas de transporte es un sistema que permite la asignación de vehículos a pedidos de transporte. Está compuesto por un backend, un frontend y un algoritmo de optimización. El backend es el encargado de recibir los pedidos, procesarlos y enviarlos al algoritmo de optimización. El frontend es una interfaz gráfica que permite realizar las pruebas del algoritmo de optimización con unos datos de prueba introducidos por el usuario (simulando la aplicación final y los datos de Sinex). El algoritmo de optimización es el encargado de asignar los vehículos a los pedidos de transporte.

---

### Proceso de Optimización

El optimizador comienza con la recepción de un pedido, que puede ser nacional o internacional. A partir de este punto, el algoritmo sigue una serie de pasos para determinar el vehículo más adecuado para realizar el transporte. El algoritmo tiene en cuenta las limitaciones del vehículo, las características del envasado, el material transportado, la necesidad de limpieza del vehículo, las características del punto de origen y del punto de destino, el perfil de la ruta, la distancia de los vehículos al punto de origen, la fecha y hora de entrega del pedido, el tiempo estimado de recorrido, la estimación de pausas del conductor, el número de kilómetros y pedidos realizados al trimestre, y el coste por kilómetro del transportista. Una vez que se han tenido en cuenta todos estos factores, el algoritmo asigna el viaje al vehículo más adecuado, teniendo en cuenta la cantidad de pedido y el peso del camión.

##### Entrada de datos

-   Pedido: Se recibe el identificador de un pedido y si se fuerza la limpieza del
    vehículo
-   Sinex: Se hace la consulta para obtener información sobre pedidos, origenes, destinos, clientes,
    vehículos, conductores, etc
-   Jaltest: Se hace la consulta para obtener información de los vehículos y conductores (geolocalización, estado del vehículo, conductor, etc)
-   Here: Se recibe las informaciones necesarias para el cálculo de la distancia, tiempos y rutas
    de los vehículos al punto de origen y destino

##### Procesado de datos

En la recepción de un pedido se ejecuta un adaptador para la conversión de los datos a nuestro esquema. A continuación, se ejecuta el algoritmo, que sigue el siguiente flujo de decisión en función de los parámetros definidos por el cliente:

-   Viaje internacional/Nacional (pedido): el punto de entrega es nacional o
    internacional
-   Limitaciones del vehículo/condiciones del conductor (Sinex) : Si el vehículo
    no ha pasado itv, conductor de baja médica, necesidad de revisión, etc
-   Características del envasado (pedido): en cuba, palet, bañera..
-   Mismo material: si el vehículo transporta el mismo material que en el porte
    anterior (Pedido-Pedidos anteriores)
-   Necesidad de realizar una limpieza del vehículo para la asignación de un
    nuevo porte (no, si, petición masaveu)
-   Características del punto de origen (Sinex), altura, cuba, silo
-   Características del punto de destino (sinex), altura, cuba, silo
-   Integración Perfil Ruta/diferencia de cota: A través de un servicio
    proporcionado por Dotgis, obtener el perfil de la ruta y validarlo con la
    capacidad de giro y máxima pendiente que tenga el vehículo
-   Vehículos candidatos:
-   Equipo de vehículos asociados al punto de origen.
-   Vehículos disponibles de otros equipos que estén por la zona
    geográfica del punto de origen y que tengan como destino la zona
    geográfica asociada al equipo del vehículo.
-   Del conjunto de candidatos existentes, siempre tendrán prioridad los del
    punto (b) sobre los del punto (a).
-   Distancia de los vehículos al punto de Origen, llamada a here y
    posicionamiento del vehículo de Sinex
-   Validación del cumplimiento de fecha y hora de entrega del pedido.
-   Cálculo estimado del tiempo de:
-   Recorrido hasta el punto de origen (Pex).
-   Gestión de carga en Pex.
-   Recorrido hasta el punto de destino.
-   Estimación de pausas del conductor.
-   Pedidos asignados a los distintos transportistas, asignación que tenga
    menor número de Km y Pedidos realizados al trimestre. Se estimará el
    coste por km del transportista
-   Asignación del viaje, esta podrá ser manual o automática
-   Cantidad de Pedido, validar peso de camión

##### Salida de datos

-   Lista de vehículos candidatos
-   Vehículo óptimo para el pedido
-   Rutas de los vehículos al punto de origen
-   Ruta de origen a destino

Las salidas de datos son almacenadas en una caché para agilizar las siguientes optimizaciones.

##### Integraciones a realizar

-   Integración Jaltest: Se implementará la API Jaltest de Masaveu para lo
    necesario en la optimización
-   Integración Sinex: Se implementará una versión adaptada a nuestro
    backend basándose en los datos aportados, una vez se tenga acceso a la
    API se creará una adaptador para la conversión de dichos datos a nuestro
    esquema.
-   Integración de servicio para diferencias de cota y capacidad de giro: Se
    implementará un servicio que nos permita obtener el perfil de la ruta y
    validarlo con la capacidad de giro y máxima pendiente que tenga el
    vehículo

##### Tecnologías

-   Python
-   Redis
-   Here
-   Docker

---

### Backend

El backend está compuesto por un servidor web que recibe los pedidos de transporte y los procesa. El servidor web se comunica con el algoritmo de optimización a través de una API REST. Tiene implementado un sistema de caché para almacenar los resultados de las optimizaciones y agilizar las siguientes optimizaciones. Además cuenta con un sistema de autenticación básico para el acceso a la API.

##### Tecnologías

-   Python
-   Django
-   Redis
-   Docker
-   Swagger

---

### Frontend

El frontend es una interfaz gráfica que permite realizar las pruebas del algoritmo de optimización con unos datos de prueba introducidos por el usuario. El frontend se comunica con el backend a través de una API REST, recibe los resultados del algoritmo de optimización y los muestra al usuario. Además, se muestra un mapa con los vehículos coloreados en una escala de colores dependiendo de su puntuación, las rutas al punto de origen y la ruta de origen a destino. Se destaca el vehículo óptimo para el pedido.

##### Tecnologías

-   React
-   Docker
-   Mapbox
-   Deck GL
-   Material-UI
-   Vite

---

Todos los componentes del proyecto están desplegados en contenedores Docker y orquestados con Docker Compose. Para iniciar cada uno de los componentes, se debe ejecutar el siguiente comando _make_ en sus respectivas carpetas.
