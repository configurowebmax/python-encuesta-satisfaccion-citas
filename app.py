"""
=====================================================================
 Encuesta de Satisfacción de Citas
 ConfiguroWeb · 2026 · Python real en el navegador (PyScript)
=====================================================================
"""
from pyscript import document, window
from js import localStorage
import json
import math

APP_CLAVE = "python_encuesta_satisfaccion_citas_datos"
VERSION = "1.0.0"


# =====================================================================
#  Lógica de negocio
# =====================================================================
class Calculadora:
    """Modelo de cálculo de Encuesta de Satisfacción de Citas."""

    def __init__(self, n, suma, promotores):
        self.n = float(n)
        self.suma = float(suma)
        self.promotores = float(promotores)

    def calcular(self):
        """Ejecuta el cálculo principal y devuelve un dict de resultados."""

        if self.n == 0:
            return {"error": "N° de encuestados no puede ser 0."}
        promedio = self.suma / self.n
        pct_satisfechos = (self.promotores / self.n) * 100
        nps = (self.promotores / self.n) * 100 - 10  # simplificado
        return {"promedio": promedio, "pct": pct_satisfechos, "nps": nps}


    def diagnostico(self, resultados):
        """Texto explicativo del resultado."""

        if resultados["promedio"] >= 4.5:
            return "🌟 Excelente satisfacción."
        elif resultados["promedio"] >= 3.5:
            return "👍 Satisfacción aceptable."
        return "⚠️ Revisa la calidad del servicio."



# =====================================================================
#  Formateadores
# =====================================================================
def fmt_moneda(v):
    if v is None:
        return "—"
    if math.isinf(v):
        return "∞"
    return f"${v:,.0f}"

def fmt_num(v):
    if v is None:
        return "—"
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return f"{v:,}"

def fmt_pct(v):
    if v is None:
        return "—"
    return f"{v:.1f}%"


# =====================================================================
#  Persistencia localStorage
# =====================================================================
def cargar_guardado():
    try:
        raw = localStorage.getItem(APP_CLAVE)
        if raw:
            return json.loads(raw)
    except Exception:
        pass
    return None

def guardar_ls(datos):
    try:
        localStorage.setItem(APP_CLAVE, json.dumps(datos))
        return True
    except Exception:
        return False


# =====================================================================
#  UI helpers
# =====================================================================
def input_float(eid):
    el = document.querySelector(f"#{eid}")
    if not el or not el.value:
        return 0.0
    try:
        return float(el.value)
    except (ValueError, TypeError):
        return 0.0

def mostrar(html, clase=""):
    caja = document.querySelector("#resultado")
    caja.innerHTML = html
    caja.classList.remove("hidden", "is-error", "is-success")
    if clase:
        caja.classList.add(clase)


# =====================================================================
#  Handlers
# =====================================================================
def calcular_handler(event=None):
    """Lee inputs, instancia, calcula y muestra."""

    c = Calculadora(input_float("n"), input_float("suma"), input_float("promotores"))
    r = c.calcular()
    if "error" in r:
        mostrar(f'❌ {r["error"]}', clase="is-error"); return
    html = f"""
      <div class="result-value">⭐ {r["promedio"]:.2f} / 5</div>
      <p class="result-detail">Satisfechos: {fmt_pct(r["pct"])} · NPS: {r["nps"]:.0f}</p>
      <p class="result-detail">{c.diagnostico(r)}</p>
    """
    mostrar(html, clase="is-success")



def guardar_datos(event=None):
    datos = {
            "n": input_float("n"),
            "suma": input_float("suma"),
            "promotores": input_float("promotores"),
        "version": VERSION,
    }
    ok = guardar_ls(datos)
    if ok:
        mostrar("💾 Datos guardados en este navegador.", clase="is-success")
    else:
        mostrar("❌ No se pudieron guardar los datos.", clase="is-error")


def cargar_al_inicio():
    datos = cargar_guardado()
    if not datos:
        return
    try:
            if "n" in datos:
                document.querySelector("#n").value = datos["n"]
            if "suma" in datos:
                document.querySelector("#suma").value = datos["suma"]
            if "promotores" in datos:
                document.querySelector("#promotores").value = datos["promotores"]
        aviso = document.querySelector("#resultado")
        aviso.innerHTML = "📂 Datos cargados. Pulsa <em>Calcular</em>."
        aviso.classList.remove("hidden")
    except Exception:
        pass


def inicializar():
    cargar_al_inicio()
    window.dispatchEvent(window.Event.new("py:ready"))

inicializar()
