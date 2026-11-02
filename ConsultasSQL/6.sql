
-- =========================================
-- 1. TABLA EMPRESAS
-- =========================================

CREATE TABLE empresas (
    id_empresa INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    sector VARCHAR(100),
    direccion VARCHAR(200),
    telefono VARCHAR(30),
    email VARCHAR(150),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================================
-- 2. TABLA EMPLEADOS
-- =========================================

CREATE TABLE empleados (
    id_empleado INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    cargo VARCHAR(100),
    fecha_ingreso DATE DEFAULT CURRENT_DATE
);

-- =========================================
-- 3. TABLA CLIENTES
-- =========================================

CREATE TABLE clientes (
    id_cliente INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE,
    telefono VARCHAR(30),
    direccion VARCHAR(200),
    estado VARCHAR(20) DEFAULT 'Activo'
        CHECK (estado IN ('Activo', 'Inactivo', 'Potencial')),
    id_empresa INTEGER,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_cliente_empresa
    FOREIGN KEY (id_empresa)
    REFERENCES empresas(id_empresa)
);

-- =========================================
-- 4. TABLA INTERACCIONES
-- =========================================

CREATE TABLE interacciones (
    id_interaccion INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_cliente INTEGER NOT NULL,
    id_empleado INTEGER NOT NULL,
    tipo VARCHAR(30) NOT NULL
        CHECK (tipo IN ('Llamada', 'Correo', 'Reunion', 'Mensaje')),
    descripcion TEXT,
    fecha_interaccion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_interaccion_cliente
    FOREIGN KEY (id_cliente)
    REFERENCES clientes(id_cliente),

    CONSTRAINT fk_interaccion_empleado
    FOREIGN KEY (id_empleado)
    REFERENCES empleados(id_empleado)
);

-- =========================================
-- 5. TABLA OPORTUNIDADES
-- =========================================

CREATE TABLE oportunidades (
    id_oportunidad INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_cliente INTEGER NOT NULL,
    id_empleado INTEGER NOT NULL,
    titulo VARCHAR(150) NOT NULL,
    descripcion TEXT,
    valor NUMERIC(12,2) DEFAULT 0
        CHECK (valor >= 0),
    estado VARCHAR(30) DEFAULT 'Nueva'
        CHECK (estado IN ('Nueva', 'En proceso', 'Ganada', 'Perdida')),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_oportunidad_cliente
    FOREIGN KEY (id_cliente)
    REFERENCES clientes(id_cliente),

    CONSTRAINT fk_oportunidad_empleado
    FOREIGN KEY (id_empleado)
    REFERENCES empleados(id_empleado)
);

-- =========================================
-- 6. INDICES PARA OPTIMIZAR LAS CONSULTAS
-- =========================================

CREATE INDEX idx_clientes_empresa
ON clientes(id_empresa);

CREATE INDEX idx_interacciones_cliente
ON interacciones(id_cliente);

CREATE INDEX idx_interacciones_empleado
ON interacciones(id_empleado);

CREATE INDEX idx_oportunidades_cliente
ON oportunidades(id_cliente);

CREATE INDEX idx_oportunidades_empleado
ON oportunidades(id_empleado);
