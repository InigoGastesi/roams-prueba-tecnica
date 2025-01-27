# Roams Back-end IA

API que genera texto usando un modelo preentrenado de HuggingFace.

## Requisitos

- Python 3.10
- pip
- Conda (opcional)
- Docker (opcional)

## Instalación

### Sin Docker

#### Usando Conda

1. Clona el repositorio:

    ```sh
    git clone https://github.com/InigoGastesi/roams-prueba-tecnica.git
    cd roams-prueba-tecnica
    ```

2. Crea y activa el entorno Conda:

    ```sh
    conda env create -f environment.yml
    conda activate roams-env
    ```

3. Inicia la aplicación:

    ```sh
    cd app
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```

#### Usando pip y venv

1. Clona el repositorio:

    ```sh
    git clone https://github.com/InigoGastesi/roams-prueba-tecnica.git
    cd roams-prueba-tecnica
    ```

2. Crea y activa un entorno virtual:

    ```sh
    python -m venv roams-env
    source roams-env/bin/activate  # En Windows usa `roams-env\Scripts\activate`
    ```

3. Instala las dependencias:

    ```sh
    pip install -r requirements.txt
    ```

4. Inicia la aplicación:

    ```sh
    cd app
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```

### Con Docker

1. Clona el repositorio:

    ```sh
    git clone https://github.com/InigoGastesi/roams-prueba-tecnica.git
    cd roams-prueba-tecnica
    ```

2. Construye la imagen de Docker:

    ```sh
    docker build -t roams-backend .
    ```

3. Inicia el contenedor:

    ```sh
    docker run -p 8000:8000 roams-backend
    ```

## Uso

La API estará disponible en `http://localhost:8000`. Primero es necesario registrar un usuario para luego logearse y poder usar los endpoints. Hay ejemplos en las configuraciones de postman

### Endpoints

- `POST /register`: Registrar un nuevo usuario.
- `POST /login`: Iniciar sesión y obtener un token de autenticación.
- `POST /generate`: Generar texto con GPT-2 (requiere autenticación).
- `GET /history`: Obtener el historial de textos generados por el usuario (requiere autenticación).

### Ejemplos de uso con Postman

1. Importa la colección de Postman desde `postman/ROAMS.postman_collection.json`.
2. Importa el entorno de Postman desde `postman/Local.postman_environment.json`.
3. Usa los endpoints definidos en la colección para interactuar con la API.

## Notas

- Asegúrate de tener configurado el archivo `.env` con las variables necesarias si es requerido.
- La base de datos SQLite se crea automáticamente en `app/db/connection.py`.
- La primera vez que ejecutes la aplicación, puede tardar un poco porque necesita descargar el modelo GPT-2.