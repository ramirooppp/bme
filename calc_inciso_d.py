import numpy as np

# Componentes: 1: N2, 2: Etileno, 3: HCl, 4: Cloroetano
# In steady state:
# Let's analyze the species:
# N2: Feed 2 has 2 kmol/h. In steady state, purge (Stream 12) removes 2 kmol/h of N2.
# Since purge is beta = 0.10 of Stream 11:
# f_1,11 = 2 / 0.10 = 20 kmol/h.
# Recycle f_1,15 = 0.90 * 20 = 18 kmol/h.
# In Stream 3: f_1,3 = 2 + 18 = 20 kmol/h.

# Etileno:
# Feed 2 has 48 kmol/h.
# In reactor, X_et = 0.90 -> 90% of f_2,3 reacts: eps = 0.90 * f_2,3
# f_2,4 = 0.10 * f_2,3.
# In Flash: alpha_2 = 46.722771
# f_2,9 = (46.722771 / 47.722771) * f_2,6 = 0.9790457 * f_2,4
# f_2,7 = (1 / 47.722771) * f_2,4 = 0.0209543 * f_2,4
# In Tower: f_2,8 = 0 -> f_2,10 = f_2,7 = 0.0209543 * f_2,4
# In Mixer 2: f_2,11 = f_2,9 + f_2,10 = f_2,4
# In Recycle: f_2,15 = 0.90 * f_2,11 = 0.90 * f_2,4 = 0.90 * 0.10 * f_2,3 = 0.09 * f_2,3.
# In Mixer 1: f_2,3 = 48 + f_2,15 = 48 + 0.09 * f_2,3
# (1 - 0.09) * f_2,3 = 48 => 0.91 * f_2,3 = 48
# f_2,3 = 48 / 0.91 = 52.74725 kmol/h!
# eps = 0.90 * 52.74725 = 47.47253 kmol/h.

# Now in Inciso d):
# We WANT: f_3,3 = f_2,3 = 52.74725 kmol/h (Ratio 1:1 in reactor feed!)
# Let's trace HCl (Component 3):
# In reactor: f_3,4 = f_3,3 - eps = 52.74725 - 47.47253 = 5.274725 kmol/h!
# In Flash: alpha_3 = 31.259085
# f_3,9 = (31.259085 / 32.259085) * f_3,4 = 0.9689998 * f_3,4
# f_3,7 = (1 / 32.259085) * f_3,4 = 0.0310002 * f_3,4
# In Tower: f_3,8 = 0.001 * f_3,7 -> f_3,10 = 0.999 * f_3,7 = 0.0309692 * f_3,4
# In Mixer 2: f_3,11 = f_3,9 + f_3,10 = (0.9689998 + 0.0309692) * f_3,4 = 0.999969 * f_3,4
# In Recycle: f_3,15 = 0.90 * f_3,11 = 0.90 * 0.999969 * 5.274725 = 4.74711 kmol/h!
# In Mixer 1: f_3,3 = F1 + f_3,15
# Therefore: F1 = f_3,3 - f_3,15 = 52.74725 - 4.74711 = 48.00014 kmol/h!

print(f"Required Fresh HCl feed F1 = 48.00 kmol/h (approx 48 kmol/h)")
print(f"Reactor Feed Stream 3: Etileno = 52.75 kmol/h, HCl = 52.75 kmol/h (Ratio = 1.000)")
