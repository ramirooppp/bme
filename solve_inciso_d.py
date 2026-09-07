import numpy as np
from scipy.optimize import root

# Componentes: 1: N2, 2: Etileno, 3: HCl, 4: Cloroetano
# F2 is fixed: 50 kmol/h (96% etileno, 4% N2) -> [2, 48, 0, 0]
f2 = np.array([2.0, 48.0, 0.0, 0.0])
x1 = np.array([0.0, 0.0, 1.0, 0.0]) # Pure HCl feed
nu = np.array([0.0, -1.0, -1.0, 1.0])
X_et = 0.90
alpha = np.array([5509.730752, 46.722771, 31.259085, 1.0])
LK = 0.001
HK = 0.001
beta = 0.10

def equations(vars):
    # vars: f (4x15 = 60 values), eps (1), F1 (1) -> 62 variables
    f = vars[:60].reshape((4, 15), order='F') # 1-indexed cols 1..15
    eps = vars[60]
    F1 = vars[61]
    
    eqs = []
    
    # 1. Feed 1 definition: f^<1> = F1 * x1
    for i in range(4):
        eqs.append(f[i, 0] - F1 * x1[i])
        
    # 2. Feed 2 definition: f^<2> = f2
    for i in range(4):
        eqs.append(f[i, 1] - f2[i])
        
    # 3. Mixer 1: f^<1> + f^<2> + f^<15> = f^<3>
    for i in range(4):
        eqs.append(f[i, 0] + f[i, 1] + f[i, 14] - f[i, 2])
        
    # 4. Reactor ratio 1:1 -> f_{2,3} = f_{3,3} (etileno = HCl)
    eqs.append(f[1, 2] - f[2, 2])
    
    # 5. Reactor balance: f^<3> + nu * eps = f^<4>
    for i in range(4):
        eqs.append(f[i, 2] + nu[i] * eps - f[i, 3])
        
    # 6. Reactor conversion: X_et = (f_{2,3} - f_{2,4}) / f_{2,3}
    eqs.append(X_et * f[1, 2] - (f[1, 2] - f[1, 3]))
    
    # 7. Compressor: f^<4> = f^<5>
    for i in range(4):
        eqs.append(f[i, 3] - f[i, 4])
        
    # 8. Cooler: f^<5> = f^<6>
    for i in range(4):
        eqs.append(f[i, 4] - f[i, 5])
        
    # 9. Flash balance: f^<6> = f^<7> + f^<9>
    for i in range(4):
        eqs.append(f[i, 5] - (f[i, 6] + f[i, 8]))
        
    # 10. Flash equilibrium: f^<9> = alpha * f^<7>
    for i in range(4):
        eqs.append(f[i, 8] - alpha[i] * f[i, 6]) # wait, alpha * f_7
    # fix eq 10:
    for i in range(4):
        eqs[-(4-i)] = f[i, 8] - alpha[i] * f[i, 6] # wait, f_7 is index 6
        
    # 11. Tower balance: f^<7> = f^<8> + f^<10>
    for i in range(4):
        eqs.append(f[i, 6] - (f[i, 7] + f[i, 9]))
        
    # 12. Tower specs:
    eqs.append(f[0, 7] - 0.0) # f_1,8 = 0
    eqs.append(f[1, 7] - 0.0) # f_2,8 = 0
    eqs.append(f[2, 7] - LK * f[2, 6]) # f_3,8 = LK * f_3,7
    eqs.append(f[3, 9] - HK * f[3, 6]) # f_4,10 = HK * f_4,7
    
    # 13. Mixer 2: f^<9> + f^<10> = f^<11>
    for i in range(4):
        eqs.append(f[i, 8] + f[i, 9] - f[i, 10])
        
    # 14. Divider: f^<11> = f^<12> + f^<13>
    for i in range(4):
        eqs.append(f[i, 10] - (f[i, 11] + f[i, 12]))
        
    # 15. Purge spec: f^<12> = beta * f^<11>
    for i in range(4):
        eqs.append(f[i, 11] - beta * f[i, 10])
        
    # 16. Valve: f^<13> = f^<14>
    for i in range(4):
        eqs.append(f[i, 12] - f[i, 13])
        
    # 17. Heater: f^<14> = f^<15>
    for i in range(4):
        eqs.append(f[i, 13] - f[i, 14])
        
    return np.array(eqs)

# Initial guess:
init_vars = np.ones(62)
init_vars[60] = 43.0
init_vars[61] = 48.0

sol = root(equations, init_vars, method='lm')
f_sol = sol.x[:60].reshape((4, 15), order='F')
eps_sol = sol.x[60]
F1_sol = sol.x[61]

print(f"Solved successfully: {sol.success}")
print(f"Required Fresh HCl Feed (F1): {F1_sol:.4f} kmol/h")
print(f"Reaction Extent (eps): {eps_sol:.4f} kmol/h")
print(f"Reactor Inlet Stream 3 (f^<3>):")
print(f"  N2: {f_sol[0,2]:.4f} kmol/h")
print(f"  Etileno: {f_sol[1,2]:.4f} kmol/h")
print(f"  HCl: {f_sol[2,2]:.4f} kmol/h")
print(f"  Cloroetano: {f_sol[3,2]:.4f} kmol/h")
print(f"  Ratio HCl / Etileno in Stream 3: {f_sol[2,2] / f_sol[1,2]:.6f}")
