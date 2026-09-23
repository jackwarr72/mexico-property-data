# Resumen de funciones, mejoras y restricciones futuras

## 1. Estado actual

El sistema actual incluye:

- Ingesta de propiedades desde archivos JSON locales.
- Normalización y deduplicación de propiedades.
- Exportación de propiedades a CSV.
- Importación de propiedades a PostgreSQL.
- Registro de fuentes y metadatos de cumplimiento.
- Registro de contenido comunitario, foros, Q&A, comentarios y redes sociales.
- Configuraciones de fuentes con estado habilitado, deshabilitado o revisión manual.
- Dashboard Streamlit en español.
- Filtros por estado, tipo de propiedad, fuente y rango de precio.
- Detalle interactivo de propiedades.
- Notas de seguimiento por propiedad.
- Directorio de alianzas: brokers, notarios, valuadores, abogados y financiamiento.
- Registro manual de KPIs.
- Metas operativas: 20 o más propiedades por día y 10 o más citas por semana.
- Alertas por palabras clave como `Venta urgente` y `Reducción de precio`.
- Búsquedas avanzadas de Google con `site:`, `intitle:` e `inurl:`.
- Analytics e Insights con datos reales o datos demo claramente identificados.
- Tendencias, sentimiento, preocupaciones, mapas de actividad y rankings.
- Exportaciones CSV, JSON, Excel, PDF, PNG y SVG.
- Historial de exportaciones.
- PostgreSQL local mediante Docker.
- Pruebas automatizadas de ingesta, analytics y exportaciones.

## 2. Mejoras prioritarias

### Datos y backend

- Reemplazar datos demo por agregaciones reales de `community_content`.
- Calcular preguntas, temas, sentimiento, intención y tendencias a partir de fechas reales.
- Añadir filtros server-side por periodo, ubicación, fuente, intención, sentimiento y tema.
- Incorporar paginación SQL para conjuntos grandes.
- Añadir índices PostgreSQL para fechas, fuente, municipio, sentimiento y tipo de contenido.
- Crear vistas SQL para métricas diarias, semanales y mensuales.
- Mantener historial de cambios de precio y estado de anuncios.
- Detectar automáticamente anuncios nuevos, modificados, retirados y duplicados.
- Añadir validación de calidad de datos y reportes de registros incompletos.
- Implementar un sistema de estados para revisión humana: nuevo, revisado, aprobado, rechazado y archivado.

### Ingesta y fuentes

- Crear adaptadores separados para cada fuente autorizada.
- Añadir ejecución programada para feeds oficiales y APIs permitidas.
- Añadir reintentos con backoff y límites de velocidad.
- Registrar cada ejecución de ingesta, duración, cantidad de registros y errores.
- Registrar `last_crawled_at`, `last_success_at` y `last_error` en cada fuente.
- Añadir validación automática de robots.txt, términos de uso y permisos antes de activar una fuente.
- Añadir pruebas de contrato por adaptador.
- Crear una cola de revisión para nuevas fuentes descubiertas.
- Permitir pausar una fuente inmediatamente cuando cambien sus reglas de acceso.

### Analytics

- Calcular tendencias contra periodos anteriores reales.
- Clasificar automáticamente intención de compra, venta, renta, financiamiento y consulta general.
- Extraer temas y entidades relevantes de discusiones.
- Calcular sentimiento solo mediante un proveedor o modelo aprobado y documentado.
- Separar siempre hechos medidos de interpretaciones generadas por IA.
- Añadir referencias y fuentes verificables a cada insight.
- Añadir comparación por estado, municipio, colonia, fuente y plataforma.
- Añadir alertas por cambios anómalos de volumen, precio o sentimiento.
- Permitir guardar filtros y vistas frecuentes.

### Dashboard

- Añadir navegación de página real si se migra a una aplicación web con rutas.
- Mantener la vista Operations existente sin regresiones.
- Añadir estados de carga, vacío, error y reintento para cada widget.
- Añadir actualización manual y automática de datos.
- Añadir filtros globales compartidos por todos los widgets.
- Mejorar el mapa con coordenadas reales y agrupación de puntos.
- Añadir tooltips, leyendas y accesibilidad para gráficos.
- Añadir vista móvil específica para tablas, filtros y exportaciones.
- Añadir permisos por rol: administrador, analista, operador y solo lectura.

### Exportaciones

- Mantener CSV y JSON para análisis técnico.
- Mantener Excel para análisis operativo y presentación interna.
- Mejorar PDF con identidad visual, paginación, fuentes y gráficos vectoriales.
- Exportar cada gráfico con los filtros y periodo activos.
- Añadir exportación de datos geográficos compatible con GeoJSON.
- Añadir exportación de tablas filtradas desde cada widget.
- Implementar trabajos en segundo plano para exportaciones grandes.
- Mostrar progreso, estado, error y descarga de cada trabajo.
- Añadir caducidad y limpieza automática de archivos exportados.
- Añadir controles de acceso antes de generar cualquier exportación.
- Mantener historial de usuario, fecha, formato, filtros y estado.

## 3. Restricciones legales y de cumplimiento

Estas restricciones deben mantenerse en todas las futuras mejoras:

- Solo ingerir contenido públicamente accesible y legalmente permitido.
- No acceder a cuentas, grupos o perfiles privados.
- No evadir autenticación, controles técnicos, paywalls o restricciones de acceso.
- No ignorar robots.txt, términos de uso ni límites de velocidad.
- No realizar scraping masivo de portales restringidos sin autorización escrita.
- Usar APIs oficiales únicamente con credenciales, permisos y alcance autorizados.
- Facebook Graph API solo cuando la aplicación y el acceso estén oficialmente permitidos.
- X/Twitter, TikTok, YouTube, Reddit, LinkedIn y Quora deben respetar sus APIs y políticas vigentes.
- No almacenar datos personales innecesarios.
- Preferir nombres públicos de display y evitar datos sensibles.
- No inferir identidad, situación financiera, domicilio privado u otras características sensibles.
- Aplicar minimización de datos, retención limitada y eliminación cuando corresponda.
- Conservar URL, fuente, fecha, licencia y requisitos de atribución.
- Separar información oficial gubernamental de contenido generado por usuarios.
- Marcar contenido no verificado como `manual_review`.
- No presentar una interpretación de IA como un hecho comprobado.
- Mantener trazabilidad desde cada métrica hasta sus registros de origen.
- Revisar permisos antes de activar una fuente nueva o cambiar su frecuencia.

## 4. Restricciones técnicas

- El sistema actual usa Python, Streamlit, PostgreSQL y Docker.
- Los nombres de tablas y campos existentes deben conservarse para evitar romper imports.
- Las nuevas funciones deben reutilizar `AnalyticsData` y `export_service.py`.
- No crear datasets independientes para la interfaz y las exportaciones.
- El dashboard debe continuar funcionando si `community_content` está vacío.
- Los datos demo deben estar claramente etiquetados y aislados.
- Las exportaciones deben usar UTF-8 y preservar caracteres españoles.
- Las consultas SQL deben usar parámetros, nunca concatenar valores del usuario.
- Los archivos exportados deben tener nombres seguros y no permitir traversal de rutas.
- Las cargas grandes deben paginarse o procesarse en segundo plano.
- Los errores de una fuente no deben detener las demás fuentes.
- Las migraciones de base de datos deben ser idempotentes.
- Las credenciales deben permanecer en `.env` y nunca en el código fuente.
- Los logs no deben imprimir contraseñas, tokens ni contenido privado.
- El sistema debe continuar siendo ejecutable localmente con Docker.

## 5. Seguridad y permisos futuros

- Incorporar autenticación de usuarios.
- Implementar autorización por rol y por fuente.
- Aplicar los permisos en el backend, no solo en la interfaz.
- Verificar permisos antes de consultar, mostrar o exportar datos.
- Auditar accesos a contenido sensible o de revisión manual.
- Rotar credenciales de APIs y usar variables de entorno seguras.
- Añadir límites de solicitudes por usuario.
- Añadir protección contra inyección SQL, XSS y cargas maliciosas.
- Validar URLs externas antes de mostrarlas o procesarlas.
- Limitar tamaño y profundidad de JSON importado.
- Escanear archivos de entrada y exportación cuando el entorno lo requiera.

## 6. Pruebas necesarias

### Pruebas de datos

- Normalización de cada adaptador.
- Deduplicación por ID, URL y huella de contenido.
- Fechas inválidas y zonas horarias.
- Precios, rentas y superficies con valores faltantes.
- Caracteres españoles y Unicode.
- Datos incompletos o malformados.
- Registros duplicados entre fuentes.

### Pruebas del dashboard

- Filtros combinados.
- Periodos de 7, 30 y 90 días.
- Ubicación, fuente, intención y sentimiento.
- Estado vacío.
- Error de PostgreSQL.
- Error de una fuente individual.
- Uso en escritorio, tablet y móvil.
- Navegación entre Operaciones, Análisis y Tendencias.

### Pruebas de exportación

- Headers y filas CSV.
- UTF-8 y caracteres españoles.
- Hojas y formatos XLSX.
- PDF con secciones y saltos de página.
- PNG y SVG de gráficos.
- Filtros aplicados a todas las salidas.
- Nombres de archivo seguros.
- Exportación de conjuntos grandes.
- Permisos insuficientes.
- Eliminación y caducidad de archivos.

## 7. Roadmap recomendado

### Fase 1: Consolidación

- Mantener pruebas automatizadas.
- Corregir cualquier texto restante en inglés.
- Añadir índices y vistas SQL.
- Añadir registros de ejecución de ingesta.
- Confirmar migraciones idempotentes.

### Fase 2: Datos reales

- Importar contenido comunitario autorizado.
- Implementar métricas reales desde `community_content`.
- Sustituir progresivamente los datos demo.
- Añadir validación y revisión humana.

### Fase 3: Operación automatizada

- Programar feeds y APIs autorizadas.
- Añadir alertas de cambios y errores.
- Añadir colas para ingestas y exportaciones.
- Añadir historial y monitoreo operativo.

### Fase 4: Seguridad y colaboración

- Autenticación.
- Roles y permisos.
- Auditoría.
- Compartición segura de reportes.

### Fase 5: Escala

- Separar frontend y API si Streamlit deja de ser suficiente.
- Añadir rutas como `/analytics` y `/trends`.
- Añadir almacenamiento de objetos para exportaciones.
- Añadir workers y una cola de tareas.
- Añadir observabilidad, métricas y alertas de infraestructura.

## 8. Decisiones que requerirán confirmación

Antes de implementar fases posteriores conviene decidir:

- Qué fuentes tienen autorización formal.
- Qué datos personales se pueden conservar.
- Cuánto tiempo deben conservarse los datos.
- Qué usuarios podrán exportar información.
- Qué proveedor se usará para sentimiento o clasificación.
- Si los insights de IA requieren aprobación humana.
- Si la aplicación seguirá siendo local o se desplegará en la nube.
- Qué volumen de datos se espera por día y por fuente.
- Si se necesita multiusuario y auditoría completa.
- Qué identidad visual deben tener los reportes PDF.
