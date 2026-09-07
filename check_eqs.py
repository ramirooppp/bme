import numpy as np
from scipy.optimize import root

# Componentes: 1: N2, 2: HCl, 3: C2H4, 4: C2H5Cl
# 15 streams, each with 4 component flows: f is 4x15 matrix (60 variables)
# plus eps_R1 (1 variable) -> 61 variables

# Feeds:
f1 = np.array([0.0, 50.0, 0.0, 0.0]) # HCl puro (50 kmol/h) - wait, in clase24.8.26 is f1 HCl or N2/C2H4?
f2 = np.array([2.0, 0.0, 48.0, 0.0]) # 96% C2H4, 4% N2 (50 kmol/h)

nu = np.array([0.0, -1.0, -1.0, 1.0])
X_et = 0.90
alpha_K1 = np.array([5509.730752, 31.259085, 46.722771, 1.0])
LK = 0.001
HK = 0.001
beta = 0.10

# Let's check the equations from clase24.8.26:
# 1) Mezclador 1: f^<1> + f^<2> + f^<15> = f^<3> (4 eq)
# 2) Conversión: X_et = (f_3,3 - f_3,4) / f_3,3  (1 eq)
# 3) Reactor: f^<3> + nu * eps_R1 = f^<4> (4 eq)
# 4) Compresor: f^<4> = f^<5> (4 eq)
# 5) Enfriador: f^<5> = f^<6> (4 eq)
# 6) Flash balance: f^<6> = f^<7> + f^<10> (4 eq)
# 7) Flash equilibrio: f_i,10 = alpha_i * f_i,7 (4 eq)
# 8) Torre Destilación balance: f^<7> = f^<8> + f^<9> (4 eq)
# 9) Torre especificaciones:
#    f_1,8 = f_1,7 (o f_1,8 = f_1,7 - f_1,9 con f_1,9 = 0)
#    f_1,8 = 0? wait: R71 says f_1,8 = 0 or f_1,9 = 0? In R71: f_{1,8} = 0?
#    Let's check R71, R73, R74, R75:
#    R71: f_{1,8} = 0 (wait! N2 in distillate 8?)
#    R73: f_{2,8} = 0 ?
#    R74: f_{3,8} = LK * f_{3,7}
#    R75: f_{4,9} = HK * f_{4,7}
# 10) Mezclador 2: f^<6>? wait! In R77: f^<6> + f^<10> = f^<11>?
#     Wait! Let's check R77 in clase24.8.26! R77 wrote f^<6> + f^<10> = f^<11> instead of f^<8> + f^<10> = f^<11>!
# 11) Divisor: f^<11> = f^<12> + f^<13> (4 eq)
# 12) Purga: f^<12> = beta * f^<11> (4 eq)
# 13) Expansión: f^<13> = f^<14> (4 eq)
# 14) Calentador/Reciclo: f^<14> = f^<15> (4 eq)

print("Checking equations...")
