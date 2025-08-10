from __future__ import annotations

import argparse
import sys
from importlib import import_module
from pathlib import Path


def _add_src_to_sys_path() -> None:
    """
    Intenta localizar la carpeta 'src' y agregarla al sys.path para que
    se pueda importar el paquete 'quality' ya sea que ejecutes desde
    EXAMEN_ASEGURAMIENTO o desde quality-enforcer.
    """
    script_dir = Path(__file__).resolve().parent
    cwd = Path.cwd().resolve()

    candidates = [
        script_dir / "src",
        script_dir / "quality-enforcer" / "src",
        cwd / "src",
        cwd / "quality-enforcer" / "src",
        script_dir.parent / "src",
        cwd.parent / "src",
    ]

    for p in candidates:
        if p.is_dir():
            sp = str(p)
            if sp not in sys.path:
                sys.path.insert(0, sp)
            # en cuanto encontramos una válida, basta
            break


def _import_first(*module_names: str):
    """
    Intenta importar el primer módulo disponible de la lista.
    Permite soportar nombres cortos (maxrule/namingrule) o largos
    (max_line_length_rule/naming_convention_rule) y con/sin prefijo 'src.'.
    """
    last_exc = None
    for name in module_names:
        try:
            return import_module(name)
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
    if last_exc:
        raise last_exc
    raise ImportError("No se pudo importar ningún módulo de la lista proporcionada.")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Aplica reglas de calidad a un archivo .py"
    )
    p.add_argument("file", type=str, help="Ruta del archivo Python a verificar")
    p.add_argument("--max-len", type=int, default=100, help="Largo máximo de línea")
    return p.parse_args()


def main() -> int:
    _add_src_to_sys_path()

    # Importa Engine
    engine_mod = None
    try:
        engine_mod = _import_first("src.quality.engine", "quality.engine")
    except Exception as e:
        print("Error importando 'engine':", e)
        return 3
    Engine = getattr(engine_mod, "Engine")

    # Importa reglas (intenta nombres cortos y largos, con y sin 'src.')
    try:
        max_mod = _import_first(
            "src.quality.maxrule",
            "quality.maxrule",
            "src.quality.max_line_length_rule",
            "quality.max_line_length_rule",
        )
        naming_mod = _import_first(
            "src.quality.namingrule",
            "quality.namingrule",
            "src.quality.naming_convention_rule",
            "quality.naming_convention_rule",
        )
    except Exception as e:
        print("Error importando reglas:", e)
        return 3

    # Obtiene clases
    MaxLineLengthRule = getattr(max_mod, "MaxLineLengthRule")
    NamingConventionRule = getattr(naming_mod, "NamingConventionRule")

    args = parse_args()
    path = Path(args.file)
    if not path.exists():
        print(f"Archivo no encontrado: {path}")
        return 1

    engine = Engine(
        rules=[
            NamingConventionRule(),
            MaxLineLengthRule(args.max_len),
        ]
    )

    results = engine.run_on_file(path)
    ok = True
    for name, res in results:
        print(f"\n=== {name} ===")
        for msg in res.messages:
            print(msg)
        ok &= res.passed

    print("\nRESULTADO FINAL:", "OK" if ok else "CON PROBLEMAS")
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
