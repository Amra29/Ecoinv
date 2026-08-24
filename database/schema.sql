-- Creación de la base de datos (Opcional si la creas manualmente desde phpMyAdmin o DBeaver)
CREATE DATABASE IF NOT EXISTS ecoinv_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE ecoinv_db;

-- Desactivar verificación de claves foráneas temporalmente para reconstrucción limpia
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS incidencias;
DROP TABLE IF EXISTS toners;
DROP TABLE IF EXISTS modelos_toner;
DROP TABLE IF EXISTS usuarios;
DROP TABLE IF EXISTS empresas;

SET FOREIGN_KEY_CHECKS = 1;

-- 1. Tabla de Empresas Clientes
CREATE TABLE empresas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    ruc_nit VARCHAR(20) UNIQUE NOT NULL,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. Tabla de Usuarios (Soporta Administradores de la Distribuidora y Clientes)
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    empresa_id INT NULL,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    rol ENUM('SUPERADMIN', 'CLIENTE') NOT NULL DEFAULT 'CLIENTE',
    FOREIGN KEY (empresa_id) REFERENCES empresas(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Catalogación de Modelos de Tóner
CREATE TABLE modelos_toner (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo_modelo VARCHAR(50) UNIQUE NOT NULL,
    descripcion VARCHAR(255) NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. Tóners Físicos Individuales (Asociados a un UUID impreso en el QR)
CREATE TABLE toners (
    id INT AUTO_INCREMENT PRIMARY KEY,
    empresa_id INT NOT NULL,
    modelo_id INT NOT NULL,
    uuid_qr VARCHAR(36) UNIQUE NOT NULL,
    estado ENUM('EN_ALMACEN', 'EN_USO', 'DEFECTUOSO', 'AGOTADO') DEFAULT 'EN_ALMACEN' NOT NULL,
    fecha_ingreso TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_apertura DATETIME NULL,
    FOREIGN KEY (empresa_id) REFERENCES empresas(id) ON DELETE CASCADE,
    FOREIGN KEY (modelo_id) REFERENCES modelos_toner(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. Registro de Incidencias y Reporte de Fallas
CREATE TABLE incidencias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    toner_id INT NOT NULL,
    usuario_id INT NOT NULL,
    tipo_falla VARCHAR(100) NOT NULL,
    descripcion TEXT NULL,
    fecha_reporte TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (toner_id) REFERENCES toners(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;