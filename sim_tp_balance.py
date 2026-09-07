"""
Simulation of Problema 1 - Síntesis de Cloroetano (Balance de Masa)
"""
import numpy as np

# Componentes: 1: N2, 2: HCl, 3: Etileno (C2H4), 4: Cloruro de etilo (C2H5Cl)
MW = np.array([28.02, 36.46, 28.05, 64.51]) # g/mol or kg/kmol

# Alimentaciones:
# F1: HCl puro 50 kmol/h
# F2: 50 kmol/h (96% etileno, 4% N2)
f1 = np.array([0.0, 50.0, 0.0, 0.0])
f2 = np.array([50.0 * 0.04, 0.0, 50.0 * 0.96, 0.0]) # [2.0, 0.0, 48.0, 0.0]

# Purga:
beta = 0.10 # 10%
# Conversión de etileno en reactor:
X_et = 0.90 # 90%

# Estequiometria:
# HCl (2) + Etileno (3) -> Cloruro de etilo (4)
nu = np.array([0.0, -1.0, -1.0, 1.0])

# Flash a 20 atm, 20 °C:
# K-values from Yaws Antoine/Vapor Pressure or flash split in clase24.8.26
# Let's inspect what clase24.8.26 used for alpha_flash
# In clase24.8.26:
# P_sat at 20 °C (293.15 K):
# substance: N2, HCl, etileno, cloroetano
# alpha = [5509.73, 31.259, 46.723, 1.0] (relative to cloroetano)
# Let's check the exact flash model used in clase24.8.26:
# f^<10>_i = alpha_i * (f^<10>_4 / f^<7>_4) * f^<7>_i or similar?

print(f"Feed 1 (HCl): {f1}")
print(f"Feed 2 (Etileno/N2): {f2}")
