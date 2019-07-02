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
		self.posicion = random.randint(0, 1499), random.randint(0, 1499) ## OJO: así se crea un par ordenado, un tuple de dos valores
		self.estado = Tortuga.EstadoTortuga.inactiva ##se inicializa inactiva y cuando arriba es cuando se le asigna el estado de vagar
		return 
	
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
		self.posicion = pn
		return
	 
	@classmethod
	def proba_desactivarse(self, archivo):
		probabilidad  = np.random.uniform(low = 0.0, high = 1.0, size = None)
		desactivada = False
		# remplazar los valores de probabilidad necesarios para cambiar de estado por lo que se va a leer de los archivos
		if(probabilidad <= 0.2 and self.estado == Tortuga.EstadoTortuga.vagar):
			self.estado = Tortuga.EstadoTortuga.inactiva
			desactivada = True
		elif(probabilidad <= 0.2 and self.estado == Tortuga.EstadoTortuga.camar):
			self.estado = Tortuga.EstadoTortuga.inactiva
			desactivada = True
		elif(probabilidad <= 0.6 and self.estado == Tortuga.EstadoTortuga.excavar):
			self.estado = Tortuga.EstadoTortuga.inactiva
			desactivada = True
		elif(probabilidad <= 0.2 and self.estado == Tortuga.EstadoTortuga.poner):
			self.estado = Tortuga.EstadoTortuga.inactiva
			desactivada = True
		elif(probabilidad <= 0.01 and self.estado == Tortuga.EstadoTortuga.tapar):
			self.estado = Tortuga.EstadoTortuga.inactiva
			desactivada = True
		elif(probabilidad <= 0.01 and self.estado == Tortuga.EstadoTortuga.camuflar):
			self.estado = Tortuga.EstadoTortuga.inactiva
			desactivada = True
		return desactivada
	
	## sacar los datos de distribucion normal y el 372 de archivos
	## Inicializa las duraciones de cada estado de cada tortuga
	@classmethod
	def inicializar_duraciones(self, archivo):
		duracion_camar = np.random.normal(1.58,1.44,None) #distribucion normal de camar
		duracion_excavar = np.random.normal(12.35,4.92,None) #distribucion normal de excavar
		duracion_poner = np.random.normal(11.64,4.34,None) #distribucion normal de poner
		duracion_tapar = np.random.normal(4.98,3.74,None) #distribucion normal de tapar
		duracion_camuflar = np.random.normal(5.01,1.81,None) #distribucion normal de camuflar
		duracion_vagar = 372-(duracion_camar+duracion_excavar+duracion_poner+duracion_tapar+duracion_camuflar) 
		duraciones.append(duracion_vagar) #duracion de vagar
		duraciones.append(duracion_camar) #duracion de camar, etc...
		duraciones.append(duracion_excavar) 
		duraciones.append(duracion_poner) 
		duraciones.append(duracion_tapar)	
		duraciones.append(duracion_camuflar) 
		
	## este metodo esta directamente relacionado a avanzar y la desviacion estandar de la duracion de cada estado
	## la desviacion estandar es algo diferente para cada tortuga
	@classmethod
	def cambiar_estado(self, archivo):
		if not(proba_desactivarse(self, archivo)):
			if(self.estado == Tortuga.EstadoTortuga.vagar and duracion_actual >= duraciones[0]):
				self.estado = Tortuga.EstadoTortuga.camar
				duracion_actual = 0
			elif(self.estado == Tortuga.EstadoTortuga.camar and duracion_actual >= duraciones[1]):
				self.estado = Tortuga.EstadoTortuga.excavar
				duracion_actual = 0
			elif(self.estado == Tortuga.EstadoTortuga.excavar and duracion_actual >= duraciones[2]):
				self.estado = Tortuga.EstadoTortuga.poner
				duracion_actual = 0
			elif(self.estado == Tortuga.EstadoTortuga.poner and duracion_actual >= duraciones[3]):
				self.estado = Tortuga.EstadoTortuga.tapar
				duracion_actual = 0
			elif(self.estado == Tortuga.EstadoTortuga.tapar and duracion_actual >= duraciones[4]):
				self.estado = Tortuga.EstadoTortuga.camuflar
				
		
	## EFE: avanza la tortuga de acuerdo con su estado
	def avanzar(self):
		return
	
