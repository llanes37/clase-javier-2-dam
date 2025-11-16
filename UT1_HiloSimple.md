# UT1 - Hilos en Java: Teoría y Fragmentos Clave

Este documento reúne los **conceptos teóricos** más importantes sobre hilos en Java y fragmentos de código esenciales para tu estudio. Incluye explicaciones detalladas y comentarios por bloque de código.

---

## 1. ¿Qué es un Hilo (Thread)?

* Un **hilo** es una unidad de ejecución dentro de un proceso. La **JVM (Java Virtual Machine)** puede lanzar múltiples hilos dentro del mismo programa.
* Se usa para ejecutar tareas en **paralelo** o en **concurrencia**, aprovechando mejor los núcleos del procesador.
* Todos los hilos comparten memoria, lo que permite trabajar sobre los mismos datos, pero requiere cuidado con sincronización.

```java
// Ejemplo mínimo: crea y arranca un hilo
public class MiHilo extends Thread {
    @Override
    public void run() { // Código que se ejecutará en paralelo
        System.out.println("Hola desde MiHilo");
    }
}

// En main:
new MiHilo().start(); // Se lanza el hilo
```

---

## 2. Ciclo de Vida de un Hilo

Java define varios **estados de ejecución** para los hilos:

1. **NEW**: se ha creado un objeto `Thread`, pero aún no se ha iniciado.
2. **RUNNABLE**: el hilo está listo para ejecutarse y esperando CPU.
3. **BLOCKED / WAITING / TIMED\_WAITING**: el hilo está esperando (ej: `sleep()`, `join()`).
4. **TERMINATED**: el hilo ha terminado su ejecución.

```java
Thread hilo = new Thread(() -> {/*...*/});  // NEW
hilo.start();                                // RUNNABLE
// Thread.sleep(1000);                       // TIMED_WAITING
// hilo.join();                              // WAITING
// finaliza run()                          // TERMINATED
```

---

## 3. `start()` vs `run()`

* `start()` → crea un **nuevo hilo del sistema operativo**, ejecuta `run()` en paralelo.
* `run()` → simplemente ejecuta el método en el **hilo actual**, sin concurrencia.

```java
UT1_HiloSimple miHilo = new UT1_HiloSimple();
miHilo.start(); // ✅ Concurrencia real
miHilo.run();   // ⚠️ Solo ejecuta run() en el main
```

Usar `run()` directamente NO crea un hilo nuevo, solo llama al método.

---

## 4. `sleep()` e `interrupt()`

* `Thread.sleep(millis)`: pausa el hilo actual durante el tiempo indicado.
* `interrupt()`: indica que se desea interrumpir un hilo (por ejemplo, si está esperando o durmiendo).

```java
try {
    Thread.sleep(500); // pausa medio segundo
} catch (InterruptedException e) {
    System.out.println("Hilo interrumpido");
}
```

También puedes interrumpir manualmente:

```java
Thread hilo = new Thread(() -> {
    while (!Thread.currentThread().isInterrupted()) {
        // bucle hasta que se interrumpa
    }
});
hilo.start();
hilo.interrupt(); // pide su interrupción
```

---

## 5. `join()`

Sirve para que **un hilo espere a otro** antes de continuar. Es útil para forzar orden de ejecución.

```java
Thread hilo = new Thread(() -> {
    System.out.println("Tarea del hilo");
});
hilo.start();
hilo.join();  // El hilo principal espera a que hilo termine
System.out.println("Fin tras join");
```

---

## 6. Prioridad de Hilo

Los hilos tienen prioridad entre 1 y 10:

* `Thread.MIN_PRIORITY = 1`
* `Thread.NORM_PRIORITY = 5`
* `Thread.MAX_PRIORITY = 10`

No se garantiza el orden, pero puede influir en el **planificador del sistema operativo**.

```java
Thread hilo = new Thread(...);
hilo.setPriority(Thread.MAX_PRIORITY); // prioridad más alta
```

---

## 7. Sincronización y Condiciones de Carrera

Cuando múltiples hilos acceden a un mismo recurso (como una variable), puede haber errores llamados **race conditions**.

Se usa `synchronized` para proteger secciones críticas:

```java
public class Contador {
    private int count = 0;

    public synchronized void incrementar() { // solo 1 hilo a la vez puede ejecutar esto
        count++;
    }

    public int getCount() {
        return count;
    }
}
```

También se puede sincronizar sobre un objeto:

```java
synchronized (this) {
    // sección crítica
}
```

---

## 8. Runnable y ExecutorService

* En vez de extender `Thread`, se puede implementar `Runnable` (mejor práctica).
* `ExecutorService` permite gestionar un **pool de hilos reutilizables**.

```java
ExecutorService pool = Executors.newFixedThreadPool(3); // pool con 3 hilos

pool.submit(() -> {
    System.out.println("Tarea ejecutada en hilo del pool");
});

pool.shutdown(); // No se aceptan más tareas, se espera a que terminen
```

📌 `submit()` permite enviar tareas Runnable.

---

## 9. ¿Por qué usar hilos? Casos reales

* **Servidores web**: manejar miles de usuarios a la vez.
* **Interfaces gráficas**: no bloquear la ventana mientras se carga algo.
* **Juegos**: movimiento, lógica, sonido en paralelo.
* **Aplicaciones de red**: transferencias, conexiones, etc.
* **Procesamiento masivo**: usar los núcleos del procesador de forma eficiente.

---

## Fragmentos Clave para Práctica Rápida

### 1. Extender Thread

```java
public class MiHilo extends Thread {
    @Override
    public void run() {
        System.out.println("Paso 1");
    }
}

new MiHilo().start();
```

### 2. Implementar Runnable

```java
Runnable tarea = () -> System.out.println("Desde Runnable");
new Thread(tarea).start();
```

### 3. Uso de join() con timeout

```java
hilo.join(500); // espera 500ms máximo
System.out.println("Esperé max 0.5s");
```

### 4. Sincronización básica

```java
public synchronized void metodoCritico() {
    // sección que solo un hilo puede usar
}
```

### 5. Interrupción

```java
Thread hilo = new Thread(() -> {
    while (!Thread.currentThread().isInterrupted()) {
        // bucle infinito controlado
    }
});
hilo.start();
hilo.interrupt();
```

---

Este resumen cubre todos los puntos esenciales de **UT1 - Hilos en Java**, con explicaciones claras, ejemplos comentados y fragmentos listos para escribir en un examen o practicar en clase.
