# README

## Instalación y Configuración

Instrucciones para configurar y ejecutar la aplicación **aX-IAnalyzer** mediante un modelo de lenguaje local (LLM) utilizando LM Studio y Python.

---

### 1. Descargar LM Studio Desktop

Descargar la aplicación LM Studio desde el siguiente enlace:  
[LM Studio Download](https://lmstudio.ai/download)

---

### 2. Descargar un Modelo en LM Studio

Se recomienda descargar el modelo **Llama 3.1 8B**. Para ello:

1. Abrir LM Studio.
2. En el menú horizontal, seleccionar la opción **Search**.
3. Ingresar la siguiente URL en la barra de búsqueda:
   ```plaintext
   https://huggingface.co/lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF
   ```
4. Descargar el modelo desde el enlace proporcionado.

**Nota:** El modelo **Llama 3.1 8B** requiere recursos significativos, incluyendo un procesador de al menos 8 núcleos y 16 GB de RAM. Para un rendimiento óptimo con GPU, se recomienda una tarjeta NVIDIA RTX 3090 o superior con al menos 24 GB de VRAM. Si tu equipo tiene limitaciones, puedes optar por versiones cuantizadas más pequeñas y ligeras, como las de 4 u 8 bits.

---

### 3. Clonar el Repositorio

Para clonar el repositorio, utilizar el siguiente comando:

#### Usando SSH:
```bash
git clone git@github.com:Luminicen/DCU.git
```

---

### 4. Posicionarse en el Repositorio e Instalar Dependencias

1. Acceder al directorio clonado:

   ```bash
   cd DCU
   ```

2. (Opcional) Crear y activar un entorno virtual para la instalación:

   - En Linux/Mac:
     ```bash
     python -m venv env
     source env/bin/activate
     ```
   - En Windows:
     ```bash
     python -m venv env
     .\env\Scripts\activate
     ```

3. Instalar las dependencias requeridas:

   ```bash
   pip install -r requirements.txt
   ```

---

### 5. Cargar y Ejecutar el Modelo en LM Studio

1. Abrir LM Studio.
2. En el menú vertical, seleccionar la opción **Local Server**.
3. En la parte superior, seleccionar la opción **Select a model to load**.
4. Elegir el modelo que se descargó previamente (por ejemplo, **Llama 3.1 8B**).

---

### 6. Ejecutar la Aplicación Python

1. Acceder al directorio del proyecto:

   ```bash
   cd AccesibilidadIA
   ```

2. Ejecutar la aplicación desde el terminal utilizando el siguiente comando:

   ```bash
   python manage.py runserver
   ```

3. Abrir el navegador e ingresar a la dirección:

   ```plaintext
   http://127.0.0.1:8000/analizador
   ```

