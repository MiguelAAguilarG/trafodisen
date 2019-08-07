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
}

datos_opcionales_dict = {}

datos_por_defecto_dict = {
'constante_V_por_vuelta_mono': 0.183, 
'constante_V_por_vuelta_tri': 0.076,
'ka': 0.95, #factor de apilamiento
'D_dimension': 0.1905, #m
'J_primario_cobre': 2.6, #A/mm^2
'J_secundario_aluminio': 1.8, #A/mm^2
'espesor_molde': 0.0035, #m
'margen_baja': 0.01, #m
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