# analisis_espacial_marginalNoise PRototipo 1

Este repositorio contiene la arquitectura de procesamiento (pipeline espacial) diseñada para evaluar el impacto del ruido del tráfico vehicular a escala macro-urbana. La metodología fusiona modelos físicos de emisión acústica con macro-simulación de tráfico y datos de demanda poblacional mediante grillas hexagonales (H3).
---

## Datos disponibles

Actualmente, el modelo se alimenta de dos fuentes de datos estáticas que representan la "Demanda" (Receptores) y la "Oferta" (Infraestructura):

### A. Demanda Poblacional y Social (`miercoles_rm.csv`)
Base de datos agregada temporalmente (perfil horario) basada en datos pasivos/celulares.
* **Geometría:** Polígonos hexagonales del sistema H3 de Uber (Resolución 9, lado ~174m).
* **Columnas Clave:**
  * `h3_9`: Identificador único del hexágono.
  * `hora`: Ventana temporal de análisis.
  * `poblacion_flotante`: Cantidad dinámica de personas en la zona (Receptores).
  * `gse_ab`, `gse_c2`, `gse_d`, `gse_e`, etc.: Caracterización socioeconómica (proporciones).
  * `edad_*`: Caracterización demográfica.

### B. Infraestructura Vial (`red_vial_procesada.gpkg`)
Red topológica de calles extraída (ej. vía OpenStreetMap) y procesada geométricamente.
* **Geometría:** Líneas (LineString) proyectadas en coordenadas UTM (EPSG:32719).
* **Columnas Clave:**
  * `geometry`: Trazado exacto de la calle.
  * `velocidad_vf`: Velocidad máxima permitida o Flujo Libre ($v_f$).
  * `lanes`: Número de pistas (utilizado para calcular la Densidad de Atasco, $k_j$).

## Instalacion y funcionamiento

### 1. Activar Ambiente Virtual

```powershell
# Activar ambiente virtual con dependencias
source .venv/bin/activate

#deactivar
deactivate
```

## 2. Subir la data a utilizar
Se puede subir la data a traves de un programa. Pero se puede realizar manual en la carpeta data.

En data subir carpeta RedVial y miercoles_rm.csv (hexagonos)

```powershell
# Subir la data en tu carpeta Downloads (si no quieres hacerlo manual)
python3 captura_datos.py
```

## Metodología Implementada (Pipeline)
El código modularizado realiza el siguiente flujo de procesamiento:

1. **Fusión Espacial (Spatial Join):** Intersección geométrica (`gpd.overlay`) entre las líneas de las calles y los hexágonos H3. Las vías "heredan" la carga poblacional de su entorno.
2. **Estimación de Tráfico (Proxy):** Aplicación de un Factor de Conversión (10%) para transformar la `poblacion_flotante` zonal en un flujo vehicular estimado ($q$).
3. **Física de Tráfico (Greenshields):** Resolución de la ecuación macroscópica de Greenshields para obtener la Velocidad Operativa ($v_{op}$) y la Densidad ($k$) bajo condiciones de congestión.
4. **Modelo Acústico (Cai et al., 2015):** Cálculo del Nivel de Presión Sonora Continuo Equivalente ($L_{eq}$) emitido por cada tramo vial en función de su $v_{op}$ y $q$.
5. **Cálculo de Ruido Marginal ($dL/dk$):** Resolución de la derivada analítica del modelo de emisión para cuantificar la sensibilidad de la vía ante un vehículo adicional, discriminando regímenes "Sensibles" ($>0$) y "Saturados" ($<0$).
6. **Inmisión Territorial (Agregación Zonal):** Retorno de los niveles de ruido a los hexágonos mediante un **Promedio Energético Ponderado** (para $L_{eq}$) y un **Promedio Aritmético Ponderado** (para $dL/dk$), ponderando por la longitud de las vías intersectadas.
7. **Índice de Riesgo Social (IR):** Cálculo del impacto final multiplicando el clima acústico del hexágono por el logaritmo de su población flotante ($IR = L_{eq} \times \ln(1 + P)$).

---

## Limitaciones Actuales
El prototipo actual (Fase 1) es una prueba de concepto arquitectónica y posee las siguientes limitaciones metodológicas que deben ser consideradas al interpretar los resultados:

1. **Estimación Indirecta del Tráfico:** No se utilizan datos empíricos de sensores ni Matrices Origen-Destino (O-D). El flujo vehicular se infiere como un proxy proporcional a la población flotante del hexágono subyacente. No hay ruteo ni asignación de tráfico bajo equilibrio de Wardrop.
2. **Parámetros de Velocidad Simulados:** La velocidad operativa es un resultado netamente teórico derivado del modelo de Greenshields, el cual asume un comportamiento de flujo ininterrumpido que no siempre captura fricciones urbanas (ej. semáforos, eventos).
3. **Composición Vehicular Homogénea:** El modelo de emisión asume un flujo compuesto 100% por vehículos livianos, subestimando severamente el impacto acústico en vías con alto porcentaje de transporte de carga pesada.
4. **Resolución Espacial de Inmisión:** Se asume la Resolución 9 de H3 (~174m). Si bien es idónea para evaluar el "Clima Acústico Macrozonal" a nivel de barrio, no sustituye la modelación de propagación acústica 3D necesaria para evaluar el ruido específico en fachadas de edificaciones.

---