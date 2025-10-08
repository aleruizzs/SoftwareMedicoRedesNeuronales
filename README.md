# Quick Installation and Usage Guide in English

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/aleruizzs/SoftwareMedicoRedesNeuronales.git
   cd SoftwareMedicoRedesNeuronales
   ```

2. **Start the containers**
   
     ```bash
     docker-compose up --build web inference
     ```
     ⚠️ The first time it may take several minutes, as the required models and dependencies are downloaded.
---

## Usage

1. **Access**

   * Visit `http://localhost:8000`.
   * Log in with your username and password.  
    Default: username: admin, password: admin123  
    <i>(The project report explains how to create a new one if desired).</i>


2. **Analyze image**

   1. Choose a **model**.
   2. Enter the patient ID **(DNI)**.
   3. Select the **image** (JPG/PNG) and click **“Procesar Imagen”**.
   4. Wait a few seconds while the **spinner** indicates progress.

3. **Results**

   * The **Original Image** and the **Processed Image** are displayed side by side
   * Download the result using the **“Descargar imagen procesada”** button.

4. **History**

   * Click **📂 Historial** to view all processed images.
   * Filter by **DNI** using the search bar.
   * Use 🔍 to open an image or 🗑️ to delete it.

5. **Log out**

   * Click **🚪 Cerrar sesión** at the top of the page


# Guía Rápida de Instalación y Uso en Español

## Instalación

1. **Clonar el repositorio**

   ```bash
   git clone https://github.com/aleruizzs/SoftwareMedicoRedesNeuronales.git
   cd SoftwareMedicoRedesNeuronales
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
