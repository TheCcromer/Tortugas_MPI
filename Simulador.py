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
	tortugas = []
	contadores_TPB = []
	contadores_TVB = []
	contadores_C = []
	conteo_tpb = 0 		## variable para el conteo basado en transecto paralelo
	conteo_tsv = 0		## variable para el conteo basado en transectos verticales
	conteo_cs = 0		## variable para el conteo basado en cuadrantes
	marea_id = 0
	## MÉTODOS DE CLASE
	
	## EFE:Inicializa los sectores de playa con sp. 
	@classmethod
	def inicializar_playa(cls, sp):
		cls.sectores_playa = sp
		return
	
	## EFE: Inicializa los datos de la marea con la posición i de la lista mareas.
	@classmethod
	def inicializar_marea(cls, mareas, i):  # i es cual fila especificamente de cual fila se va a usar 
		cls.marea = mareas[i]
		return
		
	## EFE: Inicializa la arribada con el comportamiento de las tortugas y la cantidad 
	## indicada por nt de tortugas a simular.
	def inicializar_comportamiento(cls, comportamiento)
		cls.comportamiento_tortugas = comportamiento
	@classmethod
	def inicializar_arribada(cls): #se debe llamar este metodo cada vez que haya un cambio en la marea, las tortugas inicializadas avanzan
		if(cls.id_marea == 1):
			for i in range(0.25 * len(tortugas)):
				tortugas[i].activar_tortuga()
				tortugas[i].asg_posicion(15)
		elif(cls.id_marea == 2):
			for i in range(0.25 * len(tortugas),0.75 * len(tortugas)):
				tortugas[i].activar_tortuga()
				tortugas[i].asg_posicion(30)
		elif(cls.id_marea == 3):
			for i in range(0.75 * len(tortugas),len(tortugas)):
				tortugas[i].activar_tortuga()
				tortugas[i].asg_posicion(40)
		return

	## EFE: Inicializa el transecto paralelo a la berma.
	@classmethod
	def inicializar_transecto_berma(cls, tb):
		cls.transecto_berma = tb
		return
	
	## EFE: Inicializa los transectos verticales.
	@classmethod
	def inicializar_transectos_verticales(cls, tsv):
		cls.transectos_verticales = tsv
		return
	
	## EFE: Inicializa los cuadrantes.
	@classmethod
	def inicializar_cuadrantes(cls, cs):
		cls.cuadrantes = cs
		return	
		
	@classmethod
	def inicializar_tortugas(cls, lista_tortugas):
		cls.tortugas = lista_tortugas
		
	@classmethod 
	def inicializar_contadores(cls, lista_contadores_TPB, lista_contadores_TVB, lista_contadores_C):	
		cls.contadores_TPB = lista_contadores_TPB
		cls.contadores_TVB = lista_contadores_TVB
		cls.contadores_C = lista_contadores_C
	
	@classmethod
	def asg_posicion_contadores(cls):
		for i in range(transectos_verticales[0][0]): #inicializar posicion contadores de transectos verticales
			cls.contadores_TVB[i].asg_posicion(transectos_verticales[i+1][0],(transectos_verticales[i+1][1] + transectos_verticales[i+1][2])//2)
		
		for i in range(3): #inicializar posicion contadores de cuadrantes
			cls.contadores_C[i].asg_posicion(cuadrantes[i+1][0]+5,cuadrantes[i+1][1]+5)
		
		for i in range(transecto_berma[0][0]): #inicializar posicion contadores de transecto paralelo a la berma
			cls.contadores_TPB[i].asg_posicion(0,30)
					
	#determina los rangos de duracion de las mareas usando metodos de probabilidad 
	@classmethod
	def distribucion_duracion_mareas(cls):
		nivel_mareas = []
		nivel_mareas.append(2.2 * 0.33)
		nivel_mareas.append(nivel_mareas[0] + 2.2 * 0.45)
		return nivel_mareas
		
	@classmethod
	def determinar_altura_marea(cls,tic):
		return 0.004301 * tic + 0.6
	
	@classmethod
	def determinar_tipo_marea(cls,nivel_mareas, altura_marea):
		hubo_cambio = False ## esta variable se utiliza mas tarde para saber si hubo cambio y llamar a arribada
		if(altura_marea >= cls.marea[0] and altura_marea < nivel_mareas[0] and cls.marea_id == 0):
			cls.marea_id = 1
			hubo_cambio = True
		elif(altura_marea >= nivel_mareas[0] and altura_marea < nivel_mareas[1] and cls.marea_id == 1):
			cls.marea_id = 2
			hubo_cambio = True
		elif(altura_marea >= nivel_mareas[1] and altura_marea < cls.marea[1] and cls.marea_id == 2):
			cls.marea_id = 3
			hubo_cambio = True
		return hubo_cambio
	
	@classmethod 
	def formula_TPB(cls,Nc,m,i):
		return Nc * i / (4.2 * m)
	
	@classmethod
	def formula_TVB(cls,A,d,w,m,Nc):
		j = 0
		for i in range (transectos_verticales[0][1]):
			j = j + 2
		pt = 64.8 #me lo da el enunciado
		return (A*d / (2*w*m*j)) * (Nc / pt)
	
	@classmethod
	def formula_C(cls,Nc,d,m):
		Ac = cuadrantes[1][2] - cuadrantes[1][0] * cuadrantes[1][3] - cuadrantes[1][1]
		#A = #area de observacion total entre la berma y las dunas
		return Nc * 1.25 * (Ac / A) * d / (1.08 * m)		
	
	@classmethod
	def simular(cls,tics,comportamiento):
		cls.comportamiento_tortugas = comportamiento
		nivel_mareas = cls.distribucion_duracion_mareas()
		for tic_actual in range(tics):
			altura_marea = cls.determinar_altura_marea(tic_actual)
			hubo_cambio_de_marea = cls.determinar_tipo_marea(nivel_mareas, altura_marea) 
			if(hubo_cambio_de_marea):
				cls.inicializar_arribada()
			for t in range(len(tortugas)):
				tortugas[t].avanzar(sectores_playa,comportamiento_tortugas)
				if(tic % cuadrantes[0][1] == 0):
					posicion_tortuga = tortugas[t].obt_posicion()
					for i in range(len(contadores_C)):
						if(posicion_tortuga[0] >= cuadrantes[i+1][0] and posicion_tortuga[0] <= cuadrantes[i+1][2] and posicion_tortuga[1] >= cuadrantes[i+1][1] and posicion_tortuga[1] <= cuadrantes[i+1][3]):
							contadores_C[i].contar()
				if(tic % transectos_verticales[0][1] == 0):
					for i in range(len(contadores_TVB)):
						if(posicion_tortuga[0] >= transectos_verticales[i+1][0] and posicion_tortuga[0] <= transectos_verticales[i+1][0]+2 and posicion_tortuga[1] >= transectos_verticales[i+1][1] and posicion_tortuga[1] <= transectos_verticales[i+1][2]):
							contadores_TVB[i].contar()
				if(tic % transecto_berma[0][1] == 0):
					for i in range(len(contadores_TPB)):
						if(posicion_tortuga[0] >= contadores_TPB[i].obt_posicion()[0] and posicion_tortuga[0] <= contadores_TPB[i].obt_posicion()[0]+30 and posicion_tortuga[1] >= contadores_TPB[i].obt_posicion()[1]-30 and posicion_tortuga[1] <= contadores_TPB[i].obt_posicion()[1]+30):
							contadores_TPB[i].contar()
	## DE ESTA CLASE SIMULADOR SÓLO EXISTIRÍA UNA INSTANCIA (SINGLETON).
	## POR LO QUE NO SE INCLUYEN MÉTODOS DE INSTANCIA, SÓLO MÉTODOS DE CLASE
