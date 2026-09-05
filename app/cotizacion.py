from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


def generar_cotizacion_pdf(
    ruc_proveedor: str,
    razon_social_proveedor: str,
    id_proveedor: int,
    facturas: list[dict],
    ruta_salida: str | Path = "cotizacion_factoring.pdf"
) -> str:
    
    #Genera el PDF comercial de una cotización de factoring.

    #La función:
    #- No consulta base de datos.
    #- No calcula nuevamente las condiciones financieras.
    #- Recibe los resultados ya obtenidos previamente.
    #- Puede recibir una o varias facturas.
    #- Las facturas pueden pertenecer a uno o varios adquirentes pero siempre al mismo proveedor.

    #Parámetros
    #----------
    #ruc_proveedor : str
    #razon_social_proveedor : str
    #id_proveedor : int
    #    0 si el proveedor es nuevo.
    #    > 0 si ya está registrado.

    #facturas : list[dict]
    #    Cada elemento debe contener:
    #    {
    #        "ruc_adquirente": str,
    #        "razon_social_adquirente": str,
    #        "id_adquirente": int,
    #        "TEM": Decimal,
    #        "FactorAdelanto": Decimal,
    #        "importe": Decimal,
    #        "fecha_pago": date,
    #        "Plazo": int,
    #        "ImporteAdelanto": Decimal,
    #        "Interes": Decimal,
    #        "IGV": Decimal,
    #        "ImporteDesembolsar": Decimal,
    #        "ImporteRemanente": Decimal
    #    }

    #ruta_salida : str | Path
    #    Archivo PDF que será generado.

    #Retorna
    #-------
    #str
    #    Ruta del PDF generado.

    # ---------------------------------------------------------
    # Validación estructural mínima
    # ---------------------------------------------------------

    if not facturas:
        raise ValueError("La cotización debe contener al menos una factura.")
    ruta_salida = Path(ruta_salida)

    # ---------------------------------------------------------
    # Colores
    # ---------------------------------------------------------
    COLOR_PRINCIPAL = HexColor("#17365D")
    COLOR_SECUNDARIO = HexColor("#2F75B5")

    COLOR_CABECERA = HexColor("#EAF2F8")
    COLOR_FILA = HexColor("#F7F9FB")
    COLOR_BORDE = HexColor("#D5DCE3")

    COLOR_TEXTO = HexColor("#222222")
    COLOR_TEXTO_SECUNDARIO = HexColor("#666666")

    COLOR_NUEVO = HexColor("#FFF6E6")
    COLOR_NUEVO_BORDE = HexColor("#E5B96A")

    COLOR_REGISTRADO = HexColor("#EEF7EE")
    COLOR_REGISTRADO_BORDE = HexColor("#A8C9A8")

    # ---------------------------------------------------------
    # Página
    # ---------------------------------------------------------

    ancho_pagina, alto_pagina = A4

    # Dejamos poco espacio lateral para aprovechar la tabla.
    margen_izquierdo = 0.70 * cm
    margen_derecho = 0.70 * cm

    documento = SimpleDocTemplate(
        str(ruta_salida),
        pagesize=A4,
        leftMargin=margen_izquierdo,
        rightMargin=margen_derecho,
        topMargin=1.10 * cm,
        bottomMargin=1.30 * cm,
    )

    ancho_util = ( ancho_pagina - margen_izquierdo - margen_derecho )

    # ---------------------------------------------------------
    # Estilos
    # ---------------------------------------------------------

    estilos = getSampleStyleSheet()

    estilo_titulo = ParagraphStyle(
        "TituloCotizacion",
        parent=estilos["Title"],
        fontName="Helvetica-Bold",
        fontSize=17,
        leading=20,
        textColor=COLOR_PRINCIPAL,
        alignment=TA_RIGHT,
        spaceAfter=2,
    )

    estilo_derecha = ParagraphStyle(
        "TextoDerecha",
        parent=estilos["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
        textColor=COLOR_TEXTO_SECUNDARIO,
        alignment=TA_RIGHT,
    )

    estilo_seccion = ParagraphStyle(
        "Seccion",
        parent=estilos["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=13,
        textColor=COLOR_PRINCIPAL,
        spaceBefore=8,
        spaceAfter=5,
    )

    estilo_label = ParagraphStyle(
        "Label",
        parent=estilos["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=COLOR_TEXTO_SECUNDARIO,
    )

    estilo_valor = ParagraphStyle(
        "Valor",
        parent=estilos["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9.2,
        leading=11,
        textColor=COLOR_TEXTO,
    )

    estilo_detalle = ParagraphStyle(
        "Detalle",
        parent=estilos["Normal"],
        fontName="Helvetica",
        fontSize=7.2,
        leading=8.5,
        textColor=COLOR_TEXTO,
    )

    estilo_detalle_cabecera = ParagraphStyle(
        "DetalleCabecera",
        parent=estilo_detalle,
        fontName="Helvetica-Bold",
        fontSize=6.8,
        leading=8,
        textColor=colors.white,
    )

    estilo_observacion = ParagraphStyle(
        "Observacion",
        parent=estilos["Normal"],
        fontName="Helvetica",
        fontSize=8.2,
        leading=11.2,
        textColor=COLOR_TEXTO,
    )

    # ---------------------------------------------------------
    # Funciones internas de presentación
    # ---------------------------------------------------------

    def formato_moneda(valor):
        return f"S/ {Decimal(valor):,.2f}"

    def formato_fecha(valor):

        if isinstance(valor, datetime):
            return valor.strftime("%d/%m/%Y")

        if isinstance(valor, date):
            return valor.strftime("%d/%m/%Y")

        return str(valor)

    def formato_porcentaje(valor, decimales=2):
        return f"{Decimal(valor):.{decimales}f}%"

    # ---------------------------------------------------------
    # Estados comerciales
    # ---------------------------------------------------------

    proveedor_nuevo = id_proveedor == 0

    existe_adquirente_nuevo = any(
        factura["id_adquirente"] == 0
        for factura in facturas
    )

    estado_proveedor = (
        "Nuevo"
        if proveedor_nuevo
        else "Registrado"
    )

    # ---------------------------------------------------------
    # Totales
    #
    # Son únicamente agregaciones para presentación.
    # No hay recálculo financiero.
    # ---------------------------------------------------------

    importe_total = sum(
        Decimal(f["Importe"])
        for f in facturas
    )

    adelanto_total = sum(
        Decimal(f["ImporteAdelanto"])
        for f in facturas
    )

    interes_total = sum(
        Decimal(f["Interes"])
        for f in facturas
    )

    igv_total = sum(
        Decimal(f["IGV"])
        for f in facturas
    )

    desembolso_total = sum(
        Decimal(f["ImporteDesembolsar"])
        for f in facturas
    )

    remanente_total = sum(
        Decimal(f["ImporteRemanente"])
        for f in facturas
    )

    # ---------------------------------------------------------
    # Documento
    # ---------------------------------------------------------

    elementos = []

    # =========================================================
    # CABECERA
    # =========================================================

    logo = Table(
        [[
            Paragraph(
                "<b>FACTOR</b><br/>"
                "<font size='7'>Financiamiento de facturas</font>",
                ParagraphStyle(
                    "Logo",
                    fontName="Helvetica",
                    fontSize=14,
                    leading=14,
                    textColor=colors.white,
                ),
            )
        ]],
        colWidths=[4 * cm],
        rowHeights=[1.45 * cm],
    )

    logo.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, -1),
                COLOR_PRINCIPAL
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                10
            ),
        ])
    )

    fecha_emision = date.today()

    encabezado_derecho = [
        Paragraph(
            "COTIZACIÓN DE FACTORING",
            estilo_titulo
        ),
        Paragraph(
            f"Fecha de emisión: "
            f"{fecha_emision.strftime('%d/%m/%Y')}",
            estilo_derecha,
        ),
        Paragraph(
            "Vigencia: hasta 15 días desde su emisión",
            estilo_derecha,
        ),
    ]

    tabla_encabezado = Table(
        [[logo, encabezado_derecho]],
        colWidths=[
            4.3 * cm,
            ancho_util - 4.3 * cm,
        ],
    )

    tabla_encabezado.setStyle(
        TableStyle([
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP"
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                0
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                0
            ),
        ])
    )

    elementos.append(tabla_encabezado)
    elementos.append(Spacer(1, 8))

    # =========================================================
    # PROVEEDOR
    # =========================================================

    elementos.append(
        Paragraph(
            "Proveedor",
            estilo_seccion
        )
    )

    tabla_proveedor = Table(
        [
            [
                Paragraph("RUC", estilo_label),
                Paragraph("Razón social", estilo_label),
                Paragraph("Estado", estilo_label),
            ],
            [
                Paragraph(
                    str(ruc_proveedor),
                    estilo_valor
                ),
                Paragraph(
                    razon_social_proveedor,
                    estilo_valor
                ),
                Paragraph(
                    estado_proveedor,
                    estilo_valor
                ),
            ],
        ],
        colWidths=[
            ancho_util * 0.20,
            ancho_util * 0.57,
            ancho_util * 0.23,
        ],
    )

    tabla_proveedor.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                COLOR_FILA
            ),
            (
                "BOX",
                (0, 0),
                (-1, -1),
                0.5,
                COLOR_BORDE
            ),
            (
                "INNERGRID",
                (0, 0),
                (-1, -1),
                0.3,
                COLOR_BORDE
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                6
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                6
            ),
        ])
    )

    elementos.append(tabla_proveedor)

    # =========================================================
    # RESUMEN
    # =========================================================

    elementos.append(
        Paragraph(
            "Resumen de la cotización",
            estilo_seccion
        )
    )

    tabla_resumen = Table(
        [
            [
                Paragraph(
                    "Facturas",
                    estilo_label
                ),
                Paragraph(
                    "Importe total",
                    estilo_label
                ),
                Paragraph(
                    "Adelanto total",
                    estilo_label
                ),
                Paragraph(
                    "Desembolso total",
                    estilo_label
                ),
            ],
            [
                Paragraph(
                    str(len(facturas)),
                    estilo_valor
                ),
                Paragraph(
                    formato_moneda(importe_total),
                    estilo_valor
                ),
                Paragraph(
                    formato_moneda(adelanto_total),
                    estilo_valor
                ),
                Paragraph(
                    formato_moneda(desembolso_total),
                    estilo_valor
                ),
            ],
        ],
        colWidths=[
            ancho_util * 0.15,
            ancho_util * 0.28,
            ancho_util * 0.28,
            ancho_util * 0.29,
        ],
    )

    tabla_resumen.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                COLOR_CABECERA
            ),
            (
                "BOX",
                (0, 0),
                (-1, -1),
                0.5,
                COLOR_SECUNDARIO
            ),
            (
                "INNERGRID",
                (0, 0),
                (-1, -1),
                0.3,
                COLOR_BORDE
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
            (
                "ALIGN",
                (1, 1),
                (-1, 1),
                "RIGHT"
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                6
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                6
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                5
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                5
            ),
        ])
    )

    elementos.append(tabla_resumen)

    # =========================================================
    # DETALLE DE FACTURAS
    # =========================================================

    elementos.append(
        Paragraph(
            "Detalle de facturas",
            estilo_seccion
        )
    )

    cabecera_detalle = [
        "#",
        "Adquirente",
        "Importe",
        "Fecha pago",
        "Plazo",
        "TEM",
        "Factor",
        "Adelanto",
        "Interés",
        "IGV",
        "Desembolso",
        "Remanente",
    ]

    filas_detalle = [
        [
            Paragraph(
                texto,
                estilo_detalle_cabecera
            )
            for texto in cabecera_detalle
        ]
    ]

    for numero, factura in enumerate(
        facturas,
        start=1
    ):

        adquirente = (
            f"<b>{factura['ruc_adquirente']}</b> "
            f"{factura['razon_social_adquirente']}"
        )

        fila = [
            Paragraph(
                str(numero),
                estilo_detalle
            ),
            Paragraph(
                adquirente,
                estilo_detalle
            ),
            Paragraph(
                formato_moneda(
                    factura["Importe"]
                ),
                estilo_detalle
            ),
            Paragraph(
                formato_fecha(
                    factura["fecha_pago"]
                ),
                estilo_detalle
            ),
            Paragraph(
                str(factura["Plazo"]),
                estilo_detalle
            ),
            Paragraph(
                formato_porcentaje(
                    factura["TEM"]*100,
                    2
                ),
                estilo_detalle
            ),
            Paragraph(
                formato_porcentaje(
                    factura["FactorAdelanto"]*100,
                    2
                ),
                estilo_detalle
            ),
            Paragraph(
                formato_moneda(
                    factura["ImporteAdelanto"]
                ),
                estilo_detalle
            ),
            Paragraph(
                formato_moneda(
                    factura["Interes"]
                ),
                estilo_detalle
            ),
            Paragraph(
                formato_moneda(
                    factura["IGV"]
                ),
                estilo_detalle
            ),
            Paragraph(
                formato_moneda(
                    factura["ImporteDesembolsar"]
                ),
                estilo_detalle
            ),
            Paragraph(
                formato_moneda(
                    factura["ImporteRemanente"]
                ),
                estilo_detalle
            ),
        ]

        filas_detalle.append(fila)

    # Distribución prácticamente sobre todo el ancho útil.
    #
    # Luego podemos ajustar columna por columna según las
    # primeras pruebas reales.

    proporciones = [
        0.025,   # #
        0.190,   # adquirente
        0.090,   # importe
        0.080,   # fecha
        0.045,   # plazo
        0.055,   # TEM
        0.050,   # factor
        0.095,   # adelanto
        0.080,   # interés
        0.065,   # IGV
        0.120,   # desembolso
        0.105,   # remanente
    ]

    anchos_detalle = [
        ancho_util * proporcion
        for proporcion in proporciones
    ]

    tabla_detalle = Table(
        filas_detalle,
        colWidths=anchos_detalle,
        repeatRows=1,
    )

    tabla_detalle.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                COLOR_PRINCIPAL
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
            (
                "BOX",
                (0, 0),
                (-1, -1),
                0.4,
                COLOR_BORDE
            ),
            (
                "INNERGRID",
                (0, 0),
                (-1, -1),
                0.25,
                COLOR_BORDE
            ),
            (
                "ROWBACKGROUNDS",
                (0, 1),
                (-1, -1),
                [
                    colors.white,
                    COLOR_FILA,
                ]
            ),
            (
                "ALIGN",
                (0, 1),
                (0, -1),
                "CENTER"
            ),
            (
                "ALIGN",
                (2, 1),
                (-1, -1),
                "RIGHT"
            ),
            (
                "ALIGN",
                (3, 1),
                (6, -1),
                "CENTER"
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                2
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                2
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                4
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                4
            ),
        ])
    )

    elementos.append(tabla_detalle)
    elementos.append(Spacer(1, 6))

    # =========================================================
    # TOTALES COMPLEMENTARIOS
    # =========================================================

    tabla_totales = Table(
        [
            [
                Paragraph(
                    "Interés total",
                    estilo_label
                ),
                Paragraph(
                    "IGV total",
                    estilo_label
                ),
                Paragraph(
                    "Remanente total",
                    estilo_label
                ),
            ],
            [
                Paragraph(
                    formato_moneda(interes_total),
                    estilo_valor
                ),
                Paragraph(
                    formato_moneda(igv_total),
                    estilo_valor
                ),
                Paragraph(
                    formato_moneda(remanente_total),
                    estilo_valor
                ),
            ],
        ],
        colWidths=[
            ancho_util / 3,
            ancho_util / 3,
            ancho_util / 3,
        ],
    )

    tabla_totales.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                COLOR_FILA
            ),
            (
                "BOX",
                (0, 0),
                (-1, -1),
                0.4,
                COLOR_BORDE
            ),
            (
                "INNERGRID",
                (0, 0),
                (-1, -1),
                0.25,
                COLOR_BORDE
            ),
            (
                "ALIGN",
                (0, 1),
                (-1, 1),
                "RIGHT"
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                6
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                6
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                5
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                5
            ),
        ])
    )

    elementos.append(tabla_totales)

    # =========================================================
    # OBSERVACIONES
    # =========================================================

    elementos.append(
        Paragraph(
            "Condiciones y observaciones",
            estilo_seccion
        )
    )

    if existe_adquirente_nuevo:

        mensaje_adquirente = (
            "<b>Adquirente nuevo.</b> "
            "Esta cotización incluye al menos un adquirente "
            "que aún no se encuentra incorporado. "
            "Será necesario realizar previamente su proceso "
            "de incorporación, el cual puede tomar hasta "
            "15 días. La atención de las facturas asociadas "
            "a dicho adquirente dependerá de la culminación "
            "de este proceso."
        )

        tabla_mensaje = Table(
            [[
                Paragraph(
                    mensaje_adquirente,
                    estilo_observacion
                )
            ]],
            colWidths=[ancho_util],
        )

        tabla_mensaje.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    COLOR_NUEVO
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    COLOR_NUEVO_BORDE
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
            ])
        )

        elementos.append(tabla_mensaje)
        elementos.append(Spacer(1, 5))

    if proveedor_nuevo:

        mensaje_proveedor = (
            "<b>Proveedor nuevo.</b> "
            "Para completar su incorporación deberá presentar "
            "la Copia Literal, Ficha RUC y Reporte Tributario "
            "de Terceros de la empresa; así como DNI y Vigencia "
            "de Poder de cada representante legal. "
            "Los documentos emitidos por SUNAT y SUNARP deben "
            "provenir de fuentes oficiales y estar firmados "
            "digitalmente. El DNI puede presentarse mediante "
            "una fotografía legible."
        )

        color_fondo = COLOR_NUEVO
        color_borde = COLOR_NUEVO_BORDE

    else:

        mensaje_proveedor = (
            "<b>Proveedor registrado.</b> "
            "Su empresa ya se encuentra incorporada, lo que "
            "permite continuar con la atención de la operación "
            "sin realizar un proceso adicional de registro."
        )

        color_fondo = COLOR_REGISTRADO
        color_borde = COLOR_REGISTRADO_BORDE

    tabla_proveedor_mensaje = Table(
        [[
            Paragraph(
                mensaje_proveedor,
                estilo_observacion
            )
        ]],
        colWidths=[ancho_util],
    )

    tabla_proveedor_mensaje.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, -1),
                color_fondo
            ),
            (
                "BOX",
                (0, 0),
                (-1, -1),
                0.5,
                color_borde
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                8
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                8
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                7
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                7
            ),
        ])
    )

    elementos.append(tabla_proveedor_mensaje)

    # =========================================================
    # PIE DE PÁGINA
    # =========================================================

    def dibujar_pie(canvas, doc):

        canvas.saveState()

        canvas.setStrokeColor(
            COLOR_BORDE
        )

        canvas.line(
            margen_izquierdo,
            0.90 * cm,
            ancho_pagina - margen_derecho,
            0.90 * cm,
        )

        canvas.setFont(
            "Helvetica",
            7.5
        )

        canvas.setFillColor(
            COLOR_TEXTO_SECUNDARIO
        )

        canvas.drawString(
            margen_izquierdo,
            0.55 * cm,
            "Cotización de factoring"
        )

        canvas.drawRightString(
            ancho_pagina - margen_derecho,
            0.55 * cm,
            f"Página {doc.page}"
        )

        canvas.restoreState()

    # =========================================================
    # GENERACIÓN
    # =========================================================

    documento.build(
        elementos,
        onFirstPage=dibujar_pie,
        onLaterPages=dibujar_pie,
    )

    return str(ruta_salida)