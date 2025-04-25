import torch
import json
import cv2
import os
import argparse
from ultralytics import YOLO

# Configurar argumentos de línea de comandos
parser = argparse.ArgumentParser(description="YOLOv8 Pothole Detection")
parser.add_argument("--input_folder", type=str, required=True, help="Ruta de la carpeta con las imágenes de entrada")
parser.add_argument("--conf_threshold", type=float, default=0.25, help="Umbral de confianza para detecciones")
args = parser.parse_args()

# Definir ruta de salida del JSON (mismo directorio que las imágenes)
output_json = os.path.join(args.input_folder, "output_annotations.json")

# Cargar el modelo YOLOv8 entrenado (debe estar en /app/best.pt dentro del contenedor)
model_path = "/app/best.pt"
if not os.path.exists(model_path):
    raise FileNotFoundError(f"El modelo '{model_path}' no fue encontrado dentro del contenedor.")
model = YOLO(model_path)

# Verifica si la carpeta de imágenes existe
if not os.path.exists(args.input_folder):
    raise FileNotFoundError(f"La carpeta '{args.input_folder}' no existe.")

# Obtener lista de imágenes en la carpeta
image_files = [f for f in os.listdir(args.input_folder) if f.endswith((".jpg", ".png", ".jpeg"))]

# Lista para guardar anotaciones en formato COCO
coco_annotations = {
    "images": [],
    "annotations": [],
    "categories": [{"id": 1, "name": "pothole", "supercategory": "damage"}],
}

annotation_id = 0  # ID para cada detección

for img_id, image_name in enumerate(image_files):
    image_path = os.path.join(args.input_folder, image_name)
    image = cv2.imread(image_path)

    if image is None:
        print(f"⚠️ No se pudo leer la imagen: {image_name}")
        continue

    # Obtener ancho y alto de la imagen
    height, width, _ = image.shape

    # Realizar inferencia con umbral configurable
    results = model(image_path, conf=args.conf_threshold)

    # Guardar info de la imagen en COCO
    coco_annotations["images"].append({
        "id": img_id,
        "file_name": image_name,
        "width": width,
        "height": height,
    })
    
    # Procesar detecciones
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0]  # Coordenadas del bounding box
            conf = float(box.conf[0])  # Confianza de la detección

            bbox_width = float(x2 - x1)
            bbox_height = float(y2 - y1)
            area = bbox_width * bbox_height  # Calcular área del bbox

            # Guardar la anotación en formato COCO
            coco_annotations["annotations"].append({
                "id": annotation_id,
                "image_id": img_id,
                "category_id": 1,
                "bbox": [float(x1), float(y1), bbox_width, bbox_height],
                "area": area,
                "score": conf,
                "iscrowd": 0,  # Se asume que no hay objetos agrupados
            })
            annotation_id += 1

# Guardar las anotaciones en un archivo JSON
with open(output_json, "w") as f:
    json.dump(coco_annotations, f, indent=4)

print(f"✅ Anotaciones guardadas en {output_json}")
