# Entorno Local

## Pre-requisitos
- Crear una base de datos en MySQL con el nombre edu_presente

## Instalacion

### uv
#### macOS y Linux
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```
#### Windows
```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Clonar este repositorio
```
git clone edu-presente-api
```
Luego dentro de la carpeta local de este repositorio, en la raiz de la carpeta se debe crear una variable `.env` que dentro defina: `DATABASE_URL = "mysql+mysqldb://{usuario_en_mysql}:{contraseña_en_mysql}@localhost/edu_presente"`

### Correr el proyecto en dev stage
Dentro de la carpeta local de este repositorio, en la raiz del proyecto se debe correr el siguiente comando:
```
uv run fastapi dev
```

### Probar endpoints
En el navegador se debe entrar a `localhost:8000/docs` para poder probar los endpoint usando Swagger
