#!/usr/bin/python3
import enum
import numpy as np	# para generar números al azar según distribución estándar
import json			# para crear una hilera json en toJSON()

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
		self.estado = Tortuga.EstadoTortuga.vagar
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
		
	## EFE: avanza la tortuga de acuerdo con su estado
	def avanzar(self):
		return
