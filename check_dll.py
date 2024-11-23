import os
import sys
from ctypes import windll, get_last_error

def check_dll(dll_path):
    try:
        # Спроба завантажити DLL
        handle = windll.kernel32.LoadLibraryW(dll_path)
        if handle:
            print(f"Successfully loaded {dll_path}")
            windll.kernel32.FreeLibrary(handle)
        else:
            error = get_last_error()
            print(f"Failed to load {dll_path}")
            print(f"Error code: {error}")

            # Спроба завантажити залежності
            dependencies = ["msvcp140.dll", "vcruntime140.dll", "vcruntime140_1.dll"]
            for dep in dependencies:
                try:
                    windll.kernel32.LoadLibraryW(dep)
                    print(f"Successfully loaded {dep}")
                except Exception as e:
                    print(f"Failed to load {dep}: {e}")
    except Exception as e:
        print(f"Exception while loading {dll_path}: {e}")

if __name__ == "__main__":
    lib_path = os.path.join("src", "gui", "lib")
    core_dll = os.path.join(lib_path, "hasami_shogi_core.dll")
    python_dll = os.path.join(lib_path, "hasami_shogi.pyd")

    print("Checking DLLs...")
    check_dll(core_dll)
    check_dll(python_dll)

    print("\nChecking Python sys.path:")
    for path in sys.path:
        print(path)

    print("\nChecking environment PATH:")
    for path in os.environ['PATH'].split(os.pathsep):
        print(path)