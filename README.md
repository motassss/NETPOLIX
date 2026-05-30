# 🎬 NETPOLIX — Retrospectiva Sprint 3

**Proyecto:** NETPOLIX · Plataforma de Streaming con Sistema de Renta de Películas  
https://netpolix.onrender.com :)
**Sprint:** 3 · Mayo – Junio 2026  
**Desarrollador:** Esteban Alejandro Pérez  
**Institución:** Politécnico Grancolombiano · Ingeniería de Sistemas  
**Metodología:** Kanban / Scrum

---

## 📊 Métricas del Sprint

| Indicador | Valor |
|-----------|-------|
| Tareas totales | 47 |
| ✅ Terminadas | 12 |
| 🔵 En progreso | 11 |
| 🔴 Backlog activo | 8 |
| 🐛 Bugs activos | 5 |
| 📦 Progreso general | **58%** |
| 🎯 MVP listo | **85%** |

---

## ✅ ¿Qué salió bien?

**Entregas completadas:**
- Sistema de autenticación JWT funcional
- Login con diseño profesional y registro multistep con validaciones
- Catálogo dinámico con categorías desde API
- Modal de película con información completa
- Carrito de renta: agregar, eliminar, calcular total
- Pago simulado y desbloqueo de películas operativo
- Mi Lista con persistencia en base de datos
- Perfil de usuario con estadísticas básicas
- Buscador en tiempo real y manual de usuario interactivo

**Prácticas efectivas:**
- Tablero Kanban como fuente de verdad del proyecto
- Separación clara entre tareas FE y BE
- Roadmap V1 / V2 / V3 documentado desde el inicio
- Estimaciones de esfuerzo en horas por tarea
- Diferenciación clara entre MVP y funciones futuras

---

## ❌ ¿Qué salió mal?

**Bugs y problemas técnicos:**
- `NP-001` y `NP-002`: modal crítico sin resolver, bloquea scroll del body
- `NP-006`: error visual en cards con imágenes faltantes
- Dependencia circular entre `NP-001` y `NP-012` generó bloqueo de animaciones
- Navbar sin responsive en móvil — funcionalidad crítica aún pendiente

**Problemas de proceso:**
- Acumulación de tareas en Backlog sin fecha de inicio definida
- Estimación subestimada en tareas de backend (ej. panel admin: 16h)
- Sin criterios de aceptación escritos por tarea
- Sin revisión intermedia durante el sprint

---

## 🔧 ¿Qué debe mejorar?

| Área | Acción |
|------|--------|
| **Proceso** | Definir criterios de aceptación antes de iniciar cada tarea |
| **Proceso** | Limitar WIP a máximo 3 tareas simultáneas |
| **Técnico** | Resolver bugs críticos antes de agregar nuevas features |
| **Técnico** | Separar tareas de +8h en subtareas más pequeñas |
| **Calidad** | Checklist de QA antes de mover cualquier tarea a Done |
| **Calidad** | Probar responsive en móvil al terminar cada componente UI |
| **Documentación** | Mantener el manual de usuario sincronizado con los cambios |

---

## 📈 Avance por Epics

| Epic | Total | ✅ Done | 🔵 En curso | Estado |
|------|-------|---------|-------------|--------|
| E1 · UX/UI | 8 | 3 | 2 | En progreso |
| E2 · Películas | 6 | 3 | 1 | En progreso |
| E3 · Renta | 7 | 3 | 3 | En pruebas |
| E4 · Mi Lista | 5 | 2 | 2 | En pruebas |
| E5 · Perfil | 5 | 1 | 2 | En progreso |
| E6 · Configuración | 1 | 0 | 0 | Pendiente |
| E7 · Bugs | 3 | 0 | 0 | ⚠️ Crítico |
| E8 · Premium | 5 | 1 | 2 | En progreso |
| E9 · Admin | 1 | 0 | 0 | Sin iniciar |
| E10 · Futuro | 6 | 0 | 0 | Diferido V2/V3 |

---

## 📝 Reflexión

El Sprint 3 fue el ciclo de mayor complejidad técnica del proyecto. Gestionar frontend y backend simultáneamente requirió priorización estricta, y el tablero Kanban fue la herramienta central para mantener visibilidad real del avance.

El aprendizaje más importante fue que la deuda técnica tiene un costo real: la dependencia entre `NP-001` y `NP-012` bloqueó tareas de animación completas. Resolver bugs críticos antes de avanzar en nuevas features es una regla que se aplicará desde el Sprint 4.

---

## 🚀 Compromisos — Sprint 4

| # | Compromiso | Fecha límite |
|---|-----------|-------------|
| 1 | Resolver bugs críticos `NP-001` y `NP-002` antes de cualquier feature nueva | Sprint 4 · Día 1 |
| 2 | Implementar responsive en navbar móvil (`NP-003`) | Sprint 4 · Día 2 |
| 3 | Completar endpoint `/rentas/verificar` (`NP-022`) y desbloquear dependencias | Sprint 4 · Día 3 |
| 4 | Agregar criterios de aceptación a todas las tareas en "Por hacer" | Sprint 4 · Día 1 |
| 5 | Cerrar flujo de renta (`NP-026`) y mover a Done | Sprint 4 · Día 4 |
| 6 | Checkpoint de avance a mitad de sprint | Sprint 4 · Día 5 |

**Meta Sprint 4:** Cerrar el MVP V1.0 al 100% y dejarlo listo para presentación formal. 🎯

---

*NETPOLIX · Esteban Alejandro Pérez · Politécnico Grancolombiano · 2026*
