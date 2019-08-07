from math import *
import datos

class Calculos():
	"""docstring for ClassName"""
	def __init__(self, datos, tablas, datos_opcionales = datos.datos_opcionales_dict, 
				datos_por_defecto = datos.datos_por_defecto_dict, datos_salida_dict = datos.datos_salida_dict):

		#datos_por_defecto
		self.datos_por_defecto = datos_por_defecto
		self.constante_V_por_vuelta_mono = self.datos_por_defecto['constante_V_por_vuelta_mono']
		self.constante_V_por_vuelta_tri = self.datos_por_defecto['constante_V_por_vuelta_tri']
		self.ka = self.datos_por_defecto['ka']
		self.D_dimension = self.datos_por_defecto['D_dimension']
		self.J_primario_cobre = self.datos_por_defecto['J_primario_cobre']
		self.J_secundario_aluminio = self.datos_por_defecto['J_secundario_aluminio']
		self.espesor_molde = self.datos_por_defecto['espesor_molde']
		self.margen_baja = self.datos_por_defecto['margen_baja']

		#datos_opcionales
		self.datos_opcionales = datos_opcionales

		#datos
		self.datos = datos
		self.kva = self.datos['kva']
		self.sistema = self.datos['sistema']
		self.conexion = self.datos['conexion']
		self.Vp_linea = self.datos['Vp']
		self.Vs_linea = self.datos['Vs']
		self.f = self.datos['f']
		self.B = self.datos['B']
		self.grosor_lamina = self.datos['grosor_lamina']
		self.ancho_conductor_baja = self.datos['ancho_conductor_baja']
		self.espesor_conductor_baja = self.datos['espesor_conductor_baja']
		self.Dc = self.datos['Dc']
		self.kVBIL = self.datos['kVBIL']

		self.datos_salida_dict = datos_salida_dict

		self.calcular()

	def calculo_voltajes(self):
		if self.sistema == 'trifasico' and self.conexion == 'estrella':
			self.Vp_fase = self.Vp_linea/sqrt(3)
			self.Vs_fase = self.Vs_linea/sqrt(3)
		elif self.sistema == 'trifasico' and self.conexion == 'delta':
			self.Vp_fase = self.Vp_linea
			self.Vs_fase = self.Vs_linea
		else:
			self.Vp_fase = self.Vp_linea
			self.Vs_fase = self.Vs_linea

		return self.Vp_linea, self.Vp_fase, self.Vs_linea, self.Vs_fase

	def calculo_corrientes(self):
		if self.sistema == 'trifasico' and self.conexion == 'estrella':
			self.Ip_linea = self.kva*1000/(sqrt(3)*self.Vp_linea)
			self.Ip_fase = self.Ip_linea

			self.Is_linea = self.kva*1000/(sqrt(3)*self.Vs_linea)
			self.Is_fase = self.Is_linea

		elif self.sistema == 'trifasico' and self.conexion == 'delta':
			self.Vp_fase = self.Vp_linea
			self.Vs_fase = self.Vs_linea

			self.Ip_linea = self.kva*1000/(sqrt(3)*self.Vp_linea)
			self.Ip_fase = self.kva*1000/3/self.Vp_linea
		else:
			self.Ip_linea = self.kva*1000/self.Vp_linea
			self.Ip_fase = self.Ip_linea

			self.Is_linea = self.kva*1000/self.Vs_linea
			self.Is_fase = self.Is_linea

		return self.Ip_linea, self.Ip_fase, self.Is_linea, self.Is_fase

	def calculo_V_por_vuelta(self):

		if self.sistema == 'monofasico':
			self.constante_V_por_vuelta = self.constante_V_por_vuelta_mono
		if self.sistema == 'trifasico':
			self.constante_V_por_vuelta = self.constante_V_por_vuelta_tri

		self.V_por_vuelta = self.constante_V_por_vuelta*sqrt(self.f*self.kva)

		return self.V_por_vuelta

	def calculo_Ac(self):
		self.Ac = self.V_por_vuelta/(4.44*self.f*self.B)

		return self.Ac

	def calculo_Acf(self):
		self.Acf = self.Ac/self.ka

		return self.Acf

	def calculo_E_dimension(self):
		self.E_dimension = self.Acf/(2*self.D_dimension)

		return self.E_dimension

	def calculo_no_laminas(self):
		self.no_laminas = ceil(self.E_dimension/self.grosor_lamina)

		return self.no_laminas

	def calculo_Np(self):
		self.Np = ceil(self.Vp_fase/self.V_por_vuelta)

		return self.Np

	def calculo_Ns(self):
		self.Ns = ceil(self.Vs_fase/self.V_por_vuelta)

		return self.Ns

	def calculo_seccion_conductor_primario(self):
		self.seccion_conductor_primario = self.Ip_fase/self.J_primario_cobre

		return self.seccion_conductor_primario

	def calculo_seccion_conductor_secundario(self):
		self.seccion_conductor_secundario = self.Is_fase/self.J_secundario_aluminio

		return self.seccion_conductor_secundario

	def calculo_W_molde(self):
		self.W_molde = 2*self.E_dimension + 2*self.espesor_molde

		return self.W_molde

	def calculo_L_molde(self):
		self.L_molde = self.D_dimension + 2*self.espesor_molde
		
		return self.L_molde
	
	def calculo_h_bobina_baja(self):
		self.h_bobina_baja = self.ancho_conductor_baja + 2*self.margen_baja
		
		return self.h_bobina_baja

	def calculo_espesor_aislamiento_baja(self):
		if self.espesor_conductor_baja <= 0.00089:
			self.espesor_aislamiento_conductor_baja = 0.127
		elif self.espesor_conductor_baja > 0.00089:
			self.espesor_aislamiento_conductor_baja = 0.254
		else:
			print('ERROR!. Espesor del conductor de baja tensión fuera de rango')

		return self.espesor_aislamiento_conductor_baja

	def calculo_w_bobina_baja(self):
		self.w_bobina_baja = (self.espesor_conductor_baja + self.espesor_aislamiento_conductor_baja)*self.Ns
		
		return self.w_bobina_baja

	def calculo_margen_alta(self):
		if self.Vp_linea <= 15000:
			self.margen_alta = 9.52e-3
		elif self.Vp_linea <= 25000:
			self.margen_alta = 19.0e-3
		elif self.Vp_linea <= 34500:
			self.margen_alta = 38.1e-3
		else:
			print('ERROR!. Voltaje fuera de rango')

		return self.margen_alta

	def calculo_h_bobina_alta(self):
		self.h_bobina_alta = self.h_bobina_baja - 2*self.margen_alta

		return self.h_bobina_alta

	def calculo_no_vueltas_capa(self):
		self.no_vueltas_capa = floor(self.h_bobina_alta/self.Dc)
	
		return self.no_vueltas_capa

	def calculo_no_capas_alta(self):
		self.no_capas_alta = ceil(self.Np/self.no_vueltas_capa)
		
		return self.no_capas_alta

	def calculo_V_capa(self):
		self.V_capa = 2*self.no_vueltas_capa/self.Np*self.kVBIL*1000
		
		return self.V_capa

	def calculo_E_refuerzo(self):
		if self.Vp_linea <= 15000:
			self.E_refuerzo = 1.778e-3
		elif self.Vp_linea <= 25000:
			self.E_refuerzo = 3.302e-3
		elif self.Vp_linea <= 34500:
			self.E_refuerzo = 3.302e-3
		else:
			print('ERROR!. Voltaje fuera de rango')
		
		return self.E_refuerzo

	def calcular(self):
		self.datos_salida_dict = {
		'Vp_linea': self.calculo_voltajes()[0], 
		'Vp_fase': self.calculo_voltajes()[1], 
		'Vs_linea': self.calculo_voltajes()[2],
		'Vs_fase': self.calculo_voltajes()[3],
		'Ip_linea': self.calculo_corrientes()[0],
		'Ip_fase': self.calculo_corrientes()[1],
		'Is_linea': self.calculo_corrientes()[2],
		'Is_fase': self.calculo_corrientes()[3],
		'V_por_vuelta': self.calculo_V_por_vuelta(),
		'Ac': self.calculo_Ac(),
		'Acf': self.calculo_Acf(),
		'E_dimension': self.calculo_E_dimension(),
		'no_laminas': self.calculo_no_laminas(),
		'Np': self.calculo_Np(),
		'Ns': self.calculo_Ns(),
		'seccion_conductor_primario': self.calculo_seccion_conductor_primario(),
		'seccion_conductor_secundario': self.calculo_seccion_conductor_secundario(),
		'W_molde': self.calculo_W_molde(),
		'L_molde': self.calculo_L_molde(),
		'h_bobina_baja': self.calculo_h_bobina_baja(),
		'espesor_aislamiento_baja': self.calculo_espesor_aislamiento_baja(),
		'w_bobina_baja': self.calculo_w_bobina_baja(),
		'margen_alta': self.calculo_margen_alta(),
		'h_bobina_alta': self.calculo_h_bobina_alta(),
		'no_vueltas_capa': self.calculo_no_vueltas_capa(),
		'no_capas_alta': (self).calculo_no_capas_alta(),
		'V_capa': self.calculo_V_capa(),
		'E_refuerzo': self.calculo_E_refuerzo(),
		}

		return self.datos_salida_dict

if __name__ == '__main__':
	datos = datos.datos_entrada_dict

	trafo = Calculos(datos,0)

	print(trafo.calcular())
