# 🚗 Car Rental Management System

Sistema de gestión de renta de vehículos desarrollado con **Python 3.12**, **Flet 0.27** y **SQLite**. Permite administrar vehículos, clientes, reservaciones y rentas desde una interfaz gráfica de escritorio con tema oscuro.

---

## 📋 Requisitos

| Componente | Versión |
|---|---|
| Python | 3.12.x |
| Flet | 0.27.6 |
| SQLite | Incluido con Python |

> ⚠️ **Importante:** Este proyecto fue desarrollado y probado con **Python 3.12** y **Flet 0.27.6**. No se garantiza compatibilidad con Python 3.14 ni con versiones de Flet 0.80+, ya que esas versiones tienen cambios de API incompatibles.

---

## 🚀 Instalación y ejecución

### 1. Clona o descarga el proyecto

```
car_rental_v2/
├── main.py
├── seed_data.py
├── requirements.txt
├── database/
├── views/
└── utils/
```

### 2. Crea un entorno virtual

```powershell
cd Car-Rental-System-Flet
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instala las dependencias

```powershell
pip install flet==0.27.6
```

### 4. (Opcional) Carga datos de prueba

```powershell
python seed_data.py
```

Esto crea 10 vehículos, 5 clientes, 1 reserva y 1 renta de ejemplo.

### 5. Inicia la aplicación

```powershell
python main.py
```

---

## 📁 Estructura del proyecto

```
car_rental_v2/
│
├── main.py                        # Punto de entrada, sidebar y navegación
├── seed_data.py                   # Script para cargar datos de prueba
├── requirements.txt               # Dependencias (flet==0.27.6)
│
├── database/                      # Capa de datos
│   ├── db.py                      # Conexión SQLite, esquema, VIEWs, migraciones
│   ├── vehicle_queries.py         # CRUD de vehículos
│   ├── customer_queries.py        # CRUD de clientes
│   ├── rental_queries.py          # Reservaciones, rentas, conversión automática
│   └── report_queries.py          # Consultas para dashboard y reportes
│
├── views/                         # Vistas de la interfaz
│   ├── dashboard_view.py          # Tarjetas de resumen general
│   ├── vehicles_view.py           # Gestión de vehículos
│   ├── customers_view.py          # Gestión de clientes
│   ├── reservations_view.py       # Gestión de reservaciones
│   ├── rentals_view.py            # Gestión de rentas
│   └── reports_view.py            # Reportes y estadísticas
│
└── utils/
    ├── theme.py                   # Paleta de colores, estilos, componentes reutilizables
    └── modal.py                   # Sistema de modales personalizado (reemplaza AlertDialog)
```

---

## 🗄️ Base de datos

El archivo `car_rental.db` se crea automáticamente en la carpeta `database/` al iniciar la aplicación por primera vez.

### Tablas

| Tabla | Descripción |
|---|---|
| `vehicles` | Vehículos de la flota con marca, modelo, año, tipo, tarifa y estado |
| `customers` | Clientes con nombre, teléfono, email y número de licencia |
| `reservations` | Reservas futuras vinculadas a cliente y vehículo |
| `rentals` | Rentas activas e historial con costo total |
| `maintenance` | Registros de mantenimiento por vehículo |

### VIEWs SQL

| Vista | Descripción |
|---|---|
| `available_vehicles` | Filtra vehículos con estado `available` |
| `rental_summary` | JOIN de rentas con clientes y vehículos, incluye expresión CASE para detectar rentas vencidas |

### Expresión CASE utilizada

```sql
CASE
    WHEN r.status = 'active' AND date(r.end_date) < date('now') THEN 'late'
    WHEN r.status = 'active'    THEN 'active'
    WHEN r.status = 'completed' THEN 'completed'
    ELSE r.status
END AS rental_status
```

---

## ✅ Funcionalidades

### 🏠 Dashboard
- Tarjetas de resumen: total de vehículos, disponibles, rentados, reservados, en mantenimiento
- Total de clientes, rentas activas, reservas pendientes e ingresos totales
- Botón de actualización en tiempo real

### 🚙 Vehículos
- Agregar, editar y eliminar vehículos
- Filtrar por marca, tipo y estado
- Estados: `Disponible`, `Reservado`, `Rentado`, `Mantenimiento`
- Validaciones: año entre 1900–2030, tarifa mayor a 0

### 👥 Clientes
- Agregar, editar y eliminar clientes
- Búsqueda por nombre, teléfono, email o número de licencia
- Validación de formato de email
- Número de licencia único por cliente

### 📅 Reservaciones
- Crear reservas futuras vinculando cliente y vehículo disponible
- Cancelar reservas pendientes
- Filtrar por estado: Pendiente, Convertida, Completada, Cancelada
- Detección automática de conflictos de fechas

### 🔑 Rentas
- Cargar datos desde una reserva pendiente con un clic (auto-relleno)
- Calcular el costo antes de confirmar (días × tarifa/día)
- El botón "Confirmar Renta" se habilita solo después de calcular
- Conversión automática de reserva → renta al confirmar
- Completar rentas activas
- Detección de rentas vencidas mediante expresión CASE en SQL

### 📊 Reportes
- **Flota por Estado:** conteo de vehículos agrupado por estado
- **Ingresos Mensuales:** rentas y revenue agrupados por mes
- **Top Clientes:** ranking por número de rentas y total gastado

---

## 🔒 Lógica de negocio

- Un vehículo **no puede ser reservado ni rentado** si ya tiene una reserva o renta activa en las mismas fechas (detección de overlap en SQL)
- Al **completar una renta**, el vehículo vuelve automáticamente a `available` (o `reserved` si tiene otra reserva pendiente)
- Al **crear una renta**, si existe una reserva pendiente para ese vehículo y fechas, se convierte automáticamente a estado `converted`
- Al **cancelar una reserva**, el vehículo vuelve a `available` si no tiene otras reservas activas

---

## 🎨 Tema visual

El sistema usa un tema oscuro con la siguiente paleta:

| Variable | Color | Uso |
|---|---|---|
| `BG` | `#0f1117` | Fondo principal |
| `SIDEBAR_BG` | `#1a1a2e` | Sidebar de navegación |
| `CARD_BG` | `#1e2130` | Filas de tabla y tarjetas |
| `PRIMARY` | `#4a90d9` | Botones y acentos azules |
| `SUCCESS` | `#2ecc71` | Estado activo, costos, guardar |
| `WARNING` | `#f39c12` | Botón editar, calcular |
| `DANGER` | `#e74c3c` | Eliminar, cancelar, vencido |
| `PURPLE` | `#9b59b6` | Reservas pendientes |

---

## 📝 Estrategia de commits Git sugerida

```
1. init: estructura del proyecto y esquema de base de datos
2. feat: CRUD de vehículos con validaciones
3. feat: CRUD de clientes con búsqueda
4. feat: módulo de reservaciones con detección de conflictos
5. feat: módulo de rentas con cálculo de costo
6. feat: conversión automática reserva → renta
7. feat: dashboard con tarjetas de resumen
8. feat: módulo de reportes con 3 vistas
9. fix: sistema de modales personalizado para compatibilidad Flet 0.27
10. style: tema oscuro completo y componentes reutilizables
```

---

## 🧪 Datos de prueba

El script `seed_data.py` carga:
- **10 vehículos** de distintas marcas, tipos y tarifas
- **5 clientes** con datos de contacto
- **1 reserva** activa (Honda CR-V, cliente Juan Pérez)
- **1 renta** activa (Ford F-150, cliente María García)

---

## 📚 Tecnologías y conceptos demostrados

- `SQLite` con `sqlite3` — persistencia local sin servidor
- `DDL` — `CREATE TABLE`, `CREATE VIEW`, constraints (`NOT NULL`, `CHECK`, `UNIQUE`, `REFERENCES`)
- `DML` — `INSERT`, `UPDATE`, `DELETE`
- `DQL` — `SELECT` con `JOIN`, `GROUP BY`, `COUNT`, `SUM`, `COALESCE`
- `CASE` expression — clasificación dinámica de estados
- `VIEW` — `available_vehicles` y `rental_summary`
- `FOREIGN KEYS` — integridad referencial entre tablas
- Detección de solapamiento de fechas con SQL
- GUI con Flet — navegación lateral, tablas, modales, formularios, validaciones
- Arquitectura modular — separación en capas (database, views, utils)
