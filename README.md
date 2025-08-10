# Quality Enforcer

Pequeño prototipo que aplica reglas de calidad a archivos de código.

## Requisitos evaluados
- Clase abstracta: `Rule`
- Dos interfaces: `Serializable`, `Reportable`
- Implementaciones: `NamingConventionRule`, `MaxLineLengthRule` (implementan la abstracta y ambas interfaces)
- Buenas prácticas: estructura src/, pruebas pytest, formateo Black/Isort, README, LICENSE, .gitignore

## Uso
```bash
python main.py ejemplo.py
