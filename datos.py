from math import *

datos_entrada_dict = {
'kva': 45, #kVA
'sistema': 'trifasico', #trifasico/monofasico
'conexion': 'estrella', #delta/estrella
'Vp': 12480, #voltaje primario (volts)
'Vs': 240, #voltaje secundario (volts)
'f': 60, #frecuencia (hertz)
'B': 1.537, #Teslas
'grosor_lamina' : 'M3', #m
'factor_carga': 1.0,
'fp': 0.9
}

datos_opcionales_dict = {
'consideracion_1': [2,5], # <= h_molde/w_molde <=
'consideracion_2': [1.5,6.5], # <= D_dimension/E_dimension <= 
}

datos_por_defecto_dict = {
'ancho_lamina_aluminio_list': [114.3e-3, 139.7e-3, 152.4e-3, 158.7e-3, 203.2e-3, 254e-3, 254e-3], #m
'espesor_lamina_aluminio_list': [0.3e-3, 0.45e-3, 0.55e-3, 0.89e-3, 0.89e-3, 1.24e-3, 1.78e-3], #m
'Dc_list': [0.0799e-3, 0.0897e-3, 0.1007e-3, 0.1131e-3, 0.127e-3, 0.1426e-3, 
0.1601e-3, 0.1798e-3, 0.2019e-3, 0.2268e-3, 0.2546e-3, 0.2859e-3, 0.3211e-3, 0.3606e-3, 
0.4049e-3, 0.4547e-3, 0.5106e-3, 0.5733e-3, 0.6438e-3, 0.7229e-3, 0.8118e-3, 0.9116e-3, 
1.0237e-3, 1.1495e-3, 1.2908e-3, 1.4495e-3, 1.6277e-3, 1.8278e-3, 2.0525e-3, 2.3048e-3, 
2.5881e-3, 2.9063e-3, 3.2636e-3, 3.6648e-3, 4.1153e-3, 4.6212e-3, 5.1893e-3, 5.8272e-3, 
6.5436e-3, 7.348e-3, 8.2513e-3, 9.2657e-3, 10.405e-3, 11.684e-3], #m
'D_dimension_dict': {
152.4e-3: {'monofasico': [5,15], 'trifasico': [15,30,50]}, 
190.5e-3: {'monofasico': [25,37.5], 'trifasico': [45,75]}, 
203.2e-3: {'monofasico': [50,167], 'trifasico': [112.5,300]},
304.8e-3: {'monofasico': [], 'trifasico': [500,1500]}
}, #keys (m) values kVA
'laminas_acero_dict': {'M3': 0.23e-3, 'M4': 0.27e-3, 'M5': 0.30e-3, 'M6': 0.35e-3}, #m

'constante_V_por_vuelta_mono': 0.183, 
'constante_V_por_vuelta_tri': 0.076,
'ka': 0.95, #factor de apilamiento
'redondeo_N': 2, #decimales
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
'fdB_list': [1.3, 1.4, 1.45, 1.50], #4 elementos
'Vm_list': [3.6, 7.2, 12, 17.5, 24, 36],
'Vw_ImpulsoRayo_list': [20, 40, 60, 95, 145, 170],
}

datos_salida_dict = {}