#!/usr/bin/python3

import sys
import csv  # este es un modulo reader que permite leer los archivos csv 
from enum import Enum

from Tortuga import Tortuga
from Contador import Contador
from Simulador import Simulador 
from mpi4py import MPI

comm = MPI.COMM_WORLD
pid = comm.rank
size = comm.size
## Para lectura de archivos de texto en python ver:
## https://www.pythonforbeginners.com/files/reading-and-writing-files-in-python

## Para leer archivos csv con numeros con python ver:
## https://pythonprogramming.net/reading-csv-files-python-3/

## Para manejo de excepciones en python ver:
## https://docs.python.org/3/library/exceptions.html

## Tipo enumerado para los dos tipos de numeros que se pueden leer
class Tipos_numeros(Enum):
	int = 0
	float = 1
	
## EFE: lee un archivo csv con numeros separados por coma y retorna una lista 
## de listas de numeros de tipo tn.
def lee_numeros_csv(archivo,tn):
	lista = []
	read_csv = csv.reader(archivo, delimiter=',')
	for row in read_csv:
		sublista = []
		for n in row:
			try:
				if (tn == Tipos_numeros.int):
					sublista.append(int(n))
				else: 
					sublista.append(float(n))
			except ValueError as error_de_valor:
				print("Error de tipo de valor: {0}".format(error_de_valor)) #{0} en que lugar de la ilera para el error
		lista.append(sublista)
	return lista
	
def crear_lista_de_archivos():
	archivos_csv = []
	archivos_csv.append("experimentos.csv")
	archivos_csv.append("marea.csv")
	archivos_csv.append("comportamiento_tortugas.csv")
	archivos_csv.append("terreno.csv")
	archivos_csv.append("transectos_verticales.csv")
	archivos_csv.append("transecto_paralelo_berma.csv")
	archivos_csv.append("cuadrantes.csv")
	return archivos_csv
	
def lectura_de_archivos(archivos_csv):
	data_csv_matriz = []
	for i in range(len(archivos_csv)):
		if(i == 2 or i == 1 or i == 3):	##es el numero de archivo que si se ocupa float 
			try:
				with open(archivos_csv[i]) as ct_csv:  #with open es la ruta donde se abre el archivo 
					data_csv_matriz.append(lee_numeros_csv(ct_csv,Tipos_numeros.float))
				#print(dts_ct)
			except OSError as oserror: #investigar el OSError 
				print("Error de entrada-salida de archivos: {0}".format(oserror))
		else :
			try:
				with open(archivos_csv[i]) as ct_csv:  #with open es la ruta donde se abre el archivo 
					data_csv_matriz.append(lee_numeros_csv(ct_csv,Tipos_numeros.int))
				#print(dts_ct)
			except OSError as oserror: #investigar el OSError 
				print("Error de entrada-salida de archivos: {0}".format(oserror))		
	return data_csv_matriz

def inicializar_simulaciones(data_csv_matriz):
	## solo es necesario inicializarlos una vez
	Simulador.inicializar_marea(data_csv_matriz[1],0)
	Simulador.inicializar_playa(data_csv_matriz[3])
	Simulador.inicializar_transecto_berma(data_csv_matriz[5])
	Simulador.inicializar_transectos_verticales(data_csv_matriz[4])
	Simulador.inicializar_cuadrantes(data_csv_matriz[6])
	Simulador.inicializar_comportamiento(data_csv_matriz[2])
	cantidades_totales = [0]*4
	for i in range (3):
		for k in range(data_csv_matriz[0][i][0]):
			inicio = MPI.Wtime()
			Simulador.inicializar_contadores(Contador.crea_lista_Contadores(data_csv_matriz[5][0][0]), Contador.crea_lista_Contadores(data_csv_matriz[4][0][0]),Contador.crea_lista_Contadores(data_csv_matriz[6][0][0]))
			Simulador.inicializar_tortugas(Tortuga.crea_lista_tortugas(int(data_csv_matriz[0][i][2])//size))
			cantidades = Simulador.simular(int(data_csv_matriz[1][0][2]))
			comm.barrier()
			for j in range(4):
				cantidades_totales[j] = comm.reduce(cantidades[j],op = MPI.SUM)
			comm.barrier()
			if(pid == 0):
				final = MPI.Wtime()
				print("Cantidad total de tortugas:",(int(data_csv_matriz[0][i][2])))
				print("Cantidad de tortugas que en realidad anidaron:",cantidades_totales[0])
				print("Total contadas por los contadores de cuadrantes:", cantidades_totales[1])
				print("Total contadas por los contadores de TVB:", cantidades_totales[2])
				print("Total contadas por los contadores de TPB:", cantidades_totales[3])
				print("Tiempo total de esta simulacion", final - inicio)
			cantidades_totales = [0]*4
			comm.barrier()
		comm.barrier()
def main():
	archivos_csv = crear_lista_de_archivos()
	data_csv_matriz = lectura_de_archivos(archivos_csv)
	inicializar_simulaciones(data_csv_matriz)
	
main()
