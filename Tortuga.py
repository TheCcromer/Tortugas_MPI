#!/usr/bin/python3
import enum
import numpy as np	# para generar números al azar según distribución estándar
import json			# para crear una hilera json en toJSON()
import random

class Tortuga:
	"""
	Representa una tortuga con id, velocidad y posicion.
	"""
	
	## VARIABLES DE CLASE
	id = 0 		## OJO variable static de clase para generar ids de tortugas
	
	## MÉTODOS DE CLASE
	""" metodo de clase que genera N tortugas """
	@classmethod
	def crea_lista_tortugas(cls,N):
		tortugas = []
		for i in range(N):
			t_n = Tortuga()
			tortugas.append(t_n)
		return tortugas
	
	class EstadoTortuga(enum.Enum):
		vagar = 0
		camar = 1
		excavar = 2
		poner = 3
		tapar = 4
		camuflar = 5
		inactiva = 6
		
	## MÉTODOS DE INSTANCIA
	
	## EFE: crea una tortuga inicializada al azar.
	def __init__(self):
		self.id = Tortuga.id
		Tortuga.id += 1
		self.velocidad = np.random.normal(1.0, 0.5) ## promedio = 1.0 y desviación estándar = 0.5
		self.posicion = random.randint(0, 1499), 0 ## OJO: así se crea un par ordenado, un tuple de dos valores
		self.estado = Tortuga.EstadoTortuga.inactiva ##se inicializa inactiva y cuando arriba es cuando se le asigna el estado de vagar
		self.sector = self.determinar_sector(self.posicion)
		self.duraciones = []
		self.contador_tics = 0
		self.anidar = False
		return 
	
	def determinar_sector(self,pos):
		return pos[1] // 100 
	
	## EFE: retorna una hilera en formato JSON que representa a la tortuga
	def toJSON(self):
		# (type(self).__name__ retorna como hilera el nombre de la clase de self
		# se le pasa un tuple con el nombre de la clase y los valores de los atributos de self
		return json.dumps((type(self).__name__, self.id, self.velocidad, self.posicion))
	
	def obt_id(self):
		return self.id
	
	def obt_velocidad(self):
		return self.velocidad
	
	def obt_posicion(self):
		return self.posicion
		
	def asg_velocidad(self, vn):
		self.velocidad = vn
		return
	
	def asg_posicion(self, pn):
		self.posicion = random.randint(0, 1499),pn
		return

	def activar_tortuga(self):
		if(self.estado == Tortuga.EstadoTortuga.inactiva):
			self.estado = Tortuga.EstadoTortuga.vagar
			
	def obtener_si_anido(self):
		return self.anidar
		

	def proba_desactivarse(self, archivo):
		probabilidad  = np.random.uniform(low = 0.0, high = 1.0, size = None)
		desactivada = False
		# remplazar los valores de probabilidad necesarios para cambiar de estado por lo que se va a leer de los archivos
		if(probabilidad <= archivo[0][0] and self.estado == Tortuga.EstadoTortuga.vagar):
			self.estado = Tortuga.EstadoTortuga.inactiva
			desactivada = True
		elif(probabilidad <= archivo[0][1] and self.estado == Tortuga.EstadoTortuga.camar):
			self.estado = Tortuga.EstadoTortuga.inactiva
			desactivada = True
		elif(probabilidad <= archivo[0][2] and self.estado == Tortuga.EstadoTortuga.excavar):
			self.estado = Tortuga.EstadoTortuga.inactiva
			desactivada = True
		elif(probabilidad <= archivo[0][3]and self.estado == Tortuga.EstadoTortuga.poner):
			self.estado = Tortuga.EstadoTortuga.inactiva
			desactivada = True
		elif(probabilidad <= archivo[0][4] and self.estado == Tortuga.EstadoTortuga.tapar):
			self.estado = Tortuga.EstadoTortuga.inactiva
			desactivada = True
		elif(probabilidad <= archivo[0][5] and self.estado == Tortuga.EstadoTortuga.camuflar):
			self.estado = Tortuga.EstadoTortuga.inactiva
			desactivada = True
		return desactivada
	
	## sacar los datos de distribucion normal y el 372 de archivos
	## Inicializa las duraciones de cada estado de cada tortuga
	def inicializar_duraciones(self, archivo):
		duracion_camar = np.random.normal(archivo[1][0],archivo[1][1],None) #distribucion normal de camar
		duracion_excavar = np.random.normal(archivo[1][2],archivo[1][3],None) #distribucion normal de excavar
		duracion_poner = np.random.normal(archivo[1][4],archivo[1][5],None) #distribucion normal de poner
		duracion_tapar = np.random.normal(archivo[1][6],archivo[1][7],None) #distribucion normal de tapar
		duracion_camuflar = np.random.normal(archivo[1][8],archivo[1][9],None) #distribucion normal de camuflar
		## vagar 
		self.duraciones.append(duracion_camar) #duracion de camar, etc...
		self.duraciones.append(duracion_excavar) 
		self.duraciones.append(duracion_poner) 
		self.duraciones.append(duracion_tapar)	
		self.duraciones.append(duracion_camuflar) 
		
	## este metodo esta directamente relacionado a avanzar y la desviacion estandar de la duracion de cada estado
	## la desviacion estandar es algo diferente para cada tortuga
	def cambiar_estado(self, archivo):
		if not(self.proba_desactivarse(archivo)):
			if(self.estado == Tortuga.EstadoTortuga.vagar):
				self.estado = Tortuga.EstadoTortuga.camar
				duracion_actual = 0
			elif(self.estado == Tortuga.EstadoTortuga.camar and duracion_actual >= duraciones[0]):
				self.estado = Tortuga.EstadoTortuga.excavar
				duracion_actual = 0
			elif(self.estado == Tortuga.EstadoTortuga.excavar and duracion_actual >= duraciones[1]):
				self.estado = Tortuga.EstadoTortuga.poner
				duracion_actual = 0
			elif(self.estado == Tortuga.EstadoTortuga.poner and duracion_actual >= duraciones[2]):
				self.estado = Tortuga.EstadoTortuga.tapar
				duracion_actual = 0
			elif(self.estado == Tortuga.EstadoTortuga.tapar and duracion_actual >= duraciones[3]):
				self.estado = Tortuga.EstadoTortuga.camuflar
	
	#EFE: determina la localizacion en la que se encuentra la tortuga para que con las repectivas probabilidades cambie de estado		
	#Recibe la matriz correspondiente a terreno
	def cambio_de_vagar(self,terreno,comportamiento):
		if(terreno[self.sector][1] > self.posicion[1] and  self.posicion[1] > terreno[self.sector][1] - 10):
			if(np.random.uniform(low = 0.0, high = 1.0, size = None) < comportamiento[2][0]):
				self.cambiar_estado(comportamiento)
				self.anidar = True
				self.inicializar_duraciones(comportamiento)
		if(terreno[self.sector][1] < self.posicion[1] and  self.posicion[1] < terreno[self.sector][1] + 10):
			if(np.random.uniform(low = 0.0, high = 1.0, size = None) < comportamiento[2][1]):
				self.cambiar_estado(comportamiento)
				self.inicializar_duraciones(comportamiento)
				self.anidar = True
		if(terreno[self.sector][1] + 10 < self.posicion[1] and  self.posicion[1] < terreno[self.sector][1] + 20):
			if(np.random.uniform(low = 0.0, high = 1.0, size = None) < comportamiento[2][2]):
				self.cambiar_estado(comportamiento)
				self.inicializar_duraciones(comportamiento)
				self.anidar = True
		if(terreno[self.sector][1] + 20 < self.posicion[1] and  self.posicion[1] < terreno[self.sector][1] + 30):
			if(np.random.uniform(low = 0.0, high = 1.0, size = None) < comportamiento[2][3]):
				self.cambiar_estado(comportamiento)
				self.inicializar_duraciones(comportamiento)
				self.anidar = True
			 
	
		
	## EFE: avanza la tortuga de acuerdo con su estado
	def avanzar(self,terreno,comportamiento):
		if(self.estado == Tortuga.EstadoTortuga.vagar):
			self.posicion = self.posicion[0],self.posicion[1] + self.velocidad
			self.cambio_de_vagar(terreno,comportamiento)
		else:
			if not(self.estado ==  Tortuga.EstadoTortuga.inactiva):
				self.contador_tics = self.contador_tics + 1
				if(self.estado == Tortuga.EstadoTortuga.camar):
					if(self.contador_tics >= self.duraciones[0]):
						if not(self.proba_desactivarse(comportamiento)):	
							self.estado = Tortuga.EstadoTortuga.excavar
							self.contador_tics = 0
				elif(self.estado == Tortuga.EstadoTortuga.excavar):
					if(self.contador_tics >= self.duraciones[1]):
						if not(self.proba_desactivarse(comportamiento)):
							self.estado = Tortuga.EstadoTortuga.poner
							self.contador_tics = 0
				elif(self.estado == Tortuga.EstadoTortuga.poner):
					if(self.contador_tics >= self.duraciones[2]):
						if not(self.proba_desactivarse(comportamiento)):
							self.estado = Tortuga.EstadoTortuga.tapar
							self.contador_tics = 0
				elif(self.estado == Tortuga.EstadoTortuga.tapar):
					if(self.contador_tics >= self.duraciones[3]):
						if not(self.proba_desactivarse(comportamiento)):
							self.estado = Tortuga.EstadoTortuga.camuflar
							self.contador_tics = 0
				elif(self.estado == Tortuga.EstadoTortuga.camuflar):
					if(self.contador_tics >= self.duraciones[4]):
						if not(self.proba_desactivarse(comportamiento)):
							self.estado = Tortuga.EstadoTortuga.inactiva
							self.contador_tics = 0
		#no se si esto deberia devolver algo, tenia un return
	
