# Microservicios de Comercio Electrónico

Trabajo Práctico: Considerar que se tiene desarrollado un sistema de comercio electrónico, el cual contiene 4 microservicios

Este repositorio contiene una aplicación de microservicios para un sistema de comercio electrónico. Incluye los microservicios de **catálogo** y **api-gateway**.

## Requisitos

- **Docker**
- **Docker Compose**

## Instalación

1. Clonar el repositorio:
    ```bash
    git clone https://github.com/SantiSabio/microservices.git
    cd microservices
    ```

2. Crear y levantar los contenedores:
    ```bash
    docker-compose up --build
    ```
flask create-db

## Ejecución

- **Microservicio de catálogo**:
    - URL: `http://localhost:5001/catalogo`
    
- **API Gateway**:
    - URL: `http://localhost:5000/productos`

## Estructura del Proyecto

```plaintext
microservices/
├── api-gateway/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── routes.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── run.py
├── ms-catalogo/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── routes.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── run.py
├── docs/
│   └── estructura.txt
├── docker-compose.yml
├── README.md
└── .env
