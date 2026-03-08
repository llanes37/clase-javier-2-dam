-- * Esquema base controlado por Flyway.
-- ! Reglas criticas tambien viven en DB para proteger integridad aunque falle la capa service.
-- ? SQLite permite indice parcial, util para imponer unicidad solo en estado ACTIVA.
CREATE TABLE IF NOT EXISTS alumnos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(120) NOT NULL,
    email VARCHAR(160) NOT NULL,
    fecha_nacimiento DATE NULL,
    CONSTRAINT uk_alumnos_email UNIQUE (email)
);

CREATE TABLE IF NOT EXISTS cursos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(150) NOT NULL,
    tipo VARCHAR(20) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    precio DECIMAL(10,2) NOT NULL CHECK (precio >= 0),
    CONSTRAINT ck_cursos_tipo CHECK (tipo IN ('ONLINE', 'PRESENCIAL')),
    CONSTRAINT ck_cursos_fechas CHECK (fecha_fin >= fecha_inicio)
);

CREATE TABLE IF NOT EXISTS matriculas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alumno_id INTEGER NOT NULL,
    curso_id INTEGER NOT NULL,
    fecha_matricula DATE NOT NULL,
    estado VARCHAR(20) NOT NULL,
    CONSTRAINT fk_matriculas_alumno FOREIGN KEY (alumno_id) REFERENCES alumnos (id) ON DELETE RESTRICT,
    CONSTRAINT fk_matriculas_curso FOREIGN KEY (curso_id) REFERENCES cursos (id) ON DELETE RESTRICT,
    CONSTRAINT ck_matriculas_estado CHECK (estado IN ('ACTIVA', 'ANULADA', 'FINALIZADA'))
);

CREATE INDEX IF NOT EXISTS idx_matriculas_alumno ON matriculas (alumno_id);
CREATE INDEX IF NOT EXISTS idx_matriculas_curso ON matriculas (curso_id);
CREATE INDEX IF NOT EXISTS idx_matriculas_estado ON matriculas (estado);

-- ! Evita que exista mas de una matricula ACTIVA por alumno y curso.
CREATE UNIQUE INDEX IF NOT EXISTS uk_matricula_activa
ON matriculas (alumno_id, curso_id)
WHERE estado = 'ACTIVA';

-- TODO: incluir tabla de auditoria si se quiere historico de cambios.
