# Ejercicios - Lección 10: Offline-First

## Ejercicio 1: Lista de posts offline

### Instrucciones

Crea una app de posts que funcione sin conexión.

**API:** `https://jsonplaceholder.typicode.com/posts`

### Requisitos

- Entidad `PostEntity` en Room
- DTO `PostDto` para Retrofit
- Repository que:
  - Expone Flow de posts desde Room
  - Tiene método `refresh()` que actualiza desde API
- UI que muestra datos de Room
- Pull-to-refresh para actualizar

### Criterios de aceptación

- [ ] Al abrir, muestra datos de Room (puede estar vacío)
- [ ] Pull-to-refresh obtiene de API y guarda en Room
- [ ] Si hay datos en Room pero no hay red, muestra datos cached
- [ ] Indicador de "sin conexión"

---

## Ejercicio 2: Caché inteligente

### Instrucciones

Implementa caché con tiempo de expiración.

### Requisitos

- Añadir campo `lastUpdated` a la entidad
- Solo hacer refresh si datos tienen más de 5 minutos
- Forzar refresh siempre con pull-to-refresh
- Mostrar "Actualizado hace X minutos"

### Criterios de aceptación

- [ ] Auto-refresh respeta tiempo de caché
- [ ] Pull-to-refresh siempre actualiza
- [ ] Se muestra tiempo desde última actualización

---

## Ejercicio 3: Crear posts offline

### Instrucciones

Permite crear posts cuando no hay conexión.

### Requisitos

- Formulario para crear post (título, contenido)
- Guardar inmediatamente en Room
- Intentar sincronizar con API
- Si falla, marcar como "pendiente"
- Indicador visual de posts pendientes de sincronizar

### Criterios de aceptación

- [ ] Crear funciona sin conexión
- [ ] Posts pendientes se identifican visualmente
- [ ] Cuando hay red, se sincronizan automáticamente
- [ ] Post sincronizado quita indicador de pendiente

---

## Ejercicio 4: Observador de conectividad

### Instrucciones

Implementa un observador de conectividad reutilizable.

### Requisitos

- Clase `ConnectivityObserver` con Flow
- Emite ONLINE/OFFLINE
- Banner en la UI cuando está offline
- Auto-refresh cuando vuelve la conexión

### Criterios de aceptación

- [ ] Flow emite cambios de conectividad
- [ ] Banner aparece/desaparece según estado
- [ ] Auto-refresh al recuperar conexión

---

## Ejercicio 5: Detalle con caché

### Instrucciones

Implementa pantalla de detalle que cachea individualmente.

### Requisitos

- Navegar de lista a detalle
- Buscar primero en Room
- Si no existe o está viejo, obtener de API
- Cachear resultado
- Funcionar offline si está cacheado

### Criterios de aceptación

- [ ] Detalle se carga de caché si existe
- [ ] Si no hay caché, obtiene de red
- [ ] Funciona offline con datos cacheados
- [ ] Muestra error si offline y sin caché

---

## Ejercicio 6: Eliminar offline

### Instrucciones

Implementa eliminación que funcione offline.

### Requisitos

- Swipe para eliminar post
- Eliminar de Room inmediatamente
- Intentar eliminar en API
- Si falla, guardar operación pendiente
- Sincronizar cuando haya red

### Criterios de aceptación

- [ ] Eliminación inmediata de la UI
- [ ] Sin conexión, se guarda como pendiente
- [ ] Con conexión, se sincroniza
- [ ] Operaciones pendientes no se pierden

---

## Ejercicio 7 (Bonus): App completa offline

### Instrucciones

Combina todo en una app de notas completa offline-first.

### Requisitos

- CRUD completo offline
- Sincronización bidireccional
- Conflictos: el más reciente gana
- WorkManager para sync en background
- Indicadores de estado de sincronización

### Estados de sincronización

```kotlin
enum class SyncStatus {
    SYNCED,      // Sincronizado con servidor
    PENDING,     // Cambios locales pendientes
    CONFLICT,    // Conflicto detectado
    ERROR        // Error de sincronización
}
```

### Criterios de aceptación

- [ ] Crear, editar, eliminar funcionan offline
- [ ] Sync automático con WorkManager
- [ ] Indicador de estado por item
- [ ] Conflictos se resuelven automáticamente
- [ ] Retry automático para errores

---

## Entrega

1. Estructura:
   ```
   data/
     local/
       entity/
       dao/
     remote/
       api/
       dto/
     repository/
   domain/
     model/
   ui/
   ```
2. Diagrama de flujo de datos
3. Crea rama y PR
