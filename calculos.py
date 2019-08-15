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
		self.rho_Al = self.datos_por_defecto['rho_Al']
		self.rho_Cu = self.datos_por_defecto['rho_Cu']
		self.T_base = self.datos_por_defecto['T_base']
		self.T_trabajo = self.datos_por_defecto['T_trabajo']
		self.densidad_acero = self.datos_por_defecto['densidad_acero']
		self.maximas_perdidas_nucleo = self.datos_por_defecto['maximas_perdidas_nucleo']
		self.permeabilidad_vacio = self.datos_por_defecto['permeabilidad_vacio']

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
		self.clase_aislamiento = self.datos['clase_aislamiento']
		self.factor_carga = self.datos['factor_carga']
		self.fp = self.datos['fp']

		self.datos_salida_dict = datos_salida_dict

		self.calcular_simple()

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
			self.espesor_aislamiento_conductor_baja = 0.000127
		elif self.espesor_conductor_baja > 0.00089:
			self.espesor_aislamiento_conductor_baja = 0.000254
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

	def calculo_espesor_aislamiento_capa_alta(self):
		if self.kVBIL <= 125:
			if self.V_capa < 23500:
				self.espesor_aislamiento_capa_alta = 0.000254
			elif self.V_capa >= 23500 and self.V_capa < 31500:
				self.espesor_aislamiento_capa_alta = 0.000254 + 0.000127
			elif self.V_capa >= 31500 and self.V_capa < 36000:
				self.espesor_aislamiento_capa_alta = 2*0.000254
			else:
				print('ERROR!. Voltaje entre capas de alta fuera de rango')
		elif self.kVBIL > 125 and self.kVBIL < 200:
			if self.V_capa < 16300:
				self.espesor_aislamiento_capa_alta = 0.000254
			elif self.V_capa >= 16300 and self.V_capa < 21900:
				self.espesor_aislamiento_capa_alta = 0.000254 + 0.000127
			elif self.V_capa >= 21900 and self.V_capa < 25000:
				self.espesor_aislamiento_capa_alta = 2*0.000254
			else:
				print('ERROR!. Voltaje entre capas de alta fuera de rango')
		else:
			print('ERROR!. kVBIL fuera de rango')
		
		return self.espesor_aislamiento_capa_alta

	def calculo_w_bobina_alta(self):
		self.w_bobina_alta = (self.Dc + self.espesor_aislamiento_capa_alta)*self.no_capas_alta + self.E_refuerzo
		
		return self.w_bobina_alta

	def calculo_BAR(self):
		if self.clase_aislamiento == 15.0:
			self.BAR = 5e-3
		elif self.clase_aislamiento == 25.0:
			self.BAR = 7.5e-3
		elif self.clase_aislamiento == 34.5:
			self.BAR = 10e-3
		else:
			print('ERROR!.Clase de aislamiento no corresponde')
		
		return self.BAR

	def calculo_w_total(self):
		self.w_total = self.w_bobina_baja + self.BAR + self.w_bobina_alta + self.BAR
		
		return self.w_total

	def calculo_w_bobina_total(self):
		self.w_bobina_total = self.w_total + self.espesor_molde + 3*0.000254
		
		return self.w_bobina_total

	def calculo_fdB(self):
		if self.sistema == 'trifasico':
			no_fases = 3
		elif self.sistema == 'monofasico':
			no_fases = 1
		else:
			pass

		if self.kva/no_fases >= 5 and self.kva/no_fases <= 15:
			self.fdB = 1.3
		elif self.kva/no_fases == 25:
			self.fdB = 1.4
		elif self.kva/no_fases >= 37.5 and self.kva/no_fases <= 50:
			self.fdB = 1.45
		elif self.kva/no_fases >= 55 and self.kva/no_fases <= 500:
			self.fdB = 1.50
		else:
			pass

		return self.fdB

	def calculo_YBT(self):
		self.YBT = 2*self.w_bobina_total*self.fdB + self.D_dimension

		return self.YBT

	def calculo_sB(self):
		self.sB = self.E_dimension + self.espesor_molde + self.w_bobina_baja/2

		return self.sB

	def calculo_rB(self):
		self.rB = (self.espesor_molde + self.w_bobina_baja/2)*self.fdB

		return self.rB

	def calculo_vuelta_media_baja(self):
		self.vuelta_media_baja = 2*self.L_molde + 2*pi*sqrt((self.rB**2 + self.sB**2)/2)

		return self.vuelta_media_baja

	def calculo_sA(self):
		self.sA = self.E_dimension + self.espesor_molde + self.w_bobina_baja + self.BAR + self.w_bobina_alta/2

		return self.sA

	def calculo_rA(self):
		self.rA = (self.espesor_molde + self.w_bobina_baja + self.BAR + self.w_bobina_alta/2)*self.fdB

		return self.rA

	def calculo_vuelta_media_alta(self):
		self.vuelta_media_alta = 2*self.L_molde + 2*pi*sqrt((self.rA**2 + self.sA**2)/2)

		return self.vuelta_media_alta

	def calculo_vuelta_media(self):
		self.vuelta_media = (self.vuelta_media_baja + self.vuelta_media_alta)/2

		return self.vuelta_media

	def calculo_R_baja(self):
		self.R_baja = self.rho_Al*self.vuelta_media_baja*self.Ns/self.espesor_conductor_baja/self.ancho_conductor_baja

		return self.R_baja

	def calculo_R_alta(self):
		self.R_alta = self.rho_Cu*self.vuelta_media_alta*self.Np/pi/((self.Dc/2)**2)

		return self.R_alta

	def calculo_R_T_trabajo(self, R, alpha):
		self.R_T_trabajo = R*(1+alpha*(self.T_trabajo - self.T_base))

		return self.R_T_trabajo

	def calculo_perdidas_bobina(self, R, I):
		self.perdidas_bobina = R*I**2

		return self.perdidas_bobina

	def calculo_volumen_bobina_baja(self):
		self.volumen_bobina_baja = self.vuelta_media_baja*self.w_bobina_baja*self.ancho_conductor_baja

		return self.volumen_bobina_baja

	def calculo_volumen_bobina_alta(self):
		self.volumen_bobina_alta = self.vuelta_media_alta*self.w_bobina_alta*self.h_bobina_alta

		return self.volumen_bobina_alta

	def calculo_volumen_nucleo(self):
		self.volumen_nucleo = (2*self.E_dimension*(self.h_bobina_baja + self.w_bobina_total) + pi*self.E_dimension**2)*self.D_dimension

		return self.volumen_nucleo

	def calculo_volumen_nucleo_total(self):
		self.volumen_nucleo_total = 2*self.volumen_nucleo

		return self.volumen_nucleo_total

	def calculo_peso_nucleo_total(self):
		self.peso_nucleo_total = self.densidad_acero*self.volumen_nucleo

		return self.peso_nucleo_total

	def calculo_perdidas_nucleo(self):
		self.perdidas_nucleo = self.peso_nucleo_total*self.maximas_perdidas_nucleo

		return self.perdidas_nucleo

	def calculo_eficiencia(self):
		num = self.factor_carga*self.Vs_fase*self.Is_fase*self.fp
		den = num  + self.perdidas_nucleo + self.factor_carga**2*(self.perdidas_bobina_baja + self.perdidas_bobina_baja)
		self.eficiencia = num/den

		return self.eficiencia

	def calculo_porcentaje_corriente_excitacion(self):
		self.porcentaje_corriente_excitacion = self.perdidas_nucleo/10/self.kva

		return self.porcentaje_corriente_excitacion

	def calculo_Xd(self, N):
		factor1 = 1/self.h_bobina_baja*2*pi*self.f*N**2*self.permeabilidad_vacio
		factor2 = 1/3*self.vuelta_media_baja + self.vuelta_media*self.BAR + 1/3*self.vuelta_media_alta*self.w_bobina_alta

		self.Xd = factor1*factor2
		
		return self.Xd

	def calculo_porcentaje_Xd(self, Xd, I):
		self.porcentaje_Xd = I**2*Xd/10/self.kva
		
		return self.porcentaje_Xd

	def calculo_porcentaje_R_BT(self):
		self.porcentaje_R_BT = (self.perdidas_bobina_baja + self.perdidas_bobina_alta)/10/self.kva
		
		return self.porcentaje_R_BT

	def calculo_porcentaje_Z(self):
		self.porcentaje_Z = sqrt(self.porcentaje_R_BT**2 + self.porcentaje_Xd**2)
		
		return self.porcentaje_Z

	def calcular_simple(self):
		aux_voltajes = self.calculo_voltajes()
		aux_corrientes = self.calculo_corrientes()

		self.datos_salida_dict = {
		'Vp_linea': aux_voltajes[0], 
		'Vp_fase': aux_voltajes[1], 
		'Vs_linea': aux_voltajes[2],
		'Vs_fase': aux_voltajes[3],
		'Ip_linea': aux_corrientes[0],
		'Ip_fase': aux_corrientes[1],
		'Is_linea': aux_corrientes[2],
		'Is_fase': aux_corrientes[3],
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
		'espesor_aislamiento_capa_alta': self.calculo_espesor_aislamiento_capa_alta(),
		'BAR':	self.calculo_BAR(),
		'w_bobina_alta': self.calculo_w_bobina_alta(),
		'w_total': self.calculo_w_total(),
		'w_bobina_total': self.calculo_w_bobina_total(),
		'fdB': self.calculo_fdB(),
		'YBT': self.calculo_YBT(),
		'sB': self.calculo_sB(),
		'rB': self.calculo_rB(),
		'vuelta_media_baja': self.calculo_vuelta_media_baja(),
		'sA': self.calculo_sA(),
		'rA': self.calculo_rA(),
		'vuelta_media_alta': self.calculo_vuelta_media_alta(),
		'vuelta_media': self.calculo_vuelta_media(),
		'R_baja': self.calculo_R_baja(),
		'R_alta': self.calculo_R_alta()
		}

		self.R_baja_T_trabajo = self.calculo_R_T_trabajo(self.R_baja, self.rho_Al)
		self.R_alta_T_trabajo = self.calculo_R_T_trabajo(self.R_alta, self.rho_Cu)

		self.datos_salida_dict.update({
		'R_baja_T_trabajo': self.R_baja_T_trabajo,
		'R_alta_T_trabajo': self.R_alta_T_trabajo,
		})

		self.perdidas_bobina_baja = self.calculo_perdidas_bobina(self.R_baja_T_trabajo, self.Is_fase)
		self.perdidas_bobina_alta = self.calculo_perdidas_bobina(self.R_alta_T_trabajo, self.Ip_fase)

		self.datos_salida_dict.update({
		'perdidas_bobina_baja': self.perdidas_bobina_baja,
		'perdidas_bobina_alta': self.perdidas_bobina_alta,
		'volumen_bobina_baja': self.calculo_volumen_bobina_baja(),
		'volumen_bobina_alta': self.calculo_volumen_bobina_alta(),
		'volumen_nucleo': self.calculo_volumen_nucleo(),
		'volumen_nucleo_total': self.calculo_volumen_nucleo_total(),
		'peso_nucleo_total': self.calculo_peso_nucleo_total(),
		'perdidas_nucleo': self.calculo_perdidas_nucleo(),
		'eficiencia': self.calculo_eficiencia(),
		'porcentaje_corriente_excitacion': self.calculo_porcentaje_corriente_excitacion()
		})

		self.Xd_baja = self.calculo_Xd(self.Ns)
		self.Xd_alta = self.calculo_Xd(self.Np)
		self.porcentaje_Xd_baja = self.calculo_porcentaje_Xd(self.Xd_baja, self.Is_fase)
		self.porcentaje_Xd_alta = self.calculo_porcentaje_Xd(self.Xd_alta, self.Ip_fase)

		self.datos_salida_dict.update({
		'Xd_baja': self.Xd_baja,
		'Xd_alta': self.Xd_alta,
		'porcentaje_Xd_baja': self.porcentaje_Xd_baja,
		'porcentaje_Xd_alta': self.porcentaje_Xd_alta,
		'porcentaje_R_BT': self.calculo_porcentaje_R_BT(),
		'porcentaje_Z': self.calculo_porcentaje_Z(),
		})

		return self.datos_salida_dict

if __name__ == '__main__':
	datos = datos.datos_entrada_dict

	trafo = Calculos(datos,0)

	print(trafo.calcular_simple())
