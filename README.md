# OptiTime Vision

Estudio de tiempos con visión computacional. Proyecto del Desafío OPS 360° (Procesos de Producción, UP 2026-II, Grupo 1).

Todo corre en el navegador: no se instala nada y no requiere permisos de administrador.

## Publicar en GitHub Pages (5 minutos, desde el navegador)

1. Entra a github.com e inicia sesión. Crea un repositorio **público** llamado `optitime`.
2. En el repositorio: **Add file → Upload files**. Arrastra **todo el contenido** de esta carpeta (`index.html`, `vision_bundle.mjs` y la carpeta `wasm`). Pulsa **Commit changes**.
3. **Settings → Pages**. En *Source* elige **Deploy from a branch**, rama `main`, carpeta `/ (root)`, y guarda.
4. En uno o dos minutos la página queda en `https://TU-USUARIO.github.io/optitime/`.

### Recomendado: subir también el modelo de manos

Si el archivo no está en el repositorio, la página lo descarga de los servidores de Google. Para no depender de ellos (por si la red de la universidad los bloquea):

1. Descarga `hand_landmarker.task` (unos 7,5 MB) desde:
   `https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task`
2. Súbelo a la raíz del repositorio, junto a `index.html`, con ese mismo nombre.

## Datos simulados incluidos

La página carga, la primera vez que se abre, un estudio **simulado** (no son mediciones reales) para mostrar el método completo: 15 ciclos por escenario (AS-IS y TO-BE), medidos con tres fuentes (cámara, cronómetro físico y revisión de video). Un aviso en la parte superior lo indica, y el botón **Borrar datos simulados** los elimina antes de registrar un estudio real.

| Indicador | AS-IS | TO-BE | Variación |
|---|---|---|---|
| TE del ciclo | 30,40 s | 25,53 s | −16,0 % |
| Capacidad, un operario | 118,4 u/h | 141,0 u/h | +19,1 % |
| Capacidad de línea (3 estaciones) | 250,9 u/h | 340,6 u/h | +35,7 % |
| Cuello de botella | Ensobrar y cerrar | Ensobrar y cerrar | — |
| Error medio frente al video | 0,31 s (manual) | 0,14 s (cámara) | −55 % |

Valoración 100 %, suplementos 15 %, TE = TN × (1 + s). Archivos en la carpeta `datos/`:

- `OptiTime_datos_simulados.csv`: los mismos registros, para importar en **Registros → Importar CSV**.
- `OptiTime_Verificacion_Simulada.xlsx`: verificación en Excel con fórmulas vivas (análisis, precisión, horas-analista, comparación y punto de equilibrio). La hoja *Léeme* explica todos los supuestos.
- `simular.py`: script que genera los datos (semilla fija, reproducible).

## Uso sin internet ni GitHub

Abre `index.html` con doble clic en Chrome o Edge. El modo Cronómetro, los registros, el análisis y la comparación funcionan sin internet. La cámara funciona igual, pero en ese caso el modelo se descarga de internet.

## Antes de la sustentación

- Prueba el enlace en una laptop de la universidad: permite la cámara cuando Chrome lo pida.
- Los registros se guardan solo en el navegador donde se midieron. Exporta el CSV al terminar cada sesión.
- Ten el video de la demo como respaldo.
- Para la demo en vivo, escribe en **Detener tras N ciclos** (panel «Medición en curso») cuántos ciclos quieres registrar: el registro se detiene solo al completar el último. 0 = sin límite.

## Componentes

- MediaPipe Tasks Vision 0.10.14 (Google, licencia Apache 2.0): detección de 21 puntos de cada mano.
- Lógica de zonas, cálculos de tiempo estándar y capacidad, y simulación: JavaScript propio en `index.html`.
