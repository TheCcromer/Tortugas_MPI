#!/usr/bin/python3
import enum
import numpy as np	# para generar números al azar según distribución estándar

class Simulador:
	"""
	Representa al simulador de la arribada.
	"""
	
	## VARIABLES DE CLASE y son listas de listas 
	sectores_playa = [] 
	marea = []
	comportamiento_tortugas = []
	tortugas = []
	transecto_berma = []
	transectos_verticales = []
	cuadrantes = []
	tics = 0			## cantidad total de tics a simular
	tic = 0				## tic actual
	conteo_tpb = 0 		## variable para el conteo basado en transecto paralelo
	conteo_tsv = 0		## variable para el conteo basado en transectos verticales
	conteo_cs = 0		## variable para el conteo basado en cuadrantes
	cantidad_arribadas = 0
	id_marea = 0 #para decir si la marea es baja, media o alta 1 es baja, 2 es media, 3 es alta
	## MÉTODOS DE CLASE
	
	## utilizar archivo para sacar el tiempo y la altura que se requiere
	@classmethod
	def determinar_altura_marea(archivo):
		return 0.004301 * tic + 0.6
	
	
	##devuelve un booleano indicando que el tipo de marea cambio
	@classmethod
	def determinar_tipo_marea(): 
		marea_id = 0
		bool hubo_cambio = False
		if(determinar_altura_marea() >= marea[0] and determinar_altura_marea() < marea[1] ):
			marea_id = 1
			cantidad_arribadas = cantidad_arribadas+1
			hubo_cambio = True
		elif(determinar_altura_marea() >= marea[1] and determinar_altura_marea() < marea[2]):
			marea_id = 2
			cantidad_arribadas = cantidad_arribadas+1
			hubo_cambio = True
		elif(determinar_altura_marea() >= marea[2] and determinar_altura_marea() < marea[2]):
			marea_id = 3
			cantidad_arribadas = cantidad_arribadas+1
			hubo_cambio = True
		return hubo_cambio
	## EFE:Inicializa los sectores de playa con sp. 
	@classmethod
	def inicializar_playa(cls, sp):
		sectores_playa = sp
		return
	
	## EFE: Inicializa los datos de la marea con la posición i de la lista mareas.
	@classmethod
	def inicializar_marea(cls, mareas, i):  # i es cual fila especificamente de cual fila se va a usar 
		marea = mareas[i]
		return
		
	## EFE: Inicializa la arribada con el comportamiento de las tortugas y la cantidad 
	## indicada por nt de tortugas a simular.
	@classmethod
	def inicializar_arribada(cls, comportamiento, nt): #se debe llamar este metodo cada vez que haya un cambio en la marea, las tortugas inicializadas avanzan
		comportamiento_tortugas = comportamiento
		tortugas = Tortuga.crear_lista_tortugas(nt) # falta el comportamiento
		if(id_marea == 1 and cantidad_arribadas == 0):
			cantidad_arribadas = cantidad_arribadas+1
			for i in range(0.25 * len(tortugas)):
				tortugas[i].avanzar()
		elif(id_marea == 2 and cantidad_arribadas == 1):
			cantidad_arribadas = cantidad_arribadas+1
			for i in range(0.26 * len(tortugas),0.50 * len(tortugas)):
				tortugas[i].avanzar()
		elif(id_marea == 3 and cantidad_arribadas == 2):
			cantidad_arribadas = cantidad_arribadas+1
			for i in range(0.51 * len(tortugas),len(tortugas)):
					tortugas[i].avanzar()
		return

	## EFE: Inicializa el transecto paralelo a la berma.
	@classmethod
	def inicializar_transecto_berma(cls, tb):
		transecto_berma = tb
		return
	
	## EFE: Inicializa los transectos verticales.
	@classmethod
	def inicializar_transectos_verticales(cls, tsv):
		transectos_verticales = tsv
		return
	
	## EFE: Inicializa los cuadrantes.
	@classmethod
	def inicializar_cuadrantes(cls, cs):
		cuadrantes = cs
		return	
		

	## DE ESTA CLASE SIMULADOR SÓLO EXISTIRÍA UNA INSTANCIA (SINGLETON).
	## POR LO QUE NO SE INCLUYEN MÉTODOS DE INSTANCIA, SÓLO MÉTODOS DE CLASE.

		
	
