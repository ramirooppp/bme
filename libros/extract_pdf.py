import sys
import subprocess

try:
    import PyPDF2
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyPDF2"])
    import PyPDF2

input_pdf = r"c:\Users\nahue\Desktop\segundo cuatrimestre\libros\fisicoquimica.pdf"
output_pdf = r"c:\Users\nahue\Desktop\segundo cuatrimestre\libros\Crash_Course_Termodinamica.pdf"

logical_ranges = [
    (26, 28),
    (31, 36),
    (38, 43),
    (73, 86),
    (90, 98),
    (160, 160),
    (167, 169),
    (173, 175),
    (199, 214)
]

# The user mentioned logical page 1 = PDF page 18 (1-indexed).
# So 0-indexed PDF page index = logical_page + 17 - 1 = logical_page + 16

reader = PyPDF2.PdfReader(input_pdf)
writer = PyPDF2.PdfWriter()

for start, end in logical_ranges:
    for logical_page in range(start, end + 1):
        pdf_index = logical_page + 16
        if pdf_index < len(reader.pages):
            writer.add_page(reader.pages[pdf_index])

with open(output_pdf, "wb") as f:
    writer.write(f)

print(f"Extracted {len(writer.pages)} pages successfully.")
print(f"Saved to {output_pdf}")
