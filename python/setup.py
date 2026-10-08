"""Dual-mode build script: pure Python or Cython-compiled.

Usage:
    uv build                          # Pure Python mode (default)
    BUILD_MODE=cython uv build        # Cython mode (.so, no .py for compiled modules)

Configuration via pyproject.toml [tool.builder-opt]:
    cython_modules_path   - directories whose .py files get compiled
    exclude_from_cython   - files NOT compiled (stay as .py), even if in above dirs
    exclude_from_package  - files NEVER packaged (any mode)
"""

import os
import subprocess
import tomllib

from setuptools import Extension, find_packages, setup
from setuptools.command.build_ext import build_ext


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

with open("pyproject.toml", "rb") as f:
    config = tomllib.load(f)

pyproj_cfg = config.get("tool", {}).get("builder-opt", {})
cython_paths: list[str] = pyproj_cfg.get("cython_modules_path", [])
exclude_from_cython: set[str] = set(pyproj_cfg.get("exclude_from_cython", []))
exclude_from_package: set[str] = set(pyproj_cfg.get("exclude_from_package", []))

build_mode = os.environ.get("BUILD_MODE", "python").lower()


# ---------------------------------------------------------------------------
# Determine which modules to compile and which .py files to hide
# ---------------------------------------------------------------------------

ext_modules = []
# .py files that should NOT appear in the wheel
hidden_py_files: set[str] = set()

if build_mode == "cython":
    from Cython.Build import cythonize

    for path in cython_paths:
        for root, _, files in os.walk(path):
            for file in sorted(files):
                if not file.endswith(".py"):
                    continue
                if file == "__init__.py":
                    continue  # Always keep __init__.py as pure Python

                module_path = os.path.join(root, file)

                # Skip files explicitly excluded from compilation
                if module_path in exclude_from_cython:
                    continue

                # Skip files excluded from package entirely
                if module_path in exclude_from_package:
                    continue

                # Convert "src/{{name}}/utils/helper.py" → "{{name}}.utils.helper"
                module_name = (
                    module_path.replace("src/", "", 1)
                    .replace("/", ".")
                    .removesuffix(".py")
                )
                ext_modules.append(
                    Extension(
                        name=module_name,
                        sources=[module_path],
                        extra_compile_args=["-O3"],
                    )
                )
                # The .py source is replaced by .so — hide it from the wheel
                hidden_py_files.add(module_path)

    ext_modules = cythonize(
        ext_modules,
        compiler_directives={"language_level": "3", "embedsignature": True},
        nthreads=4,
    )
    print(f"[BUILD] Cython mode: {len(ext_modules)} modules → .so")
    if exclude_from_cython:
        print(f"         {len(exclude_from_cython)} files excluded from compilation (stay .py)")
else:
    print("[BUILD] Pure Python mode: all source included in wheel")

# Files never packaged (any mode)
hidden_py_files |= exclude_from_package
print(f"         {len(hidden_py_files)} .py files hidden from wheel")


# ---------------------------------------------------------------------------
# Custom build_ext: strip + UPX (Cython mode only)
# ---------------------------------------------------------------------------


class HardenedBuildExt(build_ext):
    """After building .so files, strip symbols and compress with UPX."""

    def run(self):
        super().run()
        if build_mode != "cython":
            return
        for output in self.get_outputs():
            if not output.endswith(".so"):
                continue
            self._strip(output)
            self._upx(output)

    def _strip(self, path: str) -> None:
        try:
            print(f"  strip: {path}")
            subprocess.check_call(["strip", "--strip-all", path])
        except FileNotFoundError:
            print("  WARNING: 'strip' not found, skipping")
        except subprocess.CalledProcessError as e:
            print(f"  WARNING: strip failed: {e}")

    def _upx(self, path: str) -> None:
        try:
            print(f"  upx:   {path}")
            subprocess.check_call(["upx", "--best", path])
        except FileNotFoundError:
            print("  WARNING: 'upx' not found, skipping")
        except subprocess.CalledProcessError as e:
            print(f"  WARNING: upx failed: {e}")


# ---------------------------------------------------------------------------
# Custom build_py: remove hidden .py files after they're copied to build dir
# ---------------------------------------------------------------------------

from setuptools.command.build_py import build_py as _build_py


class FilteredBuildPy(_build_py):
    """Remove excluded .py files from the build output before wheel packaging."""

    def run(self):
        super().run()
        # Remove hidden .py files from the build directory
        for filepath in hidden_py_files:
            # filepath is like "src/testpkg/utils/helper.py"
            # In build dir it's like "build/lib/testpkg/utils/helper.py"
            rel = filepath.removeprefix("src/")
            build_path = os.path.join(self.build_lib, rel)
            if os.path.exists(build_path):
                os.remove(build_path)
                print(f"  removed: {build_path}")

        # Also remove .c files generated by Cython
        if build_mode == "cython":
            for path in cython_paths:
                pkg_rel = path.removeprefix("src/")
                build_pkg_dir = os.path.join(self.build_lib, pkg_rel)
                if os.path.isdir(build_pkg_dir):
                    for f in os.listdir(build_pkg_dir):
                        if f.endswith(".c"):
                            c_path = os.path.join(build_pkg_dir, f)
                            os.remove(c_path)
                            print(f"  removed: {c_path}")


# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

setup(
    use_scm_version=True,
    ext_modules=ext_modules,
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=False,
    zip_safe=False,
    cmdclass={
        "build_ext": HardenedBuildExt,
        "build_py": FilteredBuildPy,
    },
)
