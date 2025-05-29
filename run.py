import uvicorn
# from app.main import app # Ya no es necesario importar app directamente aquí

if __name__ == "__main__":
    # Pasa la aplicación como una cadena de importación "module:variable"
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=True) 