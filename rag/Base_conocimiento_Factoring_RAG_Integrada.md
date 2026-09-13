# Base de conocimiento RAG integrada - Factoring - Etapa 5

**Estado:** aprobada para uso del agente  
**Composición:** 36 tarjetas `legal_comercial` + 35 tarjetas `politica_producto` = 71 tarjetas.  
**Diseño recomendado:** un único corpus de recuperación para runtime, conservando la separación mediante `capa` e `id`. Los archivos de Etapa 3 y Etapa 4 se mantienen como fuentes maestras/auditoría.  
**Eficiencia:** no cargar este archivo completo en el prompt. Indexar/fragmentar por tarjeta y recuperar solo los bloques pertinentes (top-k pequeño). El consumo de tokens depende de los bloques recuperados, no del número físico de archivos.  

## Reglas de precedencia y uso

- Las herramientas/backend prevalecen para datos calculados, tasas, estados y validaciones dinámicas.
- `politica_producto` define elegibilidad, requisitos, costos, derivaciones y comportamiento del producto.
- `legal_comercial` explica el marco normativo y sus límites; no convertirlo en política interna no aprobada.
- Si ambas capas aplican, recuperar ambas y construir una sola respuesta coherente, sin llamar “ley” a una política interna.
- No completar vacíos con conocimiento externo.

---

# CAPA 1 - LEGAL_COMERCIAL

## C01 | Qué es factoring sin recurso
[capa=legal_comercial; nivel=Activo; prioridad=alta; exposicion=conversacion_habitual]
Conocimiento: El factoring consiste en que el Factor adquiere a título oneroso un crédito documentado y asume el riesgo crediticio del deudor. En el producto del agente, esta es la base del factoring sin recurso.
Cliente: “Compramos el derecho de cobro de tu factura o recibo por honorarios; el riesgo de que el pagador no cumpla por razones crediticias lo asume el factor.”
Límite: Aclarar que el proveedor conserva obligaciones sobre la existencia, exigibilidad, vigencia y correcta transferencia del crédito. No presentar el factoring como un préstamo.
Fuente: A1, A2, A8 | Ley 29623 arts. 1-2; Res. SBS 4358-2015 arts. 2 y 6-10.

---

## C02 | Factoring vs. descuento
[capa=legal_comercial; nivel=Activo; prioridad=alta; exposicion=conversacion_habitual]
Conocimiento: En factoring el Factor asume el riesgo crediticio del deudor. En descuento, el cliente mantiene ese riesgo y el descontante asume el riesgo crediticio del cliente.
Cliente: “Si la operación mantiene en ti el riesgo de que tu cliente no pague, estamos ante una lógica de descuento, no ante el factoring que ofrecemos.”
Límite: Usar para responder “¿es con recurso?” o “¿qué diferencia hay con descuento?”. No usar ambos términos como sinónimos jurídicos.
Fuente: A3 | Res. SBS 4358-2015 art. 11.

---

## C03 | Qué documentos pueden financiarse
[capa=legal_comercial; nivel=Activo; prioridad=alta; exposicion=conversacion_habitual]
Conocimiento: El factoring puede recaer sobre instrumentos de contenido crediticio de libre disposición, incluidas Facturas Negociables. El producto aprobado incluye facturas electrónicas y recibos por honorarios electrónicos que cumplan las condiciones aplicables.
Cliente: “Podemos evaluar facturas electrónicas y recibos por honorarios electrónicos siempre que el crédito sea válido, transferible y cumpla los requisitos aplicables.”
Límite: No prometer aceptación automática. La norma excluye instrumentos vencidos y otros supuestos específicos del Reglamento SBS.
Fuente: A4, B4 | Res. SBS 4358-2015 art. 3; Ley 29623 art. 3-A.

---

## C04 | Factura Negociable y libre transferencia
[capa=legal_comercial; nivel=Activo; prioridad=alta; exposicion=conversacion_habitual]
Conocimiento: La Factura Negociable incorpora el derecho de crédito y puede transferirse por endoso o mediante anotación en cuenta, según su representación. Los acuerdos que restrinjan o prohíban su transferencia son nulos.
Cliente: “La Factura Negociable está diseñada para poder transferirse; una cláusula que simplemente prohíba su transferencia no elimina ese derecho.”
Límite: No convertir esta regla en una opinión sobre cualquier cláusula contractual concreta sin revisar el caso.
Fuente: B1, D8 | Ley 29623 art. 2; Ley 27287 art. 2; D.S. 208-2015-EF art. 9.

---

## C05 | Contrato de factoring
[capa=legal_comercial; nivel=Activo; prioridad=alta; exposicion=conversacion_habitual]
Conocimiento: La operación se perfecciona mediante contrato escrito entre Factor y Cliente, con identificación de partes e instrumentos, precio/forma de pago, retribución cuando corresponda, responsable de cobranza y momento de asunción del riesgo del deudor.
Cliente: “La operación se formaliza mediante un contrato de factoring que identifica el crédito que se transfiere y las condiciones económicas y operativas.”
Límite: No inventar cláusulas, comisiones ni condiciones del contrato; esas serán políticas/documentos propios del producto.
Fuente: A7 | Res. SBS 4358-2015 art. 4.

---

## C06 | Obligaciones básicas del proveedor
[capa=legal_comercial; nivel=Activo; prioridad=alta; exposicion=conversacion_habitual]
Conocimiento: El proveedor debe transferir válidamente el instrumento, entregar información y documentación y garantizar, entre otros aspectos, la existencia, exigibilidad y vigencia del crédito.
Cliente: “Que el factoring sea sin recurso por riesgo crediticio no elimina tu responsabilidad sobre que el crédito exista, sea exigible y esté correctamente documentado.”
Límite: Esta precisión evita afirmar que “el proveedor nunca responde por nada” en un factoring sin recurso.
Fuente: A8 | Res. SBS 4358-2015 arts. 6-10.

---

## C07 | Factura Negociable física
[capa=legal_comercial; nivel=Secundario; prioridad=media; exposicion=solo_si_consultan]
Conocimiento: Existe un régimen para Factura Negociable originada en comprobantes impresos/importados, con tercera copia, requisitos propios y constancia de presentación.
Cliente: “También existe un régimen para documentos físicos, pero nuestro flujo comercial se concentra en comprobantes electrónicos.”
Límite: Conocimiento de reconocimiento y comparación. No incorporarlo al flujo normal de cotización del agente.
Fuente: B2, B3, C1 | Ley 29623 arts. 2, 3 y 7; D.S. 208-2015-EF; R.S. 211-2015/SUNAT.

---

## C08 | Información del CPE al crédito
[capa=legal_comercial; nivel=Activo; prioridad=alta; exposicion=conversacion_habitual]
Conocimiento: La factura electrónica o RHE al crédito debe contener la información adicional exigida por el régimen aplicable, incluyendo plazo/fechas de pago y monto neto pendiente; si hay cuotas, se identifica la información de cada cuota.
Cliente: “Para financiar el comprobante necesitamos que la información de pago esté correctamente registrada: monto pendiente y fecha o fechas de pago.”
Límite: No asumir que cualquier error puede corregirse de cualquier forma; la subsanación depende del régimen SUNAT aplicable.
Fuente: B4, B5 | Ley 29623 art. 3-A; DU 013-2020 art. 6.1; D.S. 239-2021-EF art. 5.

---

## C09 | Conformidad electrónica: plazo general
[capa=legal_comercial; nivel=Activo; prioridad=alta; exposicion=conversacion_habitual]
Conocimiento: En factura electrónica/RHE electrónico al crédito, el adquirente o usuario dispone de ocho días calendario desde la puesta a disposición para registrar conformidad o disconformidad.
Cliente: “Tu cliente tiene ocho días calendario, contados desde la puesta a disposición en SUNAT, para manifestar conformidad o disconformidad.”
Límite: No contar el plazo desde la emisión por defecto. El punto de partida aprobado es la puesta a disposición en SUNAT.
Fuente: C2, C4 | DU 013-2020 arts. 6-7; D.S. 239-2021-EF art. 6; R.S. 165-2021/SUNAT arts. 3-4.

---

## C10 | Extensión por actuación en el último día
[capa=legal_comercial; nivel=Activo; prioridad=alta; exposicion=conversacion_habitual]
Conocimiento: El régimen electrónico contempla una extensión de hasta dos días calendario cuando la disconformidad o su atención/subsanación ocurre en el último día, en los supuestos previstos.
Cliente: “Si la observación o su subsanación ocurre justo el último día, la norma contempla una extensión específica; hay que revisar el caso antes de dar por cerrada la conformidad.”
Límite: No resumir esta regla como “siempre hay diez días”. La extensión es excepcional y depende del supuesto regulado.
Fuente: C3 | DU 013-2020 art. 7; R.S. 165-2021/SUNAT art. 4.1.

---

## C11 | Qué puede observar el adquirente
[capa=legal_comercial; nivel=Activo; prioridad=alta; exposicion=conversacion_habitual]
Conocimiento: La disconformidad electrónica puede referirse al plazo de pago, monto neto pendiente o reclamos sobre los bienes o servicios, conforme al DU 013-2020.
Cliente: “El pagador puede observar, entre otros puntos, el plazo, el monto pendiente o aspectos vinculados con los bienes o servicios.”
Límite: No calificar como válida o inválida una observación concreta sin revisar su sustento y el procedimiento aplicado.
Fuente: C5 | DU 013-2020 arts. 7-8.

---

## C12 | Subsanación de disconformidad
[capa=legal_comercial; nivel=Activo; prioridad=alta; exposicion=conversacion_habitual]
Conocimiento: La plataforma SUNAT permite registrar la atención o subsanación de la disconformidad y, cuando corresponde, utilizar notas electrónicas o emitir un nuevo comprobante según el procedimiento.
Cliente: “Si existe una observación, primero debe regularizarse por el mecanismo que corresponda en SUNAT antes de tratar la operación como conforme.”
Límite: No indicar automáticamente qué nota debe emitirse; dependerá del tipo de discrepancia y del procedimiento aplicable.
Fuente: C6 | DU 013-2020 art. 7; R.S. 165-2021/SUNAT art. 5.

---

## C13 | Conformidad presunta
[capa=legal_comercial; nivel=Activo; prioridad=alta; exposicion=conversacion_habitual]
Conocimiento: Si vence el plazo legal sin disconformidad, opera la conformidad presunta e irrevocable en los términos de la ley.
Cliente: “Si transcurre el plazo sin que el adquirente registre disconformidad, la norma prevé la conformidad presunta.”
Límite: Verificar que el cómputo y el régimen sean los correctos antes de afirmar que ya existe conformidad presunta.
Fuente: C7 | Ley 29623 art. 7; DU 013-2020 art. 7; CAVALI Cap. XVII.

---

## C14 | Reclamos posteriores a la conformidad
[capa=legal_comercial; nivel=Activo; prioridad=alta; exposicion=conversacion_habitual]
Conocimiento: Producida la conformidad expresa o presunta, reclamos posteriores por vicios ocultos o defectos se dirigen contra quien corresponda y no habilitan, en los términos legales, a retener frente al legítimo tenedor el monto pendiente.
Cliente: “Después de la conformidad, un reclamo posterior no convierte automáticamente en impagable la Factura Negociable frente a su legítimo tenedor.”
Límite: Evitar prometer que ningún reclamo posterior tendrá efecto alguno; la regla debe explicarse en los términos y condiciones legales.
Fuente: C8 | Ley 29623 art. 7; DU 013-2020 art. 7.

---

## C15 | SUNAT y CAVALI en la conformidad actual
[capa=legal_comercial; nivel=Activo; prioridad=alta; exposicion=conversacion_habitual]
Conocimiento: Para CPE al crédito del régimen vigente, la conformidad/disconformidad se manifiesta por los medios SUNAT y CAVALI obtiene esa información mediante interconexión para sus efectos registrales.
Cliente: “La conformidad se gestiona en SUNAT; CAVALI recibe esa información para el registro de la Factura Negociable.”
Límite: No usar el antiguo esquema de ocho días hábiles desde una comunicación de CAVALI para CPE sujetos al régimen actual.
Fuente: C9, H3, H4 | CAVALI Cap. XVII DV 01; DU 013-2020; D.S. 239-2021-EF; R.S. 165-2021/SUNAT.

---

## C16 | Anotación en cuenta y registro en CAVALI
[capa=legal_comercial; nivel=Activo; prioridad=alta; exposicion=conversacion_habitual]
Conocimiento: La Factura Negociable electrónica se representa mediante anotación en cuenta en una ICLV. CAVALI presta el servicio de registro centralizado de estas Facturas Negociables.
Cliente: “Para negociar electrónicamente la Factura Negociable, esta se registra por anotación en cuenta en CAVALI.”
Límite: No afirmar que el simple CPE, sin el registro que corresponda, ya fue transferido al factor.
Fuente: D1, D2 | Ley 27287 art. 2; Ley 29623 arts. 2 y 8; CAVALI Cap. XVII.

---

## C17 | Validaciones antes/durante el registro
[capa=legal_comercial; nivel=Activo; prioridad=alta; exposicion=conversacion_habitual]
Conocimiento: SUNAT/CAVALI contemplan verificaciones de validez del comprobante y controles de registro antes o durante la anotación en cuenta.
Cliente: “El registro no es solo cargar un archivo: existen validaciones sobre el comprobante y la información que sustenta la Factura Negociable.”
Límite: No prometer que una factura será registrable hasta que las validaciones correspondientes hayan sido superadas.
Fuente: D3 | D.S. 208-2015-EF arts. 7-8; R.S. 211-2015/SUNAT arts. 2-3; CAVALI Cap. XVII.

---

## C18 | Cuándo puede transferirse una FN electrónica
[capa=legal_comercial; nivel=Activo; prioridad=alta; exposicion=conversacion_habitual]
Conocimiento: La Factura Negociable originada en CPE puede transferirse desde que está registrada ante una ICLV; la transferencia contable se efectúa al registro del comprador/titular.
Cliente: “Una vez registrada en CAVALI, la Factura Negociable electrónica puede ser transferida al nuevo titular.”
Límite: Distinguir registro, transferencia y desembolso: son hitos diferentes y no deben presentarse como simultáneos por definición.
Fuente: D4, D5 | Ley 29623 art. 8; D.S. 208-2015-EF art. 15; CAVALI DV 03.

---

## C19 | Comunicación de la transferencia
[capa=legal_comercial; nivel=Activo; prioridad=alta; exposicion=conversacion_habitual]
Conocimiento: Tras la transferencia debe comunicarse oportunamente al adquirente, de forma fehaciente, la identidad del nuevo legítimo tenedor y la información necesaria para el pago. CAVALI puede efectuar la comunicación electrónica cuando corresponda a su aplicativo.
Cliente: “Después de la cesión, el pagador debe quedar informado de quién es el nuevo titular y cómo debe efectuar el pago.”
Límite: No afirmar que toda comunicación la hará siempre CAVALI; depende del mecanismo aplicable y del registro del adquirente.
Fuente: D5, D6 | Ley 29623 art. 8; D.S. 208-2015-EF art. 15.3; CAVALI DV 03.

---

## C20 | A quién debe pagar el adquirente
[capa=legal_comercial; nivel=Activo; prioridad=alta; exposicion=conversacion_habitual]
Conocimiento: El adquirente debe pagar la Factura Negociable al legítimo tenedor conforme a la notificación recibida, salvo instrucción válida diferente comunicada antes del pago.
Cliente: “Una vez notificada la transferencia, el pago debe dirigirse al legítimo tenedor informado.”
Límite: No dar instrucciones de cuenta o beneficiario que no provengan del sistema/proceso autorizado.
Fuente: D7 | Ley 29623 art. 8.

---

## C21 | Inicio del plazo de pago
[capa=legal_comercial; nivel=Activo; prioridad=alta; exposicion=conversacion_habitual]
Conocimiento: En el régimen electrónico del DU 013-2020, el plazo acordado de pago se inicia el día calendario siguiente al vencimiento del plazo de ocho días de conformidad/disconformidad.
Cliente: “Para este régimen, el plazo pactado de pago empieza después de finalizar el período legal de conformidad.”
Límite: No confundir fecha de emisión, puesta a disposición, conformidad y fecha de inicio del plazo de pago.
Fuente: E1 | DU 013-2020 art. 5; D.S. 239-2021-EF art. 4.1.a.

---

## C22 | Plazo superior a 30 días
[capa=legal_comercial; nivel=Activo; prioridad=alta; exposicion=conversacion_habitual]
Conocimiento: Proveedor y adquirente pueden pactar excepcionalmente un plazo superior a treinta días calendario si el acuerdo consta en escritura pública o documento con firmas legalizadas notarialmente y contiene la información mínima exigida.
Cliente: “Un plazo mayor a 30 días puede pactarse excepcionalmente, pero debe existir el acuerdo formal exigido por el reglamento.”
Límite: No concluir, solo por ausencia de ese acuerdo, que la Factura Negociable es automáticamente inválida o intransferible; la Etapa 2 no estableció esa consecuencia.
Fuente: E8 | D.S. 120-2022-EF, Reglamento de la Ley 31362, art. 5.

---

## C23 | Cuotas, vencimiento y prórroga
[capa=legal_comercial; nivel=Secundario; prioridad=media; exposicion=solo_si_consultan]
Conocimiento: La Factura Negociable puede contemplar una o varias fechas de pago. Las prórrogas, pagos parciales y reprogramaciones deben reflejarse conforme a la ley y al registro aplicable.
Cliente: “Si el pago es por cuotas o se reprograma, la información debe quedar correctamente reflejada en el título/registro.”
Límite: Antes de explicar una reprogramación concreta, verificar que haya sido previamente acordada con el adquirente y registrada conforme al procedimiento.
Fuente: E2, E6 | Ley 29623 art. 4; Ley 27287 art. 49; D.S. 208-2015-EF; CAVALI DV 04.

---

## C24 | Intereses de la Factura Negociable
[capa=legal_comercial; nivel=Secundario; prioridad=media; exposicion=solo_si_consultan]
Conocimiento: La ley permite pactar interés compensatorio hasta el vencimiento y regula intereses compensatorios y moratorios sobre el importe impago en los términos legales.
Cliente: “La Factura Negociable puede contemplar intereses y, ante incumplimiento, aplican las reglas de intereses pactados o legales que correspondan.”
Límite: No informar tasas específicas si no provienen del contrato, herramienta o política aprobada del producto.
Fuente: E3 | Ley 29623 art. 5; Ley 27287 art. 51.

---

## C25 | Pago recibido por el proveedor después de transferir
[capa=legal_comercial; nivel=Activo; prioridad=alta; exposicion=conversacion_habitual]
Conocimiento: Si el proveedor recibe un pago del adquirente después de transferida la Factura Negociable, debe entregarlo al legítimo tenedor conforme al régimen aplicable.
Cliente: “Si tu cliente te paga por error después de que transferiste la factura, ese dinero corresponde al legítimo tenedor y debe ser entregado.”
Límite: No presentar ese pago equivocado como una cancelación automática de obligaciones frente al legítimo tenedor.
Fuente: E4 | Res. SBS 4358-2015 art. 10.4; D.S. 208-2015-EF art. 15.4.

---

## C26 | Registro del pago y redención
[capa=legal_comercial; nivel=Secundario; prioridad=media; exposicion=solo_si_consultan]
Conocimiento: CAVALI contempla el registro de la fecha efectiva de pago y la redención del valor; en pagos por cuotas, la redención concluye con la última cuota pendiente. El DU 013-2020 contempla además registro de fecha efectiva de pago en la Plataforma de Pago Oportuno cuando corresponda.
Cliente: “El pago efectivo también debe quedar registrado para cerrar correctamente la Factura Negociable.”
Límite: Materia principalmente operativa; no cargar al cliente con el detalle registral salvo que pregunte o exista una incidencia.
Fuente: E5, E7 | CAVALI DV 04; DU 013-2020 arts. 6.2 y 9; D.S. 239-2021-EF art. 12.

---

## C27 | Mérito ejecutivo y cobranza
[capa=legal_comercial; nivel=Activo; prioridad=alta; exposicion=conversacion_habitual]
Conocimiento: La Factura Negociable que cumple los requisitos aplicables tiene mérito ejecutivo. Para valores anotados en cuenta, la constancia de inscripción y titularidad emitida por la ICLV sustenta la acción ejecutiva y no requiere protesto en los términos legales.
Cliente: “La Factura Negociable registrada y con los requisitos correspondientes puede servir como título para exigir judicialmente el pago si el obligado incumple.”
Límite: No prometer resultado, plazo ni recuperabilidad de una cobranza judicial. El mérito ejecutivo no equivale a garantía de cobro.
Fuente: F1, F2, F3 | Ley 27287 art. 18; Ley 29623 art. 6; CAVALI Cap. XVII.

---

## C28 | Protesto / sin protesto
[capa=legal_comercial; nivel=Secundario; prioridad=media; exposicion=solo_si_consultan]
Conocimiento: La Ley de Títulos Valores admite cláusula sin protesto, pero la Factura Negociable tiene reglas especiales; la FN anotada en cuenta se ejecuta sobre la constancia de la ICLV sin requerir protesto.
Cliente: “En la Factura Negociable electrónica anotada en cuenta, la constancia de la ICLV cumple la función ejecutiva prevista por la ley.”
Límite: No generalizar la exoneración de protesto a todos los títulos o a todos los supuestos físicos.
Fuente: F4 | Ley 27287 art. 52; Ley 29623 art. 6.

---

## C29 | Impugnación o retención dolosa
[capa=legal_comercial; nivel=Secundario; prioridad=media; exposicion=solo_si_consultan]
Conocimiento: La Ley 29623 tipifica como infracción administrativa la impugnación dolosa o retención indebida de la Factura Negociable y contempla derechos del proveedor o legítimo tenedor perjudicado.
Cliente: “La normativa protege la circulación de la Factura Negociable frente a actuaciones dolosas que busquen bloquearla indebidamente.”
Límite: No acusar al adquirente de conducta dolosa en una conversación comercial; una calificación de ese tipo requiere análisis del caso.
Fuente: F5 | Ley 29623 art. 9; D.S. 208-2015-EF.

---

## C30 | Riesgo crediticio, límites y LA/FT
[capa=legal_comercial; nivel=Interno; prioridad=interna; exposicion=soporte_interno]
Conocimiento: Para entidades comprendidas en la Ley 26702, el factoring está sujeto a gestión del riesgo del deudor, provisiones, límites prudenciales y controles de prevención LA/FT. Estas materias sustentan evaluación y controles internos.
Cliente: Al cliente solo se comunica la consecuencia necesaria: “la operación está sujeta a evaluación y controles regulatorios/internos”.
Límite: No explicar provisiones, límites o criterios internos salvo que exista una política aprobada para comunicarlos. Las futuras reglas propias del producto deben identificarse como política interna.
Fuente: G1, G2, G3 | Res. SBS 4358-2015 arts. 17, 20, 22-24; Ley 29623 art. 10.

---

## C31 | Adquirente y solvencia del comprador de la FN
[capa=legal_comercial; nivel=Secundario; prioridad=media; exposicion=solo_si_consultan]
Conocimiento: El adquirente de bienes o usuario de servicios no es responsable por la idoneidad o solvencia de quien compra la Factura Negociable, en los términos de la Ley 29623.
Cliente: “Al pagador no le corresponde garantizar la solvencia de la empresa que adquiere la Factura Negociable.”
Límite: Usar solo cuando la consulta trate sobre responsabilidad del adquirente respecto del factor/comprador.
Fuente: G4 | Ley 29623 art. 10.

---

## C32 | Perímetro institucional del oferente
[capa=legal_comercial; nivel=Interno; prioridad=interna; exposicion=soporte_interno]
Conocimiento: La base comercial asume que el producto es ofrecido por una entidad comprendida en la Ley 26702. El régimen de empresas de factoring fuera de la Ley General se conserva solo como contexto.
Cliente: No es necesario explicar al cliente el régimen registral de otras empresas de factoring salvo que pregunte por diferencias institucionales.
Límite: No mezclar las obligaciones de empresas registradas fuera de la Ley 26702 con las reglas operativas del producto del agente.
Fuente: A5, A6, G5 | Ley 26702 art. 282.8; Ley 30308 art. 2; Res. SBS 4358-2015 Cap. VI.

---

## C33 | Servicios adicionales del Factor
[capa=legal_comercial; nivel=Secundario; prioridad=media; exposicion=solo_si_consultan]
Conocimiento: El Reglamento SBS permite al Factor prestar servicios adicionales, como información comercial, gestión/cobranza, servicios contables, estudios de mercado y asesoría, entre otros similares.
Cliente: “La regulación permite que una empresa de factoring brinde servicios adicionales, aunque los que efectivamente ofrecemos dependen de nuestro producto.”
Límite: No prometer ningún servicio adicional que no haya sido definido expresamente por la empresa.
Fuente: A9 | Res. SBS 4358-2015 art. 8.

---

## C34 | Reglas del comprobante de pago subyacente
[capa=legal_comercial; nivel=Secundario; prioridad=media; exposicion=solo_si_consultan]
Conocimiento: El Reglamento de Comprobantes de Pago define cuándo corresponde emitir factura y la oportunidad de emisión/otorgamiento. Esas reglas complementan, pero no sustituyen, el régimen especial de Factura Negociable.
Cliente: “Primero debe existir un comprobante válido; sobre esa base operan las reglas específicas de la Factura Negociable.”
Límite: No resolver consultas tributarias generales fuera del alcance del factoring con estas reglas parciales.
Fuente: B6 | R.S. 007-99/SUNAT arts. 4-5.

---

## C35 | Normas históricas y prioridad del régimen actual
[capa=legal_comercial; nivel=Control; prioridad=control; exposicion=control_de_interpretacion]
Conocimiento: El D.S. 047-2011-EF está derogado. Las reglas antiguas de ocho días hábiles no deben mezclarse con el régimen actual de CPE al crédito, que usa ocho días calendario desde la puesta a disposición SUNAT. Los textos consolidados suministrados prevalecen para este trabajo.
Cliente: No es contenido para exposición normal al cliente. Sirve para evitar respuestas basadas en versiones normativas antiguas.
Límite: Si aparece una contradicción entre un pasaje heredado y el flujo actual aprobado, usar el régimen DU 013-2020 + D.S. 239-2021-EF + R.S. 165-2021/SUNAT para CPE al crédito.
Fuente: H1-H5 | D.S. 208-2015-EF; DU 013-2020; D.S. 239-2021-EF; R.S. 165-2021/SUNAT; CAVALI v10.

---

## C36 | Nota de crédito y monto sujeto a conformidad
[capa=legal_comercial; nivel=Activo; prioridad=alta; exposicion=conversacion_habitual]
Conocimiento: El registro de la conformidad corresponde al comprobante electrónico corregido o modificado por las notas de crédito electrónicas que estén registradas en la Plataforma SUNAT a la fecha de la conformidad. Si una nota de crédito corrige o modifica el monto neto pendiente de pago, la conformidad recae sobre el comprobante modificado y ese monto neto pendiente es el dato relevante del crédito.
Cliente: “Si una factura de S/ 10,000 tiene una nota de crédito de S/ 1,000 que reduce el monto pendiente y está registrada antes de la conformidad, la conformidad corresponde al comprobante modificado: el monto neto pendiente será S/ 9,000.”
Límite: No confundir el monto neto pendiente sujeto a conformidad con el “importe a financiar”. SUNAT gestiona la conformidad del monto neto pendiente; el importe efectivamente financiado dependerá de las condiciones del producto. Verificar que la N/C esté registrada antes de la conformidad y que efectivamente modifique ese monto.
Fuente: B5, C5, C6 | DU 013-2020 arts. 6 y 8; R.S. 165-2021/SUNAT arts. 4.3 y 5.1.

---

# CAPA 2 - POLITICA_PRODUCTO

## P01 | Instrumentos financiables
[capa=politica_producto; categoria=Elegibilidad; tipo=politica; prioridad=alta; estado=Confirmada]
Regla: El producto evalúa Facturas Negociables originadas en facturas electrónicas y recibos por honorarios electrónicos.
Disparador: Cuando el cliente consulta qué documentos puede financiar.
Acción: Informar el alcance y continuar solo si el documento pertenece al alcance aprobado.
Cliente/Límite: “Evaluamos facturas electrónicas y recibos por honorarios electrónicos que cumplan las condiciones del producto y del régimen aplicable.”
Fuente interna: Características del producto; Etapa 3 C03/C07.

---

## P02 | Moneda
[capa=politica_producto; categoria=Elegibilidad; tipo=elegibilidad_exclusion; prioridad=alta; estado=Confirmada]
Regla: Solo se financian operaciones en moneda nacional.
Disparador: Al recibir los datos de la factura/RHE.
Acción: Si la moneda no es PEN, no continuar con la cotización estándar.
Cliente/Límite: Comunicar que el producto opera únicamente en soles.
Fuente interna: Características del producto, punto 3.c.

---

## P03 | Plazo mínimo
[capa=politica_producto; categoria=Elegibilidad; tipo=elegibilidad_exclusion; prioridad=alta; estado=Confirmada]
Regla: El plazo mínimo de financiamiento es 15 días.
Disparador: Al calcular el plazo desde la fecha de desembolso hasta la fecha de pago.
Acción: Si el plazo es menor a 15 días, no cotizar bajo el producto estándar.
Cliente/Límite: Explicar que el producto requiere un plazo mínimo de 15 días.
Fuente interna: Características del producto, puntos 3.a y 7.

---

## P04 | Importe mínimo
[capa=politica_producto; categoria=Elegibilidad; tipo=elegibilidad_exclusion; prioridad=alta; estado=Confirmada]
Regla: El importe mínimo a financiar por factura es S/ 100.
Disparador: Al evaluar el importe de la operación por factura.
Acción: Si el importe a financiar es menor a S/ 100, no continuar con la cotización estándar.
Cliente/Límite: Informar el mínimo de S/ 100 por factura.
Fuente interna: Características del producto, puntos 3.b y 6.

---

## P05 | Adquirente en CAVALI
[capa=politica_producto; categoria=Elegibilidad; tipo=elegibilidad_exclusion; prioridad=critica; estado=Confirmada]
Regla: El adquirente debe estar inscrito como participante de CAVALI. Si no está inscrito, la operación queda excluida del factoring. No se define un flujo alternativo para regularización dentro del agente.
Disparador: Al evaluar la elegibilidad del adquirente.
Acción: Verificar la condición cuando el dato esté disponible. Si no está inscrito, excluir la operación y no continuar con la cotización.
Cliente/Límite: Comunicar que el producto solo admite adquirentes inscritos como participantes de CAVALI; no ofrecer un flujo alternativo.
Fuente interna: Características del producto, punto 2.a; decisión expresa del usuario; Etapa 3 C15-C19.

---

## P06 | Empresas vinculadas
[capa=politica_producto; categoria=Riesgo; tipo=elegibilidad_exclusion; prioridad=critica; estado=Confirmada / declarativa]
Regla: No se aceptan operaciones de factoring entre proveedor y adquirente vinculados. Basta que se cumpla uno de estos tres criterios: (1) propiedad o participación directa o indirecta en el capital; (2) misma dirección; o (3) coincidencia en el equipo de alta gerencia, como gerentes o directores.
Disparador: Cuando se conozca información de proveedor y adquirente suficiente para advertir cualquiera de los tres criterios.
Acción: Si se cumple al menos uno de los criterios, excluir la operación. Por ahora la regla se declara al agente; no se define una herramienta automática adicional de vinculación.
Cliente/Límite: Comunicar que el producto no admite operaciones entre empresas vinculadas. No exponer criterios internos salvo que sea necesario explicar la exclusión.
Fuente interna: Características del producto, punto 14; aclaración expresa del usuario.

---

## P34 | Aprobación humana por plazo
[capa=politica_producto; categoria=Riesgo; tipo=derivacion_humana; prioridad=critica; estado=Confirmada]
Regla: Si el plazo de la factura es mayor a 100 días, se requiere aprobación humana para cotizar.
Disparador: Plazo calculado > 100 días.
Acción: No emitir cotización automática. Indicar al cliente que debe comunicarse por canal telefónico con un ejecutivo comercial.
Cliente/Límite: “Por el plazo de esta factura, la cotización requiere revisión de un ejecutivo comercial. Por favor comunícate por el canal telefónico.”
Fuente interna: Características del producto, punto 16.

---

## P35 | Aprobación humana por VNPP
[capa=politica_producto; categoria=Riesgo; tipo=derivacion_humana; prioridad=critica; estado=Confirmada]
Regla: Si el VNPP de una factura supera S/ 200,000, se requiere aprobación humana para cotizar.
Disparador: VNPP > S/ 200,000.
Acción: No emitir cotización automática. Indicar al cliente que debe comunicarse por canal telefónico con un ejecutivo comercial.
Cliente/Límite: “Por el importe de esta factura, la cotización requiere revisión de un ejecutivo comercial. Por favor comunícate por el canal telefónico.”
Fuente interna: Características del producto, punto 17.

---

## P07 | Documentos de empresa
[capa=politica_producto; categoria=Documentación; tipo=requisito_documental; prioridad=media; estado=Confirmada]
Regla: Para el alta del proveedor se solicitan Copia Literal, Ficha RUC, Reporte Tributario de Terceros y carta simple con referencias bancarias (banco, tipo de cuenta, moneda y número de cuenta).
Disparador: Proveedor nuevo o actualización documental.
Acción: Solicitar los documentos faltantes antes de completar el alta.
Cliente/Límite: Explicar qué documentos son necesarios para el registro.
Fuente interna: Características del producto, punto 1.a.

---

## P08 | Documentos del representante
[capa=politica_producto; categoria=Documentación; tipo=requisito_documental; prioridad=media; estado=Confirmada]
Regla: El/los representante(s) que firman contrato/adendas presentan DNI vigente, vigencia de poder y constancia de no tener multas electorales pendientes.
Disparador: Alta del proveedor y cuando corresponda actualizar representación.
Acción: Solicitar y verificar existencia de la documentación requerida.
Cliente/Límite: Comunicar el checklist documental del representante.
Fuente interna: Características del producto, punto 1.b.

---

## P09 | Antigüedad documental
[capa=politica_producto; categoria=Documentación; tipo=requisito_documental; prioridad=media; estado=Confirmada]
Regla: Los documentos presentados por el proveedor deben tener una antigüedad de emisión máxima de 45 días.
Disparador: Al revisar documentación presentada.
Acción: Si excede 45 días, solicitar documento actualizado.
Cliente/Límite: Indicar que los documentos deben ser recientes, con máximo 45 días de emisión.
Fuente interna: Características del producto, punto 5.

---

## P10 | Actualización anual
[capa=politica_producto; categoria=Documentación; tipo=requisito_documental; prioridad=media; estado=Confirmada]
Regla: Los documentos del proveedor deben actualizarse cada año.
Disparador: Proveedor ya registrado.
Acción: Solicitar actualización cuando corresponda por ciclo anual.
Cliente/Límite: Informar que la documentación se actualiza anualmente.
Fuente interna: Características del producto, punto 15.

---

## P11 | Datos de contacto
[capa=politica_producto; categoria=Documentación; tipo=requisito_documental; prioridad=media; estado=Confirmada]
Regla: Los representantes legales deben indicar celular y correo electrónico, que serán validados por la empresa.
Disparador: Alta o actualización del representante.
Acción: Capturar datos y someterlos al mecanismo de validación definido por la empresa.
Cliente/Límite: Explicar que celular y correo serán validados.
Fuente interna: Características del producto, punto 9.

---

## P12 | Archivos del comprobante
[capa=politica_producto; categoria=Documentación; tipo=requisito_documental; prioridad=media; estado=Confirmada]
Regla: Para la Factura Negociable/RHE se presentan XML, PDF y CDR.
Disparador: Al ingresar una factura/RHE para evaluación.
Acción: Solicitar los tres archivos antes de completar la evaluación documental.
Cliente/Límite: Indicar que se requiere XML, PDF y CDR.
Fuente interna: Características del producto, punto 3.d.

---

## P13 | Embargos SUNAT
[capa=politica_producto; categoria=Control; tipo=control; prioridad=alta; estado=Confirmada]
Regla: En cada operación el proveedor presenta constancia de no tener multas en SUNAT con orden de embargo.
Disparador: Antes de formalizar cada operación.
Acción: Solicitar/validar la constancia; si no está disponible, no asumir cumplimiento.
Cliente/Límite: Comunicar que es un requisito por operación.
Fuente interna: Características del producto, punto 4.c.

---

## P14 | Multas electorales por operación
[capa=politica_producto; categoria=Control; tipo=control; prioridad=alta; estado=Confirmada]
Regla: El representante legal presenta constancia de no tener multas electorales cuando sea requerido.
Disparador: Cada operación, solo cuando el proceso lo solicite.
Acción: Pedir la constancia cuando el sistema/procedimiento marque el requisito.
Cliente/Límite: No presentarlo como requisito obligatorio en todas las operaciones; indicar “cuando corresponda”.
Fuente interna: Características del producto, punto 4.b.

---

## P15 | Contrato marco
[capa=politica_producto; categoria=Contratación; tipo=formalizacion; prioridad=media; estado=Confirmada]
Regla: El proveedor debe firmar un contrato marco de factoring.
Disparador: Alta/contratación inicial.
Acción: No tratar al proveedor como contratado hasta que el contrato marco esté formalizado.
Cliente/Límite: Explicar que el contrato marco habilita la relación contractual para futuras operaciones.
Fuente interna: Características del producto, punto 1.c; Etapa 3 C05.

---

## P16 | Vigencia del contrato marco
[capa=politica_producto; categoria=Contratación; tipo=formalizacion; prioridad=media; estado=Confirmada]
Regla: La vigencia del contrato marco es de 3 años.
Disparador: Al revisar si el proveedor mantiene contrato vigente.
Acción: Si está vencido, requerir renovación antes de nuevas operaciones.
Cliente/Límite: Informar vigencia de tres años cuando sea relevante.
Fuente interna: Características del producto, punto 8.

---

## P17 | Adenda por operación
[capa=politica_producto; categoria=Contratación; tipo=formalizacion; prioridad=media; estado=Confirmada]
Regla: Cada operación de factoring requiere adenda al contrato marco.
Disparador: Cada nueva operación.
Acción: Generar/requerir firma de la adenda antes de perfeccionar la operación.
Cliente/Límite: Explicar que cada operación se documenta mediante una adenda.
Fuente interna: Características del producto, punto 4.a.

---

## P18 | Agrupación de facturas en adenda
[capa=politica_producto; categoria=Contratación; tipo=formalizacion; prioridad=media; estado=Confirmada]
Regla: Una adenda puede contener una o varias facturas del mismo proveedor y adquirente.
Disparador: Cuando se cotizan varias facturas.
Acción: Agrupar únicamente facturas que compartan proveedor y adquirente.
Cliente/Límite: Explicar que pueden consolidarse varias facturas del mismo proveedor/adquirente en una adenda.
Fuente interna: Características del producto, sección Otras características.

---

## P19 | Firma electrónica
[capa=politica_producto; categoria=Firma; tipo=formalizacion; prioridad=media; estado=Confirmada]
Regla: Contrato marco y adendas se firman electrónicamente bajo el paraguas de un certificado digital del factor.
Disparador: Formalización contractual.
Acción: Usar el mecanismo de firma electrónica aprobado; no proponer mecanismos alternativos no autorizados.
Cliente/Límite: Indicar que la contratación se realiza electrónicamente.
Fuente interna: Características del producto, punto 10.

---

## P20 | Datos de la factura
[capa=politica_producto; categoria=Datos; tipo=calculo_comercial; prioridad=media; estado=Confirmada]
Regla: Los datos mínimos de la factura para el cálculo son VNPP y fecha de pago.
Disparador: Al iniciar cálculo/cotización.
Acción: Solicitar ambos datos si no están disponibles.
Cliente/Límite: Puede explicar VNPP como el valor/monto neto pendiente de pago.
Fuente interna: Características del producto, sección Datos para el factoring; Etapa 3 C08/C36.

---

## P21 | Datos del factor
[capa=politica_producto; categoria=Datos; tipo=calculo_comercial; prioridad=media; estado=Confirmada]
Regla: Para el cálculo se usan fecha de desembolso, porcentaje de adelanto y TEA/TEM/TED. Para el agente, la fecha de desembolso se asume desde el día siguiente a la interacción.
Disparador: Durante la cotización.
Acción: Obtener tasas y factor de adelanto desde herramientas; asumir desembolso desde el día siguiente conforme a la regla del producto.
Cliente/Límite: No inventar tasas ni porcentaje de adelanto; provienen de herramientas/política vigente.
Fuente interna: Características del producto, sección Datos para el factoring.

---

## P22 | Resultados por factura
[capa=politica_producto; categoria=Cálculo; tipo=calculo_comercial; prioridad=alta; estado=Confirmada]
Regla: Por cada factura se determina plazo, intereses, comisión de factoring, IGV, importe a desembolsar y saldo remanente.
Disparador: Después de tener datos de factura y factor.
Acción: Usar la herramienta de cálculo y presentar resultados por factura.
Cliente/Límite: Explicar cada componente cuando el cliente lo requiera.
Fuente interna: Características del producto, sección Datos para el factoring.

---

## P23 | Interés compensatorio
[capa=politica_producto; categoria=Costo; tipo=calculo_comercial; prioridad=alta; estado=Confirmada]
Regla: El interés compensatorio se cobra de forma adelantada.
Disparador: Al calcular el desembolso inicial.
Acción: Descontar el interés compensatorio según el cálculo de la herramienta.
Cliente/Límite: Explicar que el interés se descuenta anticipadamente del desembolso.
Fuente interna: Características del producto, punto 11.

---

## P24 | Ingreso mínimo / comisión
[capa=politica_producto; categoria=Costo; tipo=calculo_comercial; prioridad=alta; estado=Confirmada / cambio backend pendiente]
Regla: El ingreso mínimo esperado por factura es S/ 50. Si el interés compensatorio es menor a S/ 50, la comisión de factoring es la diferencia hasta S/ 50; si el interés es S/ 50 o más, la comisión es S/ 0. Fórmula: comisión = max(50 - interés compensatorio, 0).
Disparador: Durante el cálculo por factura.
Acción: Aplicar la fórmula. El backend debe ser ajustado si aún no refleja esta regla.
Cliente/Límite: Explicar el cargo resultante sin presentar una comisión adicional cuando el interés ya alcanza S/ 50.
Fuente interna: Características del producto, punto 12; decisión confirmada por el usuario.

---

## P25 | IGV
[capa=politica_producto; categoria=Costo; tipo=calculo_comercial; prioridad=alta; estado=Confirmada]
Regla: Se aplica IGV sobre los intereses compensatorios y sobre la comisión de factoring.
Disparador: Al calcular cargos.
Acción: Calcular IGV sobre ambos conceptos conforme al parámetro vigente.
Cliente/Límite: Mostrar el IGV como componente separado de la cotización.
Fuente interna: Características del producto, punto 13.

---

## P26 | Factura del factor
[capa=politica_producto; categoria=Comprobante; tipo=calculo_comercial; prioridad=media; estado=Confirmada]
Regla: El proveedor recibe una factura del factor por los intereses compensatorios y la comisión de factoring.
Disparador: Después de originar/cobrar los conceptos correspondientes.
Acción: Considerar la emisión del comprobante del factor en el flujo operativo.
Cliente/Límite: Informar al proveedor que recibirá el comprobante por dichos conceptos.
Fuente interna: Características del producto, sección Otras características.

---

## P27 | Pago en fecha
[capa=politica_producto; categoria=Liquidación; tipo=liquidacion; prioridad=media; estado=Confirmada]
Regla: Si el adquirente paga el mismo día de la fecha de pago, el saldo remanente se deposita íntegramente al proveedor.
Disparador: Fecha efectiva de pago = fecha de pago.
Acción: Liberar/depositar el saldo remanente íntegro.
Cliente/Límite: Explicar que, si el pagador cumple en fecha, se entrega el remanente sin ajuste por desfase.
Fuente interna: Características del producto, sección Saldo remanente.

---

## P28 | Pago posterior
[capa=politica_producto; categoria=Liquidación; tipo=liquidacion; prioridad=media; estado=Confirmada]
Regla: Si el adquirente paga después de la fecha de pago, se calculan interés compensatorio adicional e interés moratorio por los días de desfase; se suma el IGV y los cargos se descuentan del saldo remanente. El proveedor recibe una nota de débito por los nuevos intereses.
Disparador: Fecha efectiva de pago > fecha de pago.
Acción: Aplicar los conceptos definidos por el producto al cierre por atraso. El agente no debe inventar una tasa o fórmula que no provenga del sistema, contrato o parámetro vigente.
Cliente/Límite: Explicar que el pago posterior genera cargos por los días de atraso que reducen el saldo remanente.
Fuente interna: Características del producto, sección Otras características - pago posterior.

---

## P29 | Pago anticipado
[capa=politica_producto; categoria=Liquidación; tipo=liquidacion; prioridad=media; estado=Confirmada]
Regla: Si el adquirente paga antes de la fecha de pago, se recalculan y devuelven los intereses compensatorios e IGV correspondientes a los días de anticipo; el importe se suma al saldo remanente y el proveedor recibe una nota de crédito. No aplica interés moratorio en este escenario.
Disparador: Fecha efectiva de pago < fecha de pago.
Acción: Recalcular el ajuste por anticipo y aumentar el importe a entregar al proveedor; gestionar nota de crédito.
Cliente/Límite: Explicar que el pago anticipado genera devolución del componente financiero correspondiente a los días no utilizados.
Fuente interna: Características del producto + corrección expresa aprobada por el usuario.

---

## P30 | Gastos de cobranza
[capa=politica_producto; categoria=Cobranza; tipo=cobranza; prioridad=media; estado=Confirmada]
Regla: En caso de pago tardío pueden existir gastos de cobranza pagados por el proveedor y descontados del saldo remanente.
Disparador: Cuando el adquirente incurre en atraso y se ejecutan gestiones cobrables.
Acción: Descontar solo gastos efectivamente aplicables y soportados por el proceso; no inventar montos.
Cliente/Límite: Informar que determinados gastos de cobranza pueden descontarse del remanente si se generan.
Fuente interna: Características del producto, sección Gastos de cobranzas.

---

## P31 | Carta notarial
[capa=politica_producto; categoria=Cobranza; tipo=cobranza; prioridad=media; estado=Confirmada]
Regla: Se contempla una carta notarial a los 7 días y otra a los 15 días de vencida la factura. Cada carta tiene un costo de S/ 20 más IGV, a cargo del proveedor y descontable del saldo remanente.
Disparador: La factura alcanza 7 o 15 días de vencida y se ejecuta la gestión correspondiente.
Acción: Aplicar únicamente el cargo de la carta efectivamente generada en el hito correspondiente.
Cliente/Límite: Informar, cuando corresponda, que cada carta notarial genera un cargo de S/ 20 más IGV.
Fuente interna: Características del producto, sección gastos de cobranza.

---

## P32 | Constancia de inscripción y titularidad
[capa=politica_producto; categoria=Cobranza; tipo=cobranza; prioridad=media; estado=Confirmada]
Regla: A los 23 días de vencida la factura se contempla obtener la constancia de inscripción y titularidad. El costo es S/ 100 más IGV, a cargo del proveedor y descontable del saldo remanente.
Disparador: La factura alcanza 23 días de vencida y corresponde ejecutar el hito.
Acción: Gestionar la constancia y aplicar el cargo cuando efectivamente corresponda.
Cliente/Límite: Informar el costo de S/ 100 más IGV cuando la gestión se genere. No llamarla “protesto” de manera literal.
Fuente interna: Características del producto, sección gastos de cobranza; Etapa 3 C27-C28.

---

## P33 | Cobro de cheque
[capa=politica_producto; categoria=Cobranza; tipo=cobranza; prioridad=media; estado=Confirmada]
Regla: Si el adquirente paga con cheque, se descuenta S/ 20 más IGV por concepto de “cobro de cheque”.
Disparador: Cuando el medio efectivo de pago sea cheque.
Acción: Aplicar el cargo de S/ 20 más IGV cuando corresponda.
Cliente/Límite: Informar el cargo cuando el pago se realice con cheque.
Fuente interna: Características del producto, última regla.

---
