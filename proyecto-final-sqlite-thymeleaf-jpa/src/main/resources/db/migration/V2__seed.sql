-- * Datos iniciales para entorno didactico/local.
-- ? Facilitan demo inmediata de listados y reglas sin carga manual.
INSERT INTO alumnos (nombre, email, fecha_nacimiento)
VALUES
('Ana Ruiz', 'ana@demo.com', '2000-05-12'),
('Luis Martin', 'luis@demo.com', '1998-11-20');

INSERT INTO cursos (nombre, tipo, fecha_inicio, fecha_fin, precio)
VALUES
('Java Backend', 'ONLINE', '2026-03-01', '2026-06-30', 249.99),
('SQL Aplicado', 'PRESENCIAL', '2026-03-15', '2026-05-15', 199.00);

INSERT INTO matriculas (alumno_id, curso_id, fecha_matricula, estado)
VALUES
(1, 1, '2026-03-02', 'ACTIVA'),
(2, 2, '2026-03-16', 'ACTIVA');

-- TODO: mover seed a perfil `dev` si se requiere un entorno `prod` limpio.
