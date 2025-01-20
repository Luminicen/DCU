# README

## Instalación y Configuración

Instrucciones para configurar y ejecutar la aplicación aX-IAnalyzer mediante un modelo de lenguaje local (LLM) utilizando LM Studio y Python.

### 1. Descargar LM Studio Desktop

Descargar la aplicación LM Studio desde el siguiente enlace:
[LM Studio Download](https://lmstudio.ai/download)

### 2. Descargar un Modelo en LM Studio

Se recomienda descargar el modelo **Llama 3.1 8B**. Para ello:

1. Abrir LM Studio.
2. En el menú horizontal, seleccionar la opción **Search**.
3. Ingresar la siguiente URL en la barra de búsqueda:
   ```
   https://huggingface.co/lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF
   ```
4. Descargar el modelo desde el enlace proporcionado.

**Nota:** Se puede optar por utilizar otro modelo de mayor preferencia.

### 3. Clonar el Repositorio

Para clonar el repositorio, utilizar el siguiente comando:

#### Usando SSH:
```bash
git clone git@github.com:Luminicen/DCU.git
```

### 4. Posicionarse en el Repositorio e Instalar Dependencias

1. Acceder al directorio clonado:
   ```bash
   cd DCU
   ```

2. Instalar las dependencias requeridas:
   ```bash
   pip install -r requirements.txt
   ```

### 5. Cargar y Ejecutar el Modelo en LM Studio

1. Abrir LM Studio.
2. En el menú vertical, seleccionar la opción **Local Server**.
3. En la parte superior, seleccionar la opción **Select a model to load**.
4. Eligir el modelo que se descargó previamente (por ejemplo, **Llama 3.1 8B**).

### 6. Ejecutar la Aplicación Python

1. Posicionarse en directorio del proyecto:
   ```bash
   cd AccesibilidadIA
   ```

2. Ejecutar la aplicación desde el terminal utilizando el siguiente comando:
   ```bash
   python manage.py runserver
   ```


