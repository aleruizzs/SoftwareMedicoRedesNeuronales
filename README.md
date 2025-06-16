# Guía rápida de instalación y uso

## Instalación

1. **Clonar el repositorio**

   ```bash
   git clone https://github.com/aleruizzs/TFG.git
   cd TFG
   ```

2. **Iniciar los contenedores**
   
     ```bash
     docker-compose up --build web inference
     ```
     ⚠️ La primera vez puede tardar unos minutos, ya que se descargan los modelos y dependencias necesarias.
---

## Uso

1. **Acceso**

   * Visita `http://localhost:8000`.
   * Inicia sesión con tu usuario y contraseña.  
    Por defecto: usuario: admin, contraseña: admin123  
    <i>(En la memoria se explica cómo crear uno nuevo si lo deseas).</i>


2. **Analizar imagen**

   1. Elige un **modelo**.
   2. Introduce el **DNI del paciente**.
   3. Selecciona la **imagen** (JPG/PNG) y pulsa **“Procesar Imagen”**.
   4. Espera unos segundos mientras aparece el **spinner** de progreso.

3. **Resultados**

   * Se muestran la **Imagen Original** y la **Imagen Procesada** lado a lado.
   * Descarga el resultado con el botón **“Descargar imagen procesada”**.

4. **Historial**

   * Haz clic en **📂 Historial** para ver todas las imágenes procesadas.
   * Filtra por **DNI** usando la barra de búsqueda.
   * Usa 🔍 para abrir una imagen o 🗑️ para eliminarla.

5. **Cerrar sesión**

   * Pulsa **🚪 Cerrar sesión** en la parte superior de la página.
