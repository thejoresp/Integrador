#!/bin/bash

# Verificar si Nginx NO está corriendo
if ! systemctl is-active --quiet nginx; then
  echo "Nginx no está corriendo. Iniciando en segundo plano..."
  sudo systemctl start nginx
  echo "Nginx iniciado."
  exit 0
fi

# Si Nginx ya está corriendo, mostrar opciones
echo "Nginx ya está corriendo."
echo "----------------------"
echo "1) Detener Nginx"
echo "2) Reiniciar Nginx"
echo "0) Salir (sin detener Nginx)"
echo

read -p "Elige una opción: " opcion

case $opcion in
  1)
    sudo systemctl stop nginx
    echo "Nginx detenido."
    ;;
  2)
    sudo systemctl restart nginx
    echo "Nginx reiniciado."
    ;;
  0)
    echo "Saliendo sin detener Nginx."
    exit 0
    ;;
  *)
    echo "Opción no válida."
    ;;
esac 