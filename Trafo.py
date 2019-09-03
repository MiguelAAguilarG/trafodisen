from calculos import Calculos
from calculos import datos

class Trafo(Calculos):
	"""docstring for ClassName"""
	def __init__(self, datos, datos_opcionales = datos.datos_opcionales_dict, datos_por_defecto = datos.datos_por_defecto_dict, datos_salida_dict = datos.datos_salida_dict):

		#datos_por_defecto
		self.datos_por_defecto = datos_por_defecto

		self.ancho_lamina_aluminio_list = self.datos_por_defecto['ancho_lamina_aluminio_list']
		self.Dc_list = self.datos_por_defecto['Dc_list']
		self.espesor_lamina_aluminio_list = self.datos_por_defecto['espesor_lamina_aluminio_list']
		self.D_dimension_dict = self.datos_por_defecto['D_dimension_dict']
		self.laminas_acero_dict = self.datos_por_defecto['laminas_acero_dict']

		self.constante_V_por_vuelta_mono = self.datos_por_defecto['constante_V_por_vuelta_mono']
		self.constante_V_por_vuelta_tri = self.datos_por_defecto['constante_V_por_vuelta_tri']
		self.ka = self.datos_por_defecto['ka']
		self.redondeo_N = self.datos_por_defecto['redondeo_N']
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
		self.fdB_list = self.datos_por_defecto['fdB_list']
		self.Vm_list = self.datos_por_defecto['Vm_list']
		self.Vw_ImpulsoRayo_list = self.datos_por_defecto['Vw_ImpulsoRayo_list']
		self.pasos_perdidas_nucleo = self.datos_por_defecto['pasos_perdidas_nucleo']
		self.perdidas_nucleo_dict =  self.datos_por_defecto['perdidas_nucleo_dict']

		#datos_opcionales
		self.datos_opcionales = datos_opcionales
		if isinstance(self.datos_opcionales, dict) and self.datos_opcionales:
			self.consideracion_hw = self.datos_opcionales.get('consideracion_hw')
			self.consideracion_DE = self.datos_opcionales.get('consideracion_DE')
			self.consideracion_B = self.datos_opcionales.get('consideracion_B')
			self.consideracion_perdidas_nucleo = self.datos_opcionales.get('consideracion_perdidas_nucleo')
			self.porcentaje_Z_garantia = self.datos_opcionales.get('porcentaje_Z_garantia')
			self.eficiencia_garantia = self.datos_opcionales.get('eficiencia_garantia')
			self.paso_DE = self.datos_opcionales.get('paso_DE')
			self.paso_B = self.datos_opcionales.get('paso_B')

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
		self.factor_carga = self.datos['factor_carga']
		self.fp = self.datos['fp']

		self.datos_salida_dict = datos_salida_dict

	def base_1(self):
		#self.calculo_voltajes()
		#self.calculo_corrientes()

		#self.calculo_V_por_vuelta()
		#self.calculo_Ac()
		#self.calculo_Acf()
		#self.calculo_D_dimension()
		#self.calculo_E_dimension()
		#self.calculo_grosor_lamina()
		#self.calculo_no_laminas()
		#self.calculo_Np()
		#self.calculo_Ns()
		#self.calculo_N_ajuste()

		self.calculo_seccion_conductor_primario()
		self.calculo_seccion_conductor_secundario()
		self.calculo_Dc()
		self.calculo_lamina_aluminio()
		self.calculo_W_molde()
		self.calculo_L_molde()
		self.calculo_h_bobina_baja()
		self.calculo_espesor_aislamiento_baja()
		self.calculo_w_bobina_baja()
		self.calculo_clase_aislamiento()
		self.calculo_margen_alta()
		self.calculo_h_bobina_alta()
		self.calculo_no_vueltas_capa()
		self.calculo_no_capas_alta()
		self.calculo_kVBIL()
		self.calculo_V_capa()
		self.calculo_E_refuerzo()
		self.calculo_espesor_aislamiento_capa_alta()
		if self.error_espesor_aislamiento_capa_alta == False:
			self.calculo_BAR()
			self.calculo_w_bobina_alta()
			self.calculo_w_total()
			self.calculo_w_bobina_total()
			self.calculo_fdB()
			self.calculo_YBT()
			self.calculo_sB()
			self.calculo_rB()
			self.calculo_vuelta_media_baja()
			self.calculo_sA()
			self.calculo_rA()
			self.calculo_vuelta_media_alta()
			self.calculo_vuelta_media()
			self.calculo_R_baja()
			self.calculo_R_alta()

			self.R_baja_T_trabajo = self.calculo_R_T_trabajo(self.R_baja, self.rho_Al)
			self.R_alta_T_trabajo = self.calculo_R_T_trabajo(self.R_alta, self.rho_Cu)

			self.perdidas_bobina_baja = self.calculo_perdidas_bobina(self.R_baja_T_trabajo, self.Is_fase)
			self.perdidas_bobina_alta = self.calculo_perdidas_bobina(self.R_alta_T_trabajo, self.Ip_fase)

			self.calculo_volumen_bobina_baja()
			self.calculo_volumen_bobina_alta()
			self.calculo_volumen_nucleo()
			self.calculo_volumen_nucleo_total()
			self.calculo_peso_nucleo_total()
			self.calculo_perdidas_nucleo()
			self.calculo_eficiencia()
			self.calculo_porcentaje_corriente_excitacion()

			self.Xd_baja = self.calculo_Xd(self.Ns)
			self.Xd_alta = self.calculo_Xd(self.Np)
			self.porcentaje_Xd_baja = self.calculo_porcentaje_Xd(self.Xd_baja, self.Is_fase)
			self.porcentaje_Xd_alta = self.calculo_porcentaje_Xd(self.Xd_alta, self.Ip_fase)

			self.calculo_porcentaje_R_BT()
			self.calculo_porcentaje_Z()

	def completo(self):
		self.calculo_voltajes()
		self.calculo_corrientes()

		self.calculo_D_dimension()
		self.calculo_grosor_lamina()

		self.calculo_V_por_vuelta()
		self.calculo_Ac()
		self.calculo_Acf()
		self.calculo_E_dimension()

		self.calculo_no_laminas()
		self.calculo_Np()
		self.calculo_Ns()
		self.calculo_N_ajuste()

		self.base_1()
		if self.error_espesor_aislamiento_capa_alta == False:
			self.generador_datos_salida_dict()

			return self.datos_salida_dict

	def iterativo(self):
		self.calculo_voltajes()
		self.calculo_corrientes()

		self.calculo_D_dimension()

		self.calculo_grosor_lamina()

		d_DE = self.consideracion_DE[1] - self.consideracion_DE[0]
		c_DE = int(d_DE/self.paso_DE)

		d_B = self.consideracion_B[1] - self.consideracion_B[0]
		c_B = int(d_B/self.paso_B)

		resultados_validos = 0
		for self.DE in [round(self.consideracion_DE[0]+x*self.paso_DE,5) for x in range(c_DE+1) if round(self.consideracion_DE[0]+x*self.paso_DE,5) <= self.consideracion_DE[1]]:
			print('D/E =', self.DE)
			for self.B in [round(self.consideracion_B[0]+x*self.paso_B,5) for x in range(c_B+1) if round(self.consideracion_B[0]+x*self.paso_B,5) <= self.consideracion_B[1]]:
				print('B =', self.B)
				self.calculo_E_dimension()
				self.calculo_Acf()
				self.calculo_Ac()
				self.calculo_Np()
				self.calculo_Ns()
				self.calculo_N_ajuste()

				self.calculo_no_laminas()
				self.calculo_V_por_vuelta()

				self.base_1()
				if self.error_espesor_aislamiento_capa_alta == False:
					if (self.porcentaje_Z_garantia[0] <= self.porcentaje_Z) and (self.porcentaje_Z_garantia[1] >= self.porcentaje_Z):
						print(self.generador_datos_salida_dict())
						resultados_validos = resultados_validos + 1

		print('resultados_validos =', resultados_validos)
							
	def generador_datos_salida_dict(self):
		self.datos_salida_dict = {
		'Vp_linea': self.Vp_linea, 
		'Vp_fase': self.Vp_fase, 
		'Vs_linea': self.Vs_linea,
		'Vs_fase': self.Vs_fase,
		'Ip_linea': self.Ip_linea,
		'Ip_fase': self.Ip_fase,
		'Is_linea': self.Is_linea,
		'Is_fase': self.Is_fase,
		'V_por_vuelta': self.V_por_vuelta,
		'Ac': self.Ac,
		'Acf': self.Ac,
		'D_dimension': self.D_dimension,
		'E_dimension': self.E_dimension,
		'tipo_lamina': self.tipo_lamina,
		'grosor_lamina': self.grosor_lamina,
		'no_laminas': self.no_laminas,
		'Np_sin_ajustar': self.Np_sin_ajustar,
		'Ns_sin_ajustar': self.Ns_sin_ajustar,
		'Np': self.Np,
		'Ns': self.Ns,
		'seccion_conductor_primario': self.seccion_conductor_primario,
		'seccion_conductor_secundario': self.seccion_conductor_secundario,
		'Dc': self.Dc,
		'Dc_seccion': self.Dc_seccion,
		'ancho_conductor_baja': self.ancho_conductor_baja,
		'espesor_conductor_baja': self.espesor_conductor_baja,
		'conductor_baja_seccion': self.conductor_baja_seccion,
		'W_molde': self.W_molde,
		'L_molde': self.L_molde,
		'h_bobina_baja': self.h_bobina_baja,
		'espesor_aislamiento_conductor_baja': self.espesor_aislamiento_conductor_baja,
		'w_bobina_baja': self.w_bobina_baja,
		'clase_aislamiento': self.clase_aislamiento,
		'margen_alta': self.margen_alta,
		'h_bobina_alta': self.h_bobina_alta,
		'no_vueltas_capa': self.no_vueltas_capa,
		'no_capas_alta': self.no_capas_alta,
		'kVBIL': self.kVBIL,
		'V_capa': self.V_capa,
		'E_refuerzo': self.E_refuerzo,
		'espesor_aislamiento_capa_alta': self.espesor_aislamiento_capa_alta,
		'BAR':	self.BAR,
		'w_bobina_alta': self.w_bobina_alta,
		'w_total': self.w_total,
		'w_bobina_total': self.w_bobina_total,
		'fdB': self.fdB,
		'YBT': self.YBT,
		'sB': self.sB,
		'rB': self.rB,
		'vuelta_media_baja': self.vuelta_media_baja,
		'sA': self.sA,
		'rA': self.rA,
		'vuelta_media_alta': self.vuelta_media_alta,
		'vuelta_media': self.vuelta_media,
		'R_baja': self.R_baja,
		'R_alta': self.R_alta,
		'R_baja_T_trabajo': self.R_baja_T_trabajo,
		'R_alta_T_trabajo': self.R_alta_T_trabajo,
		'perdidas_bobina_baja': self.perdidas_bobina_baja,
		'perdidas_bobina_alta': self.perdidas_bobina_alta,
		'volumen_bobina_baja': self.volumen_bobina_baja,
		'volumen_bobina_alta': self.volumen_bobina_alta,
		'volumen_nucleo': self.volumen_nucleo,
		'volumen_nucleo_total': self.volumen_nucleo_total,
		'peso_nucleo_total': self.peso_nucleo_total,
		'perdidas_nucleo': self.perdidas_nucleo,
		'perdidas_nucleo_W_libras': self.perdidas_nucleo_W_libras,
		'eficiencia': self.eficiencia,
		'porcentaje_corriente_excitacion': self.porcentaje_corriente_excitacion,
		'Xd_baja': self.Xd_baja,
		'Xd_alta': self.Xd_alta,
		'porcentaje_Xd_baja': self.porcentaje_Xd_baja,
		'porcentaje_Xd_alta': self.porcentaje_Xd_alta,
		'porcentaje_R_BT': self.porcentaje_R_BT,
		'porcentaje_Z': self.porcentaje_Z,
		}

		return self.datos_salida_dict

if __name__ == '__main__':
	from math import sqrt
	import datos

	datos = datos.datos_entrada_dict

	trafo = Trafo(datos)

	print(trafo.iterativo())
