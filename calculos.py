from math import sqrt, pi, ceil, floor
import datos

class Calculos():
	"""docstring for ClassName"""
	def __init__(self):
		pass

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
		if self.consideracion_DE:
			self.V_por_vuelta = self.Vp_fase/self.Np
		else:
			if self.sistema == 'monofasico':
				self.constante_V_por_vuelta = self.constante_V_por_vuelta_mono
			elif self.sistema == 'trifasico':
				self.constante_V_por_vuelta = self.constante_V_por_vuelta_tri

			self.V_por_vuelta = self.constante_V_por_vuelta*sqrt(self.f*self.kva)

		return self.V_por_vuelta

	def calculo_Ac(self):
		if self.consideracion_DE:
			self.Ac = self.Acf*self.ka
		else:
			self.Ac = self.V_por_vuelta/(4.44*self.f*self.B)

		return self.Ac

	def calculo_Acf(self):
		if self.consideracion_DE:
			self.Acf = self.D_dimension*(2*self.E_dimension)
		else:
			self.Acf = self.Ac/self.ka

		return self.Acf

	def calculo_D_dimension(self):
		for D_dimension, sistema_kva_dict in self.D_dimension_dict.items():
			for sistema, kva_list in sistema_kva_dict.items():
				if self.sistema == sistema:
					tam = len(kva_list)
					for indice_rango in [2*x for x in range(int(len(kva_list[0])/2))]:
						if (self.kva >= kva_list[0][indice_rango] and self.kva <= kva_list[0][indice_rango+1]):
							self.D_dimension = D_dimension
					if tam == 2:
						if self.kva in kva_list[1]:
							self.D_dimension = D_dimension

		return self.D_dimension

	def calculo_E_dimension(self):
		if self.consideracion_DE:
			self.E_dimension = self.D_dimension/self.DE
		else:
			self.E_dimension = self.Acf/(2*self.D_dimension)

		return self.E_dimension

	def calculo_grosor_lamina(self):
		if isinstance(self.grosor_lamina, str):
			for tipo_lamina, grosor_lamina in self.laminas_acero_dict.items():
				if self.grosor_lamina == tipo_lamina:
					self.grosor_lamina = grosor_lamina
					self.tipo_lamina = tipo_lamina

		return self.tipo_lamina, self.grosor_lamina

	def calculo_no_laminas(self):
		self.no_laminas = ceil(self.E_dimension/self.grosor_lamina)

		return self.no_laminas

	def calculo_Np(self):
		if self.consideracion_DE:
			self.Np = round(self.Vp_fase/(4.44*self.f*self.B*self.Ac))
		else:
			self.Np = round(self.Vp_fase/self.V_por_vuelta)

		self.Np_sin_ajustar = self.Np
		
		return self.Np, self.Np_sin_ajustar

	def calculo_Ns(self):
		if self.consideracion_DE:
			self.Ns = round(self.Vs_fase/(4.44*self.f*self.B*self.Ac))
		else:
			self.Ns = round(self.Vs_fase/self.V_por_vuelta)

		self.Ns_sin_ajustar = self.Ns

		return self.Ns, self.Ns_sin_ajustar

	def calculo_N_ajuste(self):
		TTR_V = self.Vp_fase/self.Vs_fase
		TTR_N = self.Np/self.Ns

		while round(TTR_V,self.redondeo_N) != round(TTR_N,self.redondeo_N):
			if round(TTR_V,self.redondeo_N) >= round(TTR_N,self.redondeo_N):
				self.Np = self.Np + 1
			else:
				self.Np = self.Np - 1

			TTR_V = self.Vp_fase/self.Vs_fase
			TTR_N = self.Np/self.Ns

		return self.Np, self.Ns

	def calculo_seccion_conductor_primario(self):
		self.seccion_conductor_primario = self.Ip_fase/self.J_primario_cobre*1e-6

		return self.seccion_conductor_primario

	def calculo_seccion_conductor_secundario(self):
		self.seccion_conductor_secundario = self.Is_fase/self.J_secundario_aluminio*1e-6

		return self.seccion_conductor_secundario

	def calculo_Dc(self):
		Area_D_conductor_list = [pi*(x/2)**2 for x in self.Dc_list]
		
		for x, Area_D_conductor in enumerate(Area_D_conductor_list):
			if Area_D_conductor >= self.seccion_conductor_primario:
				self.Dc = self.Dc_list[x]
				self.Dc_seccion = Area_D_conductor_list[x]
				break

		return self.Dc, self.Dc_seccion

	def calculo_lamina_aluminio(self):

		seccion_lamina_aluminio_list = [self.ancho_lamina_aluminio_list[x]*self.espesor_lamina_aluminio_list[x] for x in range(len(self.ancho_lamina_aluminio_list))]
		
		for x, seccion_lamina_aluminio in enumerate(seccion_lamina_aluminio_list):
			if seccion_lamina_aluminio >= self.seccion_conductor_secundario:
				self.ancho_conductor_baja = self.ancho_lamina_aluminio_list[x]
				self.espesor_conductor_baja = self.espesor_lamina_aluminio_list[x]
				self.conductor_baja_seccion = seccion_lamina_aluminio_list[x]
				break

		return self.ancho_conductor_baja, self.espesor_conductor_baja, self.conductor_baja_seccion

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

	def calculo_clase_aislamiento(self):
		if self.Vp_linea <= 15000:
			self.clase_aislamiento = 15
		elif self.Vp_linea <= 25000:
			self.clase_aislamiento = 25
		elif self.Vp_linea <= 34500:
			self.clase_aislamiento = 34.5
		else:
			print('ERROR! Voltaje nominal fuera de rango')

		return self.clase_aislamiento

	def calculo_margen_alta(self):
		if self.clase_aislamiento <= 15:
			self.margen_alta = 9.52e-3
		elif self.clase_aislamiento <= 25:
			self.margen_alta = 19.0e-3
		elif self.clase_aislamiento <= 34.5:
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

	def calculo_kVBIL(self):
		for x, Vm in enumerate(self.Vm_list):
			if self.Vp_linea/1000 <= Vm:
				self.kVBIL = self.Vw_ImpulsoRayo_list[x]
				break		
		else:
			print('ERROR!. Voltaje fuera de rango')
		
		return self.kVBIL

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
		self.error_espesor_aislamiento_capa_alta = False

		if self.kVBIL <= 125:
			if self.V_capa < 23500:
				self.espesor_aislamiento_capa_alta = 0.000254
			elif self.V_capa >= 23500 and self.V_capa < 31500:
				self.espesor_aislamiento_capa_alta = 0.000254 + 0.000127
			elif self.V_capa >= 31500 and self.V_capa < 36000:
				self.espesor_aislamiento_capa_alta = 2*0.000254
			else:
				print('ERROR!. Voltaje entre capas de alta fuera de rango')
				self.error_espesor_aislamiento_capa_alta = True
		elif self.kVBIL > 125 and self.kVBIL < 200:
			if self.V_capa < 16300:
				self.espesor_aislamiento_capa_alta = 0.000254
			elif self.V_capa >= 16300 and self.V_capa < 21900:
				self.espesor_aislamiento_capa_alta = 0.000254 + 0.000127
			elif self.V_capa >= 21900 and self.V_capa < 25000:
				self.espesor_aislamiento_capa_alta = 2*0.000254
			else:
				print('ERROR!. Voltaje entre capas de alta fuera de rango')
				self.error_espesor_aislamiento_capa_alta = True
		else:
			print('ERROR!. kVBIL fuera de rango')
			self.error_espesor_aislamiento_capa_alta = True
		
		return self.espesor_aislamiento_capa_alta, self.error_espesor_aislamiento_capa_alta

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
			self.fdB = self.fdB_list[0]
		elif self.kva/no_fases == 25:
			self.fdB = self.fdB_list[1]
		elif self.kva/no_fases >= 37.5 and self.kva/no_fases <= 50:
			self.fdB = self.fdB_list[2]
		elif self.kva/no_fases >= 55 and self.kva/no_fases <= 500:
			self.fdB = self.fdB_list[3]
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
		if self.consideracion_perdidas_nucleo == 'valor':
			self.perdidas_nucleo = self.peso_nucleo_total*self.maximas_perdidas_nucleo
		elif self.consideracion_perdidas_nucleo == 'lista':
			Wlb_lista = self.perdidas_nucleo_dict[self.tipo_lamina][self.f]
			Teslas_lista = self.pasos_perdidas_nucleo

			for indice_Teslas, Teslas in enumerate(Teslas_lista):
				if Teslas >= self.B:
					y1 = Wlb_lista[indice_Teslas-1]
					y2 = Wlb_lista[indice_Teslas]
					x1 = Teslas_lista[indice_Teslas-1]
					x2 = Teslas_lista[indice_Teslas]
					break

			self.perdidas_nucleo_W_libras = (y2-y1)/(x2-x1)*(self.B-x1) + y1
			self.perdidas_nucleo = self.perdidas_nucleo_W_libras*self.peso_nucleo_total/0.4535

		return self.perdidas_nucleo, self.perdidas_nucleo_W_libras

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