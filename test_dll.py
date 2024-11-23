import os
import sys
import ctypes

def test_dll_load():
    lib_path = os.path.join('src', 'gui', 'lib')
    dll_path = os.path.join(lib_path, 'hasami_shogi_core.dll')
    pyd_path = os.path.join(lib_path, 'hasami_shogi.pyd')
    
    print(f"Testing DLL loading in directory: {os.getcwd()}")
    print(f"DLL path: {dll_path}")
    print(f"PYD path: {pyd_path}")
    
    try:
        # Спроба завантажити hasami_shogi_core.dll
        core_dll = ctypes.CDLL(dll_path)
        print("Successfully loaded hasami_shogi_core.dll")
    except Exception as e:
        print(f"Failed to load hasami_shogi_core.dll: {e}")
        
        # Спробуємо знайти відсутні залежності
        if isinstance(e, OSError):
            import platform
            import subprocess
            
            if platform.system() == 'Windows':
                try:
                    result = subprocess.run(['drmemory', '-report_mismatches', 'false', '--', 'python', 'run.py'],
                                         capture_output=True, text=True)
                    print("\nDependency analysis:")
                    print(result.stdout)
                    print(result.stderr)
                except FileNotFoundError:
                    print("drmemory not found. Skip dependency analysis.")

if __name__ == "__main__":
    test_dll_load()