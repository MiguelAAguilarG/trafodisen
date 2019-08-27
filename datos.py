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
'consideracion_hw': [2.0, 5.0], # <= h_molde/w_molde <=
'consideracion_DE': [1.5, 6.5], # <= D_dimension/E_dimension <=
'consideracion_B': [0.5, 1.8], # <= B <= 
'consideracion_perdidas_nucleo': 'lista', # 'valor': 'maximas_perdidas_nucleo', 'lista': 'perdidas_nucleo_dict'
'porcentaje_Z_garantia': [3, 10],
'eficiencia_garantia': [0.95, 1.0],
'paso_DE': 0.1,
'paso_B': 0.1,
}

#Caso base
'''datos_opcionales_dict = {
'consideracion_hw': [2.0, 5.0], # <= h_molde/w_molde <=
'consideracion_DE': [1.5, 6.5], # <= D_dimension/E_dimension <=
'consideracion_B': [0.5, 1.8], # <= B <= 
'consideracion_perdidas_nucleo': 'lista', # 'valor': 'maximas_perdidas_nucleo', 'lista': 'perdidas_nucleo_dict'
'porcentaje_Z_garantia': [3, 10],
'eficiencia_garantia': [0.95, 1.0],
'paso_DE': 0.1,
'paso_B': 0.1,
}'''

#para no hacerlo iterativo
'''datos_opcionales_dict = {
'consideracion_hw': [], # <= h_molde/w_molde <=
'consideracion_DE': [], # <= D_dimension/E_dimension <=
'consideracion_B': [], # <= B <= 
'consideracion_perdidas_nucleo': 'lista', # 'valor': 'maximas_perdidas_nucleo', 'lista': 'perdidas_nucleo_dict'
'porcentaje_Z_garantia': [],
'eficiencia_garantia': [],
'paso_DE': 0.1,
'paso_B': 0.1,
}'''

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
152.4e-3: {'monofasico': [[5,15]], 'trifasico': [[15,30],[50]]}, 
190.5e-3: {'monofasico': [[25,37.5]], 'trifasico': [[45,75]]}, 
203.2e-3: {'monofasico': [[50,167]], 'trifasico': [[112.5,300]]},
304.8e-3: {'monofasico': [[]], 'trifasico': [[500,1500]]}
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
'pasos_perdidas_nucleo': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 0.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9], #Teslas
'perdidas_nucleo_dict':
{
'M3':
{
50: [0.00147, 0.00257, 0.0125, 0.0218, 0.0336, 0.0477, 0.064, 0.0829, 0.104, 0.128, 0.154, 0.183, 0.217, 0.255, 0.303, 0.363, 0.455, 0.609, 0.795],
60: [0.00192, 0.00742, 0.0163, 0.0285, 0.0438, 0.062, 0.0834, 0.108, 0.135, 0.166, 0.2, 0.238, 0.282, 0.33, 0.393, 0.467, 0.58, 0.773, 0.999],
},
'M4':
{
50: [0.00183, 0.00702, 0.0152, 0.0265, 0.04, 0.0564, 0.0753, 0.0968, 0.12, 0.148, 0.179, 0.214, 0.253, 0.298, 0.353, 0.418, 0.514, 0.658, 0.77],
60: [0.00242, 0.00928, 0.0202, 0.0347, 0.0528, 0.0742, 0.099, 0.127, 0.159, 0.195, 0.236, 0.28, 0.333, 0.39, 0.462, 0.546, 0.666, 0.845, 0.99],
},
'M5':
{
50: [0.00195, 0.00757, 0.0165, 0.0286, 0.0437, 0.0617, 0.0828, 0.107, 0.134, 0.165, 0.199, 0.238, 0.28, 0.33, 0.39, 0.462, 0.566, 0.719, 0.898],
60: [0.00259, 0.01, 0.022, 0.038, 0.058, 0.0819, 0.11, 0.142, 0.178, 0.218, 0.263, 0.314, 0.37, 0.435, 0.513, 0.605, 0.736, 0.93, 1.15],
},
'M6':
{
50: [0.00247, 0.00928, 0.0199, 0.0342, 0.0518, 0.0728, 0.097, 0.125, 0.156, 0.19, 0.23, 0.273, 0.322, 0.376, 0.44, 0.517, 0.625, 0.776, 0.92],
60: [0.00329, 0.0124, 0.0267, 0.0458, 0.0694, 0.0973, 0.13, 0.166, 0.208, 0.254, 0.305, 0.363, 0.427, 0.498, 0.582, 0.683, 0.823, 1.02, 1.19],
}
#W/lb
}}

datos_salida_dict = {}