import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuración inicial
FILENAME = "incidencia.xlsx"
SHEETNAME = "Lista_incidencias"
FILENAME_SATIFACCION = "satisfaccion.xlsx"
SHEETNAME_SATIFACCION= "Lista_satifaccion"
FILENAME_TAREAS= "tareas.xlsx"
SHEETNAME_TAREAS="Lista_tareas"

# Funciones para manejo de incidencias
def cargar_datos():
    if os.path.exists(FILENAME):
        df = pd.read_excel(FILENAME, sheet_name=SHEETNAME)
        # Asegurar que el DataFrame tenga la columna "Estado"
        if "Estado" not in df.columns:
            df["Estado"] = "Pendiente"
        return df
    else:
        return pd.DataFrame(columns=["Nombre", "Fecha", "Incidencia", "Estado"])

def guardar_datos(df):
    with pd.ExcelWriter(FILENAME, engine='openpyxl', mode='w') as writer:
        df.to_excel(writer, sheet_name=SHEETNAME, index=False)

def agregar_incidencia():
    st.subheader("Agregar nueva incidencia")
    nombre = st.text_input("Nombre")
    fecha = st.date_input("Fecha", value=datetime.today())
    motivo = st.text_area("Motivo de la incidencia")
    estado = st.selectbox("Estado", ["Pendiente", "En proceso", "Terminado"])
    
    if st.button("Registrar incidencia"):
        if nombre and motivo:
            df = cargar_datos()
            nuevo = {
                "Nombre": nombre, 
                "Fecha": fecha.strftime("%Y-%m-%d"), 
                "Incidencia": motivo, 
                "Estado": estado
            }
            df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
            guardar_datos(df)
            st.success("✅ Incidencia registrada correctamente")
            st.rerun()  # Actualizar la vista
        else:
            st.error("❌ Debes rellenar todos los campos obligatorios")

def mostrar_incidencias():
    st.subheader("Lista de incidencias")
    df = cargar_datos()
    if df.empty:
        st.info("No hay incidencias registradas.")
    else:
        st.dataframe(df)

def eliminar_incidencia():
    st.subheader("Eliminar una incidencia")
    df = cargar_datos()
    if df.empty:
        st.info("No hay incidencias para eliminar.")
        return
    
    st.dataframe(df)
    index = st.number_input("Índice a eliminar", min_value=0, max_value=len(df)-1, step=1)

    if st.button("Eliminar"):
        st.write("Registro a eliminar:")
        st.write(df.loc[[index]])
        df = df.drop(index).reset_index(drop=True)
        guardar_datos(df)
        st.success("✅ Registro eliminado correctamente")
        st.rerun()  # Actualizar la vista

def modificar_incidencia():
    st.subheader("Modificar una incidencia")
    df = cargar_datos()
    if df.empty:
        st.info("No hay incidencias para modificar.")
        return

    st.dataframe(df)
    index = st.number_input("Índice a modificar", min_value=0, max_value=len(df)-1, step=1)

    if index is not None:
        registro = df.loc[index]
        nombre = st.text_input("Nuevo nombre", value=registro["Nombre"])
        fecha = st.date_input("Nueva fecha", value=pd.to_datetime(registro["Fecha"]))
        motivo = st.text_area("Nuevo motivo", value=registro["Incidencia"])
        estado = st.selectbox(
            "Estado", 
            ["Pendiente", "En proceso", "Terminado"],
            index=["Pendiente", "En proceso", "Terminado"].index(registro["Estado"])
        )

        if st.button("Guardar cambios"):
            df.at[index, "Nombre"] = nombre
            df.at[index, "Fecha"] = fecha.strftime("%Y-%m-%d")
            df.at[index, "Incidencia"] = motivo
            df.at[index, "Estado"] = estado
            guardar_datos(df)
            st.success("✅ Registro modificado correctamente")
            st.srerun()  # Actualizar la vista

# Función para mostrar resumen de incidencias
def mostrar_resumen_incidencias():
    df = cargar_datos()
    
    # Contar incidencias por estado
    total = len(df)
    pendientes = len(df[df["Estado"] == "Pendiente"])
    en_proceso = len(df[df["Estado"] == "En proceso"])
    terminadas = len(df[df["Estado"] == "Terminado"])
    
    # Crear tarjetas
    st.markdown("""
    <style>
    .card {
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
        margin: 10px;
        text-align: center;
        flex: 1;
    }
    .card-parent {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .cards-container {
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Tarjeta padre (resumen general)
    st.markdown(f"""
    <div class="card-parent">
        <h3 style="text-align: center; color: black;">Resumen de incidencias</h3>
        <div class="cards-container">
            <div class="card" style="background-color: #ffcccc; color: black;">
                <h4>Total</h4>
                <h2>{total}</h2>
            </div>
            <div class="card" style="background-color: #fff3cd; color: black;">
                <h4>Pendientes</h4>
                <h2>{pendientes}</h2>
            </div>
            <div class="card" style="background-color: #cce5ff; color: black;">
                <h4>En Proceso</h4>
                <h2>{en_proceso}</h2>
            </div>
            <div class="card" style="background-color: #d4edda; color: black;">
                <h4>Terminadas</h4>
                <h2>{terminadas}</h2>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
def satifaccion_cliente():
    if os.path.exists(FILENAME_SATIFACCION):
        df = pd.read_excel(FILENAME_SATIFACCION, sheet_name=SHEETNAME_SATIFACCION)
        return df
    else:
        return pd.DataFrame(columns=[
            "Fecha", 
            "Nombre", 
            "Apellido", 
            "Apellido2",
            "Correo Electronico", 
            "Diseño web", 
            "Velocidad de carga", 
            "Claridad a la navegación", 
            "Puntuación", 
            "Opiniones"
        ])

def guardar_satifiaccion_cliente(df):
    with pd.ExcelWriter(FILENAME_SATIFACCION, engine='openpyxl', mode='w') as writer:
        df.to_excel(writer, sheet_name=SHEETNAME_SATIFACCION, index=False)

def agregar_satifiaccion_cliente():
    st.subheader("Agregar nueva satisfacción del cliente")
    
    # Campos del formulario
    fecha = st.date_input("Fecha", value=datetime.today())
    nombre = st.text_input("Nombre")
    apellido = st.text_input("Apellido")
    apellido2 = st.text_input("Segundo apellido")
    correo = st.text_input("Correo Electronico")
    diseño = st.selectbox("Diseño web", options=list(range(1, 11)), index=9) 
    velocidad = st.selectbox("Velocidad de carga", options=list(range(1, 11)), index=9)
    claridad = st.selectbox("Claridad a la navegación", options=list(range(1, 11)), index=9)
    puntuacion = st.selectbox("Puntuación", options=list(range(1, 11)), index=9)
    opiniones = st.text_area("Opiniones")
    
    # Botón de registro
    if st.button("Registrar satisfacción"):
        if nombre and apellido and correo:
            try:
                df = satifaccion_cliente()
                nuevo = {
                    "Fecha": fecha.strftime("%Y-%m-%d"), 
                    "Nombre": nombre, 
                    "Apellido": apellido, 
                    "Apellido2": apellido2, 
                    "Correo Electronico": correo, 
                    "Diseño web": diseño, 
                    "Velocidad de carga": velocidad, 
                    "Claridad a la navegación": claridad, 
                    "Puntuación": puntuacion, 
                    "Opiniones": opiniones
                }
                df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
                guardar_satifiaccion_cliente(df)
                
                # Mensaje de éxito que SÍ se mostrará
                st.success("✅ Satisfacción registrada correctamente")
                
                # Opcional: Limpiar el formulario después de guardar
                st.session_state.clear()
                
            except Exception as e:
                st.error(f"❌ Error al guardar: {str(e)}")
        else:
            st.error("❌ Debes rellenar los campos obligatorios (Nombre, Apellido y Correo)")
            
            
def mostrar_resumen_satifiaccion_cliente():
    df = satifaccion_cliente()
    
    if df.empty:
        st.warning("No hay datos de satisfacción registrados")
        return
    
    # Cálculo de totales y medias
    total = len(df)
    media_diseño = df["Diseño web"].mean().round(2)
    media_velocidad = df["Velocidad de carga"].mean().round(2)
    media_claridad = df["Claridad a la navegación"].mean().round(2)
    media_puntuacion = df["Puntuación"].mean().round(2)
    
    # Crear tarjetas
    st.markdown("""
    <style>
    .card {
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
        margin: 10px;
        text-align: center;
        flex: 1;
        min-width: 150px;
    }
    .card-parent {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .cards-container {
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 10px;
    }
    .card-title {
        font-size: 1.1rem;
        margin-bottom: 10px;
        font-weight: bold;
    }
    .card-value {
        font-size: 1.8rem;
        margin: 10px 0;
    }
    .card-subtitle {
        font-size: 0.9rem;
        color: #555;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Tarjeta padre (resumen general)
    st.markdown(f"""
    <div class="card-parent">
        <h3 style="text-align: center; color: black; margin-bottom: 20px;">Satisfacción del Cliente</h3>
        <div class="cards-container">
            <!-- Tarjeta Total -->
            <div class="card" style="background-color: #f8f9fa;color: black; ">
                <div class="card-title">Total Encuestas</div>
                <div class="card-value">{total}</div>
                <div class="card-subtitle">Registros</div>
            </div>
    """, unsafe_allow_html=True)

    # Gráfico de distribución de puntuaciones
    st.subheader("Promedio de fatifíción")
    cols = st.columns(4)
    with cols[0]:
        st.metric("Diseño Web", f"{media_diseño}/10")
    with cols[1]:
        st.metric("Velocidad", f"{media_velocidad}/10")
    with cols[2]:
        st.metric("Claridad", f"{media_claridad}/10")
    with cols[3]:
        st.metric("Global", f"{media_puntuacion}/10")
    
    
def cargar_tareas():
    if os.path.exists(FILENAME_TAREAS):
        df = pd.read_excel(FILENAME_TAREAS, sheet_name=SHEETNAME_TAREAS)
        # Asegurar que el DataFrame tenga las columnas necesarias
        if "Estado" not in df.columns:
            df["Estado"] = "Pendiente"
        return df
    else:
        return pd.DataFrame(columns=["Tarea", "Descripción", "Fecha Creación", "Fecha Límite", "Estado"])

def guardar_tareas(df):
    with pd.ExcelWriter(FILENAME_TAREAS, engine='openpyxl', mode='w') as writer:
        df.to_excel(writer, sheet_name=SHEETNAME_TAREAS, index=False)

def agregar_tarea():
    st.subheader("Agregar nueva tarea")
    
    with st.form("form_tarea"):
        tarea = st.text_input("Nombre de la tarea*")
        descripcion = st.text_area("Descripción")
        fecha_creacion = st.date_input("Fecha de creación", value=datetime.today())
        fecha_limite = st.date_input("Fecha límite", value=datetime.today())
        estado = st.selectbox("Estado", ["Pendiente", "En proceso", "Finalizada"])
        
        if st.form_submit_button("Guardar tarea"):
            if tarea:
                df = cargar_tareas()
                nueva_tarea = {
                    "Tarea": tarea,
                    "Descripción": descripcion,
                    "Fecha Creación": fecha_creacion.strftime("%Y-%m-%d"),
                    "Fecha Límite": fecha_limite.strftime("%Y-%m-%d"),
                    "Estado": estado
                }
                df = pd.concat([df, pd.DataFrame([nueva_tarea])], ignore_index=True)
                guardar_tareas(df)
                st.success("✅ Tarea registrada correctamente")
            else:
                st.error("❌ El nombre de la tarea es obligatorio")

def editar_estado_tarea():
    st.subheader("Actualizar estado de tarea")
    df = cargar_tareas()
    
    if df.empty:
        st.info("No hay tareas registradas")
        return
    
    # Mostrar solo tareas no finalizadas para edición
    tareas_editables = df[df["Estado"] != "Finalizada"]
    
    if tareas_editables.empty:
        st.info("Todas las tareas están finalizadas")
        return
    
    tarea_seleccionada = st.selectbox(
        "Seleccione tarea a actualizar",
        options=tareas_editables["Tarea"].unique()
    )
    
    tarea_data = df[df["Tarea"] == tarea_seleccionada].iloc[0]
    
    st.write(f"**Descripción:** {tarea_data['Descripción']}")
    st.write(f"**Fecha Límite:** {tarea_data['Fecha Límite']}")
    st.write(f"**Estado actual:** {tarea_data['Estado']}")
    
    nuevo_estado = st.selectbox(
        "Nuevo estado",
        ["Pendiente", "En proceso", "Finalizada"],
        index=["Pendiente", "En proceso", "Finalizada"].index(tarea_data["Estado"])
    )
    
    if st.button("Actualizar estado"):
        df.loc[df["Tarea"] == tarea_seleccionada, "Estado"] = nuevo_estado
        guardar_tareas(df)
        st.success(f"✅ Estado de '{tarea_seleccionada}' actualizado a '{nuevo_estado}'")
        st.rerun()
        
def mostrar_resumen_tareas():
    df = cargar_tareas()
    
    if df.empty:
        st.warning("No hay tareas registradas")
        return
    
    # Estadísticas
    total = len(df)
    pendientes = len(df[df["Estado"] == "Pendiente"])
    en_proceso = len(df[df["Estado"] == "En proceso"])
    finalizadas = len(df[df["Estado"] == "Finalizada"])
    
    # Estilos para las tarjetas
    st.markdown("""
    <style>
    .card-container-tareas {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 15px;
        margin: 20px 0;
    }
    .card-tarea {
        background: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        padding: 15px;
        text-align: center;
    }
    .card-titulo {
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 10px;
    }
    .card-valor {
        font-size: 24px;
        font-weight: 700;
        margin: 10px 0;
    }
    .card-pendiente { border-left: 4px solid #ff6b6b; }
    .card-proceso { border-left: 4px solid #ffd166; }
    .card-finalizada { border-left: 4px solid #06d6a0; }
    .card-total { border-left: 4px solid #118ab2; }
    </style>
    """, unsafe_allow_html=True)
    
    # Tarjetas de resumen
    st.markdown(f"""
    <div class="card-container-tareas">
        <div class="card-tarea card-total">
            <div class="card-titulo">Total Tareas</div>
            <div class="card-valor">{total}</div>
        </div>
        <div class="card-tarea card-pendiente">
            <div class="card-titulo">Pendientes</div>
            <div class="card-valor">{pendientes}</div>
        </div>
        <div class="card-tarea card-proceso">
            <div class="card-titulo">En Proceso</div>
            <div class="card-valor">{en_proceso}</div>
        </div>
        <div class="card-tarea card-finalizada">
            <div class="card-titulo">Finalizadas</div>
            <div class="card-valor">{finalizadas}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabla de tareas
    st.subheader("Listado de Tareas")
    st.dataframe(df.sort_values(by="Fecha Límite"))

def mostrar_resumen_tareas():
    df = cargar_tareas()
    
    if df.empty:
        st.warning("No hay tareas registradas")
        return
    
    # Estadísticas
    total = len(df)
    pendientes = len(df[df["Estado"] == "Pendiente"])
    en_proceso = len(df[df["Estado"] == "En proceso"])
    finalizadas = len(df[df["Estado"] == "Finalizada"])
    
    # Estilos para las tarjetas
    st.markdown("""
    <style>
    .card-container-tareas {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 15px;
        margin: 20px 0;
        color: black;
    }
    .card-tarea {
        background: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        padding: 15px;
        text-align: center;
    }
    .card-titulo {
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 10px;
    }
    .card-valor {
        font-size: 24px;
        font-weight: 700;
        margin: 10px 0;
    }
    .card-pendiente { border-left: 4px solid #ff6b6b; }
    .card-proceso { border-left: 4px solid #ffd166; }
    .card-finalizada { border-left: 4px solid #06d6a0; }
    .card-total { border-left: 4px solid #118ab2; }
    </style>
    """, unsafe_allow_html=True)
    
    # Tarjetas de resumen
    st.markdown(f"""
    <div class="card-container-tareas">
        <div class="card-tarea card-total">
            <div class="card-titulo">Total Tareas</div>
            <div class="card-valor">{total}</div>
        </div>
        <div class="card-tarea card-pendiente">
            <div class="card-titulo">Pendientes</div>
            <div class="card-valor">{pendientes}</div>
        </div>
        <div class="card-tarea card-proceso">
            <div class="card-titulo">En Proceso</div>
            <div class="card-valor">{en_proceso}</div>
        </div>
        <div class="card-tarea card-finalizada">
            <div class="card-titulo">Finalizadas</div>
            <div class="card-valor">{finalizadas}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabla de tareas
    st.subheader("Listado de Tareas")
    st.dataframe(df.sort_values(by="Fecha Límite"))


# Interfaz principal
st.set_page_config(layout="wide")

# --- Menú principal en el sidebar ---
menu_principal = st.sidebar.selectbox(
    "Menú Principal",
    ["Incidencias", "Tasa de Error", "Satisfacción del Cliente", "Tareas"]
)

if menu_principal == "Incidencias":
    
    # --- Submenú de Incidencias ---
    submenu = st.radio(
        "Operaciones",
        ["Agregar", "Mostrar", "Eliminar", "Modificar"],
        horizontal=True
    )
    
    if submenu == "Agregar":
        agregar_incidencia()
    elif submenu == "Mostrar":
        mostrar_incidencias()
    elif submenu == "Eliminar":
        eliminar_incidencia()
    elif submenu == "Modificar":
        modificar_incidencia()

elif menu_principal == "Tasa de Error":
    st.title("Tasa de Error")
    mostrar_resumen_incidencias()
    mostrar_resumen_satifiaccion_cliente()
    

elif menu_principal == "Satisfacción del Cliente":
    st.title("Satisfacción del Cliente")
    agregar_satifiaccion_cliente()

elif menu_principal == "Tareas":
    st.title("Gestión de Tareas")
    
    opcion_tarea = st.radio(
        "Operaciones",
        ["Resumen", "Agregar Tarea", "Editar Estado"],
        horizontal=True
    )
    
    if opcion_tarea == "Resumen":
        mostrar_resumen_tareas()
    elif opcion_tarea == "Agregar Tarea":
        agregar_tarea()
    elif opcion_tarea == "Editar Estado":
        editar_estado_tarea()