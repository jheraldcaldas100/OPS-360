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

## Uso sin internet ni GitHub

Abre `index.html` con doble clic en Chrome o Edge. El modo Cronómetro, los registros, el análisis y la comparación funcionan sin internet. La cámara funciona igual, pero en ese caso el modelo se descarga de internet.

## Antes de la sustentación

- Prueba el enlace en una laptop de la universidad: permite la cámara cuando Chrome lo pida.
- Los registros se guardan solo en el navegador donde se midieron. Exporta el CSV al terminar cada sesión.
- Ten el video de la demo como respaldo.

## Componentes

- MediaPipe Tasks Vision 0.10.14 (Google, licencia Apache 2.0): detección de 21 puntos de cada mano.
- Lógica de zonas, cálculos de tiempo estándar y capacidad, y simulación: JavaScript propio en `index.html`.
