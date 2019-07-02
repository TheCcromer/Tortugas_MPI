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
	tics = 0			## cantidad total de tics a simular
	tic = 0				## tic actual
	conteo_tpb = 0 		## variable para el conteo basado en transecto paralelo
	conteo_tsv = 0		## variable para el conteo basado en transectos verticales
	conteo_cs = 0		## variable para el conteo basado en cuadrantes
	
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
	def inicializar_arribada(cls, comportamiento, nt): #se debe llamar este metodo cada vez que haya un cambio en la marea, las tortugas inicializadas avanzan
		comportamiento_tortugas = comportamiento
	##	tortugas = Tortuga.crear_lista_tortugas(nt) # se inicializan en el main, aqui lo que se hace es activarlas
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
		
	#determina los rangos de duracion de las mareas usando metodos de probabilidad 
	@classmethod
	def distribucion_duracion_mareas():
		nivel_mareas = []
		nivel_mareas.append(2.2 * 0.33)
		nivel_mareas.append(nivel_mareas[0] + 2.2 * 0.45)
		return mareas
		
	@classmethod
	def determinar_altura_marea(archivo):
		return 0.004301 * tic + 0.6
	
	@classmethod
	def determinar_tipo_marea(): 
		marea_id = 0
		hubo_cambio = False
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
	
	@classmethod 
	def formula_TPB(Nc,m,i):
		return Nc * i / (4.2 * m)
	
	@classmethod
	def formula_TVB(A,d,w,m,Nc):
		j = 0
		for i in range (transectos_verticales[0][1]):
			j = j + 2
		pt = 64.8 #me lo da el enunciado
		return (A*d / (2*w*m*j)) * (Nc / pt)
	
	@classmethod
	def formula_C(Nc,d,m):
		Ac = cuadrantes[1][2] - cuadrantes[1][0] * cuadrantes[1][3] - cuadrantes[1][1]
		#A = #area de observacion total entre la berma y las dunas
		return Nc * 1.25 * (Ac / A) * d / (1.08 * m)		
	
	@classmethod
	def simular(cls,tics):
		print(cls.marea[0])
		
			
	## DE ESTA CLASE SIMULADOR SÓLO EXISTIRÍA UNA INSTANCIA (SINGLETON).
	## POR LO QUE NO SE INCLUYEN MÉTODOS DE INSTANCIA, SÓLO MÉTODOS DE CLASE
