def enviar_notificacion_incidencia(empresa_nombre: str, modelo_toner: str, tipo_falla: str):
    # Lógica para envío vía SMTP
    print(f"[ALERTA ECOINV] La empresa '{empresa_nombre}' reportó falla en el tóner {modelo_toner}: {tipo_falla}")