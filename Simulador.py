#!/usr/bin/python3
import enum
import numpy as np	# para generar números al azar según distribución estándar

from mpi4py import MPI

comm = MPI.COMM_WORLD
pid = comm.rank
size = comm.size 

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
	##division_terrenos_mpi = []
	total_tortugas_anidadas = 0
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
	@classmethod 
	def inicializar_comportamiento(cls, comportamiento):
		cls.comportamiento_tortugas = comportamiento
		return
		
	@classmethod
	def inicializar_arribada(cls): #se debe llamar este metodo cada vez que haya un cambio en la marea, las tortugas inicializadas avanzan
		if(cls.marea_id == 1):
			for i in range(int(0.25 * len(cls.tortugas))):
				cls.tortugas[i].activar_tortuga()
				cls.tortugas[i].asg_posicion(15) 
		elif(cls.marea_id == 2):
			for i in range(int(0.25 * len(cls.tortugas)),int(0.75 * len(cls.tortugas))):
				cls.tortugas[i].activar_tortuga()
				cls.tortugas[i].asg_posicion(30) 
		elif(cls.marea_id == 3):
			for i in range(int(0.75 * len(cls.tortugas)),len(cls.tortugas)):
				cls.tortugas[i].activar_tortuga()
				cls.tortugas[i].asg_posicion(40) 
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
			cls.contadores_TVB[i].determinar_sector()
		
		for i in range(3): #inicializar posicion contadores de cuadrantes
			cls.contadores_C[i].asg_posicion(cuadrantes[i+1][0]+5,cuadrantes[i+1][1]+5)
			cls.contadores_C[i].determinar_sector()
		
		for i in range(transecto_berma[0][0]): #inicializar posicion contadores de transecto paralelo a la berma
			cls.contadores_TPB[0].asg_posicion(0,30)
					
	#determina los rangos de duracion de las mareas usando metodos de probabilidad 
	@classmethod
	def distribucion_duracion_mareas(cls):
		nivel_mareas = []
		nivel_mareas.append(2.2 * 0.33)
		nivel_mareas.append(nivel_mareas[0] + 2.2 * 0.45)
		return nivel_mareas
		
	@classmethod
	def determinar_altura_marea(cls,tic):
		return 0.004301 * tic + 0.6 ##este 0.6 hay que cambiarlo por el valor del archivo 
	
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
	def total_contadas_C(cls):
		for i in range(len(cls.contadores_C)):
			cls.conteo_cs = cls.conteo_cs + cls.contadores_C[i].obtener_contadas()
		
		
	@classmethod
	def total_contadas_TVB(cls):
		for i in range(len(cls.contadores_TVB)):
			cls.conteo_tsv = cls.conteo_tsv + cls.contadores_TVB[i].obtener_contadas()
		
	@classmethod
	def total_contadas_TPB(cls):
		for i in range(len(cls.contadores_TPB)):
			cls.conteo_tpb = cls.conteo_tpb + cls.contadores_TPB[i].obtener_contadas()
	
	@classmethod		
	def total_tortugas_anidaron(cls):
		for i in range(len(cls.tortugas)):
			if(cls.tortugas[i].obtener_si_anido()):
				cls.total_tortugas_anidadas = cls.total_tortugas_anidadas + 1
				
		
	
	@classmethod 
	#i es la cantidad de minutos entre muestreos, lo que dura caminando e inactivo
	#m es la cantidad total de muestreos 
	def formula_TPB(cls,m,i):
		return cls.conteo_tpb * i / (4.2 * m)
	
	@classmethod
	#d duracion en minutos de la simulacion 
	#m es la cantidad total de muestreos 
	#A el area de observación total en metros cuadrados (entra la berma y las dunas)
	#w es el ancho en metros de cada transecto
	def formula_TVB(cls,d,m):
		j = 0
		A = 0
		w = 2
		for i in range (cls.transectos_verticales[0][1]):
			j = j + 2
		for j in range(len(cls.contadores_TVB)):
			A = A + 2 * ( cls.transectos_verticales[i + 1][2] -  cls.transectos_verticales[i + 1][1]) 
		pt = 64.8 #me lo da el enunciado 
		return (A*d / (2*w*m*j)) * (cls.conteo_tsv / pt)
	
	@classmethod
	#Nc es la cantidad total de tortugas
	#d duracion en minutos de la simulacion 
	#m es la cantidad total de muestreos 
	def formula_C(cls,d,m):  
		Ac = (cls.cuadrantes[1][2] - cls.cuadrantes[1][0]) * (cls.cuadrantes[1][3] - cls.cuadrantes[1][1])
		A = 0
		for i in range(3):
			A = A + (  cls.cuadrantes[i+1][2] - cls.cuadrantes[i + 1][0] ) * (cls.cuadrantes[i + 1][3] - cls.cuadrantes[i + 1][1])
		return cls.conteo_cs * 1.25 * (Ac / A) * d / (1.08 * m)		
	
	@classmethod
	def simular(cls,tics):
		cls.total_tortugas_anidadas = 0
		cls.conteo_tpb = 0 		
		cls.conteo_tsv = 0		
		cls.conteo_cs = 0		
		cls.marea_id = 0
		if(pid == 0):
			begin = MPI.Wtime()	
		nivel_mareas = cls.distribucion_duracion_mareas()
		for tic in range(tics):
			altura_marea = cls.determinar_altura_marea(tic)
			hubo_cambio_de_marea = cls.determinar_tipo_marea(nivel_mareas, altura_marea) 
			if(hubo_cambio_de_marea):
				cls.inicializar_arribada()
			for t in range(len(cls.tortugas)):
				if(cls.tortugas[t].obt_sector() == pid):
					cls.tortugas[t].avanzar(cls.sectores_playa,cls.comportamiento_tortugas)
				if(tic % cls.cuadrantes[0][1] == 0): ##cada cuento los contadores por cuadrante cuentan
					posicion_tortuga = cls.tortugas[t].obt_posicion()
					for i in range(len(cls.contadores_C)):
						if(posicion_tortuga[0] >= cls.cuadrantes[i+1][0] and posicion_tortuga[0] <= cls.cuadrantes[i+1][2] and posicion_tortuga[1] >= cls.cuadrantes[i+1][1] and posicion_tortuga[1] <= cls.cuadrantes[i+1][3] and cls.contadores_C[i].obt_sector() == pid):
							cls.contadores_C[i].contar()
				if(tic % cls.transectos_verticales[0][1] == 0): ##cada cuento los contadores por transecto vertical cuentan
					for i in range(len(cls.contadores_TVB)):
						if(posicion_tortuga[0] >= cls.transectos_verticales[i+1][0] and posicion_tortuga[0] <= cls.transectos_verticales[i+1][0]+2 and posicion_tortuga[1] >= cls.transectos_verticales[i+1][1] and posicion_tortuga[1] <= cls.transectos_verticales[i+1][2] and cls.contadores_TVB[i].obt_sector() == pid):
							cls.contadores_TVB[i].contar()
				if(tic % cls.transecto_berma[0][1] == 0):  ##cada cuento los contadores por transecto paralelo cuentan
					if(posicion_tortuga[0] >= cls.contadores_TPB[0].obt_posicion()[0] and posicion_tortuga[0] <= cls.contadores_TPB[0].obt_posicion()[0]+30 and posicion_tortuga[1] >= cls.contadores_TPB[0].obt_posicion()[1]-30 and posicion_tortuga[1] <= cls.contadores_TPB[0].obt_posicion()[1]+30 and 0 == pid):
						cls.contadores_TPB[0].contar()
				else:
					if(pid == 0):
						cls.contadores_TPB[0].avanzar()
			comm.barrier()
		if(pid == 0):			
			cls.total_contadas_C()
			cls.total_contadas_TPB()
			cls.total_contadas_TVB()
			cls.total_tortugas_anidaron()
			end = MPI.Wtime()	
			print("Cantidad total de tortugas:",len(cls.tortugas))
			print("Cantidad de tortugas que en realidad anidaron:",cls.total_tortugas_anidadas)
			print("Total contadas por los contadores de cuadrantes:", int(cls.formula_C(tics,tics//cls.cuadrantes[0][1])) )
			print("Total contadas por los contadores de TVB:", int(cls.formula_TVB(tics,tics//cls.transectos_verticales[0][1])))
			print("Total contadas por los contadores de TPB:", int(cls.formula_TPB(tics//cls.transecto_berma[0][1],cls.transecto_berma[0][1])))
			print("Con tiempo de:", end	- begin)
		
	## DE ESTA CLASE SIMULADOR SÓLO EXISTIRÍA UNA INSTANCIA (SINGLETON).
	## POR LO QUE NO SE INCLUYEN MÉTODOS DE INSTANCIA, SÓLO MÉTODOS DE CLASE
