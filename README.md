# Agenda:1.0
agenda telefonica sencilla lista para deploy

## Tecnologias

- Docker
- Python
- una base de datos (por definir si SQLite o Mariadb)

## instrucciones (temporales) de uso:

- clonar repositorio
- copiar archivo `agenda.csv` a carpeta app
    - IKMPORTANTE: la estructura esta definida para 4 campos, con lo cual el csv exportado debe tener las mismas definiciones
- teniendo docker instalado (si no lo tienen instalado, instalar bajo [estas instrucciones](https://docs.docker.com/engine/install/) )
- ejecutar `docker compose up -d`
- acceder mediante: `localhost:5000`