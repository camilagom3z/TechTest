# Deployment Files (Docker Container)

Esta carpeta contiene todos los archivos necesarios para crear un **contenedor Docker** que despliega el modelo YOLOv8 entrenado para la detección de baches.

## Descripción general

El contenedor:
- Carga el modelo **YOLOv8** entrenado desde una ruta predefinida (`/app/best.pt`).
- Procesa **todos los archivos de imagen** dentro de una carpeta **montada por el usuario**.
- Genera un **único archivo JSON (`output_annotations.json`)** en formato COCO dentro de la misma carpeta.

---

## Instrucciones para crear el Docker

Para construir la imagen Docker, navega a la carpeta que contiene el `Dockerfile` y ejecuta:

```bash
docker build -t yolov8-pothole-detector .
```

## Instrucciones para ejecutar el Docker

Para ejecutar el contenedor y procesar imágenes, utiliza el siguiente comando:

### Para Linux:

```bash
docker run --rm -v $(pwd)/testimages:/input yolov8-pothole-detector python /app/inference.py --input_folder /input
```

### Para Windows:

```bash
docker run --rm -v "C:/Users/username/Downloads/testimages:/input" yolov8-pothole-detector python /app/inference.py --input_folder /input
```

### Nota importante sobre la ruta de las imágenes:

- La parte `/input` en el comando es la ruta **dentro del contenedor** donde se montará la carpeta con imágenes.
- La parte antes de los dos puntos (`$(pwd)/testimages` o `C:/Users/username/Downloads/testimages`) debe ser reemplazada con la **ruta completa a la carpeta de imágenes** en su sistema que desean analizar.
- Por ejemplo, si sus imágenes están en `/home/usuario/mis_imagenes` en Linux, el comando sería:
  ```bash
  docker run --rm -v /home/usuario/mis_imagenes:/input yolov8-pothole-detector python /app/inference.py --input_folder /input
  ```
- O si están en `D:\fotos\carreteras` en Windows, el comando sería:
  ```bash
  docker run --rm -v "D:\fotos\carreteras:/input" yolov8-pothole-detector python /app/inference.py --input_folder /input
  ```

## Resultados

Después de la ejecución, el contenedor generará:

✅ Un archivo `output_annotations.json` dentro de la misma carpeta que las imágenes de entrada.  
✅ El archivo JSON seguirá el formato de anotación COCO.  
✅ Si no se detectan baches en una imagen, aún así aparecerá en el JSON sin anotaciones.
