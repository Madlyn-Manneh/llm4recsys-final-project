import sys, subprocess, os, platform, ctypes

out = []
out.append("--- python --version ---")
out.append(subprocess.check_output([r".\.venv\Scripts\python.exe", "--version"], text=True).strip())
out.append("")
out.append("--- sys.version ---")
out.append(sys.version)
out.append("")
out.append("--- pip freeze ---")
out.append(subprocess.check_output([r".\.venv\Scripts\pip.exe", "freeze"], text=True).strip())
out.append("")
out.append("--- CPU model ---")
out.append(platform.processor())
out.append("")
out.append("--- Total RAM (GB) ---")
class MS(ctypes.Structure):
    _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
ms = MS()
ms.dwLength = ctypes.sizeof(MS)
ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(ms))
out.append(str(round(ms.ullTotalPhys / (1024**3), 2)))

os.makedirs("outputs", exist_ok=True)
with open("outputs/environment.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out) + "\n")
print("written")