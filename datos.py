from math import *

datos_entrada_dict = {
'kva': 45, #kVA
'sistema': 'trifasico', #trifasico/monofasico
'conexion': 'estrella', #delta/estrella
'Vp': 12480, #voltaje primario (volts)
'Vs': 240, #voltaje secundario (volts)
'f': 60, #frecuencia (hertz)
'B': 1.537, #Teslas
'grosor_lamina' : 0.23e-3, #m
'ancho_conductor_baja': 0.1397, #m
'espesor_conductor_baja': 0.00045, #m
'Dc': 1.009687e-3, #m
'kVBIL': 95, #kV
'clase_aislamiento': 15.0, #kV
'factor_carga': 1.0,
'fp': 0.9
}

datos_opcionales_dict = {}

datos_por_defecto_dict = {
'constante_V_por_vuelta_mono': 0.183, 
'constante_V_por_vuelta_tri': 0.076,
'ka': 0.95, #factor de apilamiento
'D_dimension': 0.1905, #m
'J_primario_cobre': 2.6, #A/mm^2
'J_secundario_aluminio': 1.8, #A/mm^2
'espesor_molde': 0.0032, #m
'margen_baja': 0.01, #m
'rho_Al': 2.82e-8, #ohm*m @ 20 °C
'rho_Cu': 1.70e-8, #ohm*m @ 20 °C
'alpha_Al': 3.93e-3,
'alpha_Cu': 3.90e-3,
'T_base': 20, #°C
'T_trabajo': 75, #°C
'densidad_acero': 7650, #kg/m^3
'maximas_perdidas_nucleo': 1.551, #W/kg
'permeabilidad_vacio': pi*4e-7, #N/A^2
}

datos_salida_dict = {
'Vp_linea': None, 
'Vp_fase': None, 
'Vs_linea': None,
'Vs_fase': None,
'Ip_linea': None,
'Ip_fase': None,
'Is_linea': None,
'Is_fase': None,
'V_por_vuelta': None,
'Ac': None,
'Acf': None,
'E_dimension': None,
'no_laminas': None,
'Np': None,
'Ns': None,
'seccion_conductor_primario': None,
'seccion_conductor_secundario': None
}