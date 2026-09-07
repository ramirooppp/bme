import win32com.client
import os

# ==============================================================================
# SCRIPT DE RENDERIZADO COM - MATHCAD 15 (EJERCICIO 2 SRK)
# ==============================================================================

injected_path = os.path.abspath(r"C:/Users/nahue/Desktop/segundo cuatrimestre/mathcad/Ejercicio_2_Inyectado.xmcd")
resolved_path = os.path.abspath(r"C:/Users/nahue/Desktop/segundo cuatrimestre/mathcad/Ejercicio_2_Resuelto.xmcd")

print("Iniciando instancia COM de Mathcad...")
mc = win32com.client.Dispatch('Mathcad.Application')

try:
    print(f"Abriendo archivo inyectado: {injected_path}...")
    ws = mc.Worksheets.Open(injected_path)
    
    print("Recalculando la hoja de calculo...")
    ws.Recalculate()
    
    print(f"Guardando archivo resuelto en: {resolved_path}...")
    ws.SaveAs(resolved_path)
    
    ws.Close(2) # 2 = mcDiscardChanges / close cleanly
    print("¡Ejercicio 2 resuelto y renderizado con exito!")
except Exception as e:
    print(f"Error durante la automatizacion COM de Mathcad: {e}")
finally:
    mc.Quit(2)
