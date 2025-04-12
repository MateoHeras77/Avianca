import datetime
import streamlit as st
from typing import Dict, Any, Tuple

from src.utils.form_utils import validate_time_field, format_time_for_database
from src.config.logging_config import setup_logger

# Configurar logger
logger = setup_logger()

def render_flight_form() -> Tuple[bool, Dict[str, Any]]:
    """
    Renderiza el formulario de vuelo y procesa los datos ingresados.
    
    Returns:
        tuple: (formulario_enviado, datos_procesados) donde:
            - formulario_enviado: bool que indica si el formulario fue enviado y validado
            - datos_procesados: diccionario con los datos procesados o None
    """
    with st.form("flight_form"):
        st.subheader("🚀 Datos Básicos")
        col1, col2, col3 = st.columns(3)
        with col1:
            flight_date = st.date_input("📅 Fecha de vuelo", datetime.date.today(), key="flight_date")
        with col2:
            origin = st.selectbox("🌍 Origen", ["YYZ"], index=0, key="origin")
        with col3:
            destination = st.selectbox("✈️ Destino", ["", "BOG", "SAL"], index=0, key="destination")

        flight_number = st.selectbox("🔢 Número de vuelo", ["", "AV205", "AV255", "AV627"], key="flight_number", format_func=lambda x: "Elegir vuelo" if x == "" else x)

        st.subheader("⏰ Tiempos")
        col3, col4 = st.columns(2)
        with col3:
            std = st.text_input("STD (Salida Programada)", value="", placeholder="HH:MM", key="std")
            atd = st.text_input("ATD (Salida Real)", value="", placeholder="HH:MM", key="atd")
            groomers_in = st.text_input("Groomers In", value="", placeholder="HH:MM", key="groomers_in")
            groomers_out = st.text_input("Groomers Out", value="", placeholder="HH:MM", key="groomers_out")
        with col4:
            crew_at_gate = st.text_input("Crew at Gate", value="", placeholder="HH:MM", key="crew_at_gate")
            ok_to_board = st.text_input("OK to Board", value="", placeholder="HH:MM", key="ok_to_board")
            flight_secure = st.text_input("Flight Secure", value="", placeholder="HH:MM", key="flight_secure")
            cierre_de_puerta = st.text_input("Cierre de Puerta", value="", placeholder="HH:MM", key="cierre_de_puerta")
            push_back = st.text_input("Push Back", value="", placeholder="HH:MM", key="push_back")

        st.subheader("📋 Información de Customs")
        col_customs1, col_customs2 = st.columns(2)
        with col_customs1:
            customs_in = st.text_input("Customs In", value="No Customs", placeholder="HH:MM", key="customs_in")
        with col_customs2:
            customs_out = st.text_input("Customs Out", value="No Customs", placeholder="HH:MM", key="customs_out")

        st.subheader("👥 Información de Pasajeros")
        col_pax1, col_pax2 = st.columns(2)
        with col_pax1:
            # Lista desplegable para Total Pax (0-200)
            total_pax_options = [str(i) for i in range(201)]
            total_pax = st.selectbox(
                "Total Pax", 
                options=total_pax_options,
                index=0,  # Valor por defecto: 0
                key="total_pax"
            )
            
            # Lista desplegable para PAX C (0-18)
            pax_c_options = [str(i) for i in range(19)]
            pax_c = st.selectbox(
                "PAX C", 
                options=pax_c_options,
                index=0,  # Valor por defecto: 0
                key="pax_c"
            )
        with col_pax2:
            # Lista desplegable para PAX Y (0-200)
            pax_y_options = [str(i) for i in range(201)]
            pax_y = st.selectbox(
                "PAX Y", 
                options=pax_y_options,
                index=0,  # Valor por defecto: 0
                key="pax_y"
            )
            
            # Lista desplegable para Infantes (0-200)
            infants_options = [str(i) for i in range(201)]
            infants = st.selectbox(
                "Infantes", 
                options=infants_options,
                index=0,  # Valor por defecto: 0
                key="infants"
            )

        st.subheader("⏳ Información por Demoras")
        col_delay1, col_delay2 = st.columns(2)
        with col_delay1:
            # Crear una lista de opciones de 0 a 200 para el selector de delay, más la opción adicional
            delay_options = [str(i) for i in range(201)] + [">200 Escribir en comentarios"]
            delay = st.selectbox(
                "Delay (Ingresar minutos de demora)", 
                options=delay_options,
                index=0,  # Valor por defecto: 0
                key="delay"
            )
        with col_delay2:
            delay_code = st.text_area("Delay Code (Reporte)", placeholder="Ingresar los codigos del retraso",value="", key="delay_code")

        # Actualizar etiquetas de WCHR y Agentes eliminando "AV2**" y simplificando el código
        wchr_current_label = "WCHR Vuelo Salida (AV255 - AV627 - AV205)"
        agents_current_label = "Agentes Vuelo Salida (AV255 - AV627 - AV205)"

        # Determinar el vuelo anterior basado en el número de vuelo seleccionado
        previous_flight_mapping = {
            "AV205": "AV204",
            "AV627": "AV626",
            "AV255": "AV254"
        }
        previous_flight = previous_flight_mapping.get(flight_number, "")
        wchr_previous_label = "WCHR Vuelo Llegada (AV254 - AV626 - AV204)"
        agents_previous_label = "Agentes Vuelo Llegada (AV254 - AV626 - AV204)"

        st.subheader("💬 WCHR")
        col_wchr1, col_wchr2 = st.columns(2)
        with col_wchr1:
            wchr_current_flight = st.text_area(wchr_current_label, value=" 00 WCHR | 00 WCHC", placeholder="(AV255 - AV627 - AV205) Cantidad de WCHR / WCHC / DEAF etc",key="wchr_current_flight")
            wchr_previous_flight = st.text_area(wchr_previous_label, value="00 WCHR | 00 WCHC",placeholder="(AV254 - AV626 - AV204) Cantidad de WCHR / WCHC / DEAF etc", key="wchr_previous_flight")
        with col_wchr2:
            # Crear lista de opciones para agentes (0-20 + opción adicional)
            agent_options = [str(i) for i in range(21)] + ["> 20 Escribir en comentarios"]
            
            # Selectbox para agentes de vuelo de salida
            agents_current_flight = st.selectbox(
                agents_current_label,
                options=agent_options,
                index=0,  # Valor por defecto: 0
                key="agents_current_flight"
            )
            
            # Selectbox para agentes de vuelo de llegada
            agents_previous_flight = st.selectbox(
                agents_previous_label,
                options=agent_options,
                index=0,  # Valor por defecto: 0
                key="agents_previous_flight"
            )

        st.subheader("📍 Información de Gate y Carrusel")
        col_gate1, col_gate2 = st.columns(2)
        with col_gate1:
            gate = st.text_input("Gate", key="gate").strip()
        with col_gate2:
            carrousel = st.text_input("Carrousel", key="carrousel").strip()

        st.subheader("💬 Comentarios")
        comments = st.text_area("Comentarios", value="", height=150,placeholder="Ingresar comentarios generales", key="comments")

        # Nuevo campo para Información de Gate Bag
        st.subheader("🧳  Información del Gate Bag")
        gate_bag = st.text_area("Información de Gate Bag", value="", height=150, placeholder="Ingresar status del gate bag. (Ejm: Faltan boarding pass, hojas del reporte, etc)", key="gate_bag")

        submitted = st.form_submit_button("🔍 Revisar")

    if submitted:
        return process_form_data(
                flight_date, origin, destination, flight_number,
                std, atd, groomers_in, groomers_out, crew_at_gate,
                ok_to_board, flight_secure, cierre_de_puerta, push_back,
                total_pax, pax_c, pax_y, infants, customs_in, customs_out,
                delay, gate, carrousel, delay_code,
                wchr_current_flight, wchr_previous_flight,
                agents_current_flight, agents_previous_flight, comments, gate_bag
            )
    else:
        return False, None


def process_form_data(
    flight_date, origin, destination, flight_number,
    std, atd, groomers_in, groomers_out, crew_at_gate,
    ok_to_board, flight_secure, cierre_de_puerta, push_back,
    total_pax, pax_c, pax_y, infants, customs_in, customs_out,
    delay, gate, carrousel, delay_code,
    wchr_current_flight, wchr_previous_flight,
    agents_current_flight, agents_previous_flight, comments, gate_bag
) -> Tuple[bool, Dict[str, Any]]:
    """
    Procesa y valida los datos del formulario.
    
    Returns:
        tuple: (es_valido, datos) donde:
            - es_valido: bool indicando si los datos son válidos
            - datos: dict con los datos procesados o None
    """
    logger.info("Procesando datos del formulario")

    # Validar campos obligatorios
    required_fields = {
        "Fecha de vuelo": flight_date,
        "Origen": origin,
        "Destino": destination,
        "Número de vuelo": flight_number,
        "Total Pax": total_pax,
        "Gate": gate,
        "Carrousel": carrousel,
        "WCHR": wchr_current_flight,
    }
    missing = [k for k, v in required_fields.items() if not v or str(v).strip() == ""]
    if missing:
        st.error("Complete los siguientes campos: " + ", ".join(missing))
        logger.warning(f"Faltan campos obligatorios: {missing}")
        return False, None

    # Validar campos de tiempo
    time_fields = {
        "STD": std,
        "ATD": atd,
        "Groomers In": groomers_in,
        "Groomers Out": groomers_out,
        "Crew at Gate": crew_at_gate,
        "OK to Board": ok_to_board,
        "Flight Secure": flight_secure,
        "Cierre de Puerta": cierre_de_puerta,
        "Push Back": push_back
    }

    all_valid = True
    normalized_times = {}
    for label, value in time_fields.items():
        valid, result = validate_time_field(value, label)
        if not valid:
            st.error(result)
            logger.warning(f"Campo de tiempo inválido: {label} - {result}")
            all_valid = False
        else:
            normalized_times[label] = result

    if not all_valid:
        return False, None

    # Validar campos obligatorios y numéricos para pasajeros
    passenger_fields = {
        "Total Pax": total_pax,
        "PAX C": pax_c,
        "PAX Y": pax_y,
        "Infantes": infants
    }

    for field_name, value in passenger_fields.items():
        if not value.strip():
            st.error(f"El campo '{field_name}' es obligatorio.")
            logger.warning(f"Campo obligatorio faltante: {field_name}")
            return False, None
        if not value.isdigit():
            st.error(f"El campo '{field_name}' debe contener únicamente números.")
            logger.warning(f"Campo no numérico: {field_name} - Valor ingresado: {value}")
            return False, None

    # Ya no se valida que el campo delay sea numérico, ahora acepta cualquier texto
    
    # Ya no se validan los campos de agentes como numéricos, ahora aceptan cualquier texto

    # Actualizar el esquema de datos para reflejar los cambios en la base de datos
    database_data = {
        "flight_date": flight_date.isoformat(),
        "origin": origin,
        "destination": destination,
        "flight_number": flight_number,
        "std": format_time_for_database(normalized_times["STD"]),
        "atd": format_time_for_database(normalized_times["ATD"]),
        "groomers_in": format_time_for_database(normalized_times["Groomers In"]),
        "groomers_out": format_time_for_database(normalized_times["Groomers Out"]),
        "crew_at_gate": format_time_for_database(normalized_times["Crew at Gate"]),
        "ok_to_board": format_time_for_database(normalized_times["OK to Board"]),
        "flight_secure": format_time_for_database(normalized_times["Flight Secure"]),
        "cierre_de_puerta": format_time_for_database(normalized_times["Cierre de Puerta"]),
        "push_back": format_time_for_database(normalized_times["Push Back"]),
        "pax_c": pax_c,
        "pax_y": pax_y,
        "infants": infants,
        "customs_in": customs_in,
        "customs_out": customs_out,
        "delay": delay,
        "gate": gate,
        "carrousel": carrousel,
        "delay_code": delay_code,
        "wchr_previous_flight": wchr_previous_flight,
        "agents_previous_flight": agents_previous_flight,
        "agents_current_flight": agents_current_flight,
        "wchr_current_flight": wchr_current_flight,
        "comments": comments,
        "gate_bag": gate_bag
    }

    # Revertir formato de tiempo para visualización
    display_data = database_data.copy()
    for key in normalized_times.keys():
        field_name = key.lower().replace(" ", "_")
        if display_data[field_name]:
            display_data[field_name] = normalized_times[key]

    # Asegurar que el valor de Total Pax se incluya en los datos enviados y en el reporte
    database_data["pax_ob_total"] = total_pax
    display_data["pax_ob_total"] = total_pax

    logger.info("Datos del formulario procesados y validados correctamente")

    return True, {
        "data_to_display": display_data,
        "data_for_database": database_data
    }