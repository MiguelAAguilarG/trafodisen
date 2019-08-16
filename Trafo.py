from calculos import *

class Trafo(Calculos):
	"""docstring for ClassName"""
	def __init__(self, datos, datos_opcionales = datos.datos_opcionales_dict, 
				 datos_por_defecto = datos.datos_por_defecto_dict, datos_salida_dict = datos.datos_salida_dict):

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

		#datos_opcionales
		self.datos_opcionales = datos_opcionales
		if isinstance(self.datos_opcionales, dict) and self.datos_opcionales:
			self.consideracion_1 = self.datos_opcionales['consideracion_1']
			self.consideracion_2 = self.datos_opcionales['consideracion_2']

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

	def completo(self):
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
		'D_dimension': self.calculo_D_dimension(),
		'E_dimension': self.calculo_E_dimension(),
		'grosor_lamina': self.calculo_grosor_lamina(),
		'no_laminas': self.calculo_no_laminas(),
		'Np_sin_ajustar': self.calculo_Np(),
		'Ns_sin_ajustar': self.calculo_Ns(),
		'Np': self.calculo_N_ajuste()[0],
		'Ns': self.Ns,
		'seccion_conductor_primario': self.calculo_seccion_conductor_primario(),
		'seccion_conductor_secundario': self.calculo_seccion_conductor_secundario(),
		'Dc': self.calculo_Dc()[0],
		'Dc_seccion': self.Dc_seccion,
		'ancho_conductor_baja': self.calculo_lamina_aluminio()[0],
		'espesor_conductor_baja': self.espesor_conductor_baja,
		'conductor_baja_seccion': self.conductor_baja_seccion,
		'W_molde': self.calculo_W_molde(),
		'L_molde': self.calculo_L_molde(),
		'h_bobina_baja': self.calculo_h_bobina_baja(),
		'espesor_aislamiento_baja': self.calculo_espesor_aislamiento_baja(),
		'w_bobina_baja': self.calculo_w_bobina_baja(),
		'clase_aislamiento': self.calculo_clase_aislamiento(),
		'margen_alta': self.calculo_margen_alta(),
		'h_bobina_alta': self.calculo_h_bobina_alta(),
		'no_vueltas_capa': self.calculo_no_vueltas_capa(),
		'no_capas_alta': (self).calculo_no_capas_alta(),
		'kVBIL': self.calculo_kVBIL(),
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
	from math import *
	import datos

	datos = datos.datos_entrada_dict

	trafo = Trafo(datos)

	print(trafo.completo())
