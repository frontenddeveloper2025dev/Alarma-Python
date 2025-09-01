import streamlit as st
import pandas as pd
import datetime
import time
from database import AlarmDatabase
from alarm_monitor import AlarmMonitor
import threading

# Initialize session state
if 'alarm_db' not in st.session_state:
    st.session_state.alarm_db = AlarmDatabase()

if 'alarm_monitor' not in st.session_state:
    st.session_state.alarm_monitor = AlarmMonitor(st.session_state.alarm_db)
    # Start monitoring in background
    monitor_thread = threading.Thread(target=st.session_state.alarm_monitor.start_monitoring, daemon=True)
    monitor_thread.start()

# Page configuration
st.set_page_config(
    page_title="Alarm Tool",
    page_icon="⏰",
    layout="wide"
)

st.title("⏰ Herramienta de Alarma")
st.markdown("Configure alarmas recurrentes semanales con notificaciones de audio")

# Sidebar for creating new alarms
with st.sidebar:
    st.header("➕ Crear Nueva Alarma")
    
    with st.form("new_alarm_form"):
        alarm_name = st.text_input("Nombre de la Alarma", placeholder="Mi Alarma")
        
        # Time input
        alarm_time = st.time_input("Hora", value=datetime.time(8, 0))
        
        # Days selection
        st.write("Días de la semana:")
        days = {
            'monday': st.checkbox("Lunes"),
            'tuesday': st.checkbox("Martes"),
            'wednesday': st.checkbox("Miércoles"),
            'thursday': st.checkbox("Jueves"),
            'friday': st.checkbox("Viernes"),
            'saturday': st.checkbox("Sábado"),
            'sunday': st.checkbox("Domingo")
        }
        
        submit_button = st.form_submit_button("Crear Alarma")
        
        if submit_button:
            if not alarm_name.strip():
                st.error("Por favor, ingrese un nombre para la alarma")
            elif not any(days.values()):
                st.error("Por favor, seleccione al menos un día")
            else:
                selected_days = [day for day, selected in days.items() if selected]
                success = st.session_state.alarm_db.create_alarm(
                    name=alarm_name.strip(),
                    time=alarm_time,
                    days=selected_days
                )
                if success:
                    st.success("¡Alarma creada exitosamente!")
                    st.rerun()
                else:
                    st.error("Error al crear la alarma")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📋 Mis Alarmas")
    
    # Get all alarms
    alarms = st.session_state.alarm_db.get_all_alarms()
    
    if not alarms:
        st.info("No hay alarmas configuradas. Crea tu primera alarma usando el panel lateral.")
    else:
        # Display alarms
        for alarm in alarms:
            with st.container():
                col_info, col_toggle, col_delete = st.columns([3, 1, 1])
                
                with col_info:
                    status_icon = "🟢" if alarm['is_active'] else "🔴"
                    days_str = ", ".join([day.capitalize() for day in alarm['days']])
                    st.write(f"{status_icon} **{alarm['name']}** - {alarm['time']} - {days_str}")
                
                with col_toggle:
                    if st.button("Activar" if not alarm['is_active'] else "Desactivar", 
                               key=f"toggle_{alarm['id']}"):
                        st.session_state.alarm_db.toggle_alarm(alarm['id'])
                        st.rerun()
                
                with col_delete:
                    if st.button("🗑️", key=f"delete_{alarm['id']}", help="Eliminar alarma"):
                        st.session_state.alarm_db.delete_alarm(alarm['id'])
                        st.rerun()
                
                st.divider()

with col2:
    st.header("⏱️ Estado del Sistema")
    
    # Current time display
    current_time = datetime.datetime.now()
    st.metric("Hora Actual", current_time.strftime("%H:%M:%S"))
    st.metric("Fecha", current_time.strftime("%d/%m/%Y"))
    
    # Active alarms count
    active_alarms = len([a for a in alarms if a['is_active']])
    st.metric("Alarmas Activas", active_alarms)
    
    # Next alarm info
    next_alarm = st.session_state.alarm_db.get_next_alarm()
    if next_alarm:
        st.write("**Próxima Alarma:**")
        st.write(f"📌 {next_alarm['name']}")
        next_time = next_alarm['next_trigger']
        if next_time:
            st.write(f"🕐 {next_time.strftime('%A, %d/%m/%Y a las %H:%M')}")
    else:
        st.write("**Próxima Alarma:**")
        st.write("No hay alarmas activas")

# Recent alarms section
st.header("🔔 Historial Reciente")
recent_alarms = st.session_state.alarm_db.get_recent_triggered_alarms()

if recent_alarms:
    for alarm in recent_alarms:
        trigger_time = datetime.datetime.fromisoformat(alarm['triggered_at'])
        time_ago = datetime.datetime.now() - trigger_time
        
        if time_ago.days > 0:
            time_str = f"hace {time_ago.days} días"
        elif time_ago.seconds > 3600:
            hours = time_ago.seconds // 3600
            time_str = f"hace {hours} horas"
        elif time_ago.seconds > 60:
            minutes = time_ago.seconds // 60
            time_str = f"hace {minutes} minutos"
        else:
            time_str = "hace menos de un minuto"
        
        st.write(f"🔔 **{alarm['name']}** sonó {time_str}")
else:
    st.info("No hay alarmas recientes")

# Auto-refresh every 30 seconds
time.sleep(1)
st.rerun()
