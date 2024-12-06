# Part of ImGui Bundle - MIT License - Copyright (c) 2022-2023 Pascal Thomet - https://github.com/pthom/imgui_bundle


def _glfw_set_search_path() -> None:
    """Sets os.environ["PYGLFW_LIBRARY"] so that glfw provided by pip uses our glfw library.

    venv/lib/python3.9/site-packages/glfw/library.py

    if os.environ.get('PYGLFW_LIBRARY', ''):
        try:
            glfw = ctypes.CDLL(os.environ['PYGLFW_LIBRARY'])
        except OSError:
            glfw = None

    """
    import os
    import platform

    this_dir = os.path.dirname(__file__)
    if platform.system() == "Darwin":
        lib_file = "libglfw.3.dylib"
        if not os.path.exists(f"{this_dir}/{lib_file}"):
            msg = f"Cannot find {lib_file} in {this_dir}\n"
            raise FileNotFoundError(msg)
    elif platform.system() == "Windows":
        if os.path.exists(f"{this_dir}/glfw3.dll"):
            lib_file = "glfw3.dll"
        else:
            msg = f"Cannot find glfw3.dll in {this_dir}\n"
            raise FileNotFoundError(msg)
    elif platform.system() == "Linux":
        if os.path.exists(f"{this_dir}/libglfw.so.3"):
            lib_file = "libglfw.so.3"
        elif os.path.exists(f"{this_dir}/libglfw.3.so"):
            lib_file = "libglfw.3.so"
        if os.path.exists(f"{this_dir}/libglfw.so.3.3"):
            lib_file = "libglfw.so.3.3"
        else:
            msg = f"Cannot find libglfw.so.3 or libglfw.3.so in {this_dir}\n"
            raise FileNotFoundError(msg)
    else:
        msg = f"Please implement set_pip_glfw_search_path() for your os: {platform.system()}\n"
        raise NotImplementedError(msg)
    os.environ["PYGLFW_LIBRARY"] = f"{this_dir}/{lib_file}"
