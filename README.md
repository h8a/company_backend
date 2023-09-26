# Microservicio en FastAPI con MSSQL

### Requisitos:
- Python ^3.7
- Docker image de MSSQL
  - Librerias necesarias para el driver
    - unixodbc
    - unixodbc-dev
- OPCIONAL: sqlcmd
  - https://learn.microsoft.com/en-us/sql/tools/sqlcmd/sqlcmd-utility?view=sql-server-ver16&tabs=odbc%2Clinux
- OPCIONAL: DBeaver
  - https://dbeaver.io/

### Instrucciones para docker image de MSSQL
- Post oficial de Microsoft
  - https://learn.microsoft.com/en-us/sql/linux/quickstart-install-connect-docker?view=sql-server-ver16&pivots=cs1-bash
 
## Instrucciones para librerias necesarias de driver
- Estas librerias son necesarias ya que se usa aioodbc
  - Informacion e instrucciones oficiales:
    - https://pypi.org/project/aioodbc/

## Crear una DB
Una vez este ejecutando el contenedor como se describe en la documentacion anterior es necesario conectarnos a la db
ya sea mediante dbeaver o sqlcmd y se debe de crear una Base de Datos, de preferencia con el nombre **TestDB** 
sin embargo este se puede cambiar siempre y cuando las credenciales se modifiquen en el archivo `/employees/web/settings.py`

## Instrucciones de ejecucion de microservicio
- En el archivo settings se puede modificar todas las variables de configuracion usadas
- para ejecutar el microservicio es necesario crear un ambiente virtual en la raiz del proyecto con:
  - `python -m venv .env`
- instalar las librerias encesarias con el comando:
  - `pip install -r requirements.txt`
- ejecutar el microservicio con:
  - `uvicorn employees.web.app:app`
- Una vez ejecudado es posible entrar a la documentacion en la URL `localhost:8000/docs`
- El microservico esta validado mediante OAuth2 con JWT para lo cual se habilito la cabecera de nombre `Authorization`
  - El formato indicado para el header es `Authorization: Bearer TOKEN`  
