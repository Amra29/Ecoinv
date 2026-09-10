USE ecoinv_db;

-- 1. Insertar Empresas de Prueba
INSERT INTO empresas (id, nombre, ruc_nit) VALUES
(1, 'Empresa Distribuidora Ecoinv', '0999999999001'),
(2, 'Corporación Alfa S.A.', '1790001112001'),
(3, 'Logística San José', '0987654321001');

-- 2. Insertar Usuarios
-- Contraseña para ambos: admin123 (Hash bcrypt generado)
INSERT INTO usuarios (id, empresa_id, nombre, email, password_hash, rol) VALUES
(1, NULL, 'Administrador Ecoinv', 'admin@ecoinv.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeg6Lruj3vjPGga31lW', 'SUPERADMIN'),
(2, 2, 'Juan Pérez (Alfa S.A.)', 'cliente@alfa.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeg6Lruj3vjPGga31lW', 'CLIENTE');

-- 3. Insertar Catalogación de Modelos
INSERT INTO modelos_toner (id, codigo_modelo, descripcion) VALUES
(1, 'HP-CF283A', 'Tóner HP LaserJet Pro M125 / M127 / M201'),
(2, 'CANON-CRG137', 'Tóner Canon ImageCLASS MF211 / MF212w / MF216n'),
(3, 'SAMSUNG-MLT-D111S', 'Tóner Samsung Xpress SL-M2020 / SL-M2070');

-- 4. Insertar Tóners de Prueba asignados a Corporación Alfa (Empresa ID: 2)
INSERT INTO toners (id, empresa_id, modelo_id, uuid_qr, estado) VALUES
(1, 2, 1, 'a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d', 'EN_ALMACEN'),
(2, 2, 1, 'b2c3d4e5-f6a7-8b9c-0d1e-2f3a4b5c6d7e', 'EN_ALMACEN'),
(3, 2, 2, 'c3d4e5f6-a7b8-9c0d-1e2f-3a4b5c6d7e8f', 'EN_USO');

-- 5. Insertar una Incidencia de Prueba
INSERT INTO incidencias (toner_id, usuario_id, tipo_falla, descripcion) VALUES
(3, 2, 'Mancha Impresiones', 'El tóner deja franjas negras verticales en el costado derecho de la hoja.');

USE ecoinv_db;
SELECT id, email, rol, password_hash FROM usuarios;

USE ecoinv_db;
 
UPDATE usuarios
SET password_hash = '$2b$12$bTCxTRctc488yH9NLJPM7.BCgleOuHruksqHqLXRjhdJdRP5hirBm'
WHERE email = 'admin@ecoinv.com';
 
UPDATE usuarios
SET password_hash = '$2b$12$lw4gWImbMtDkyZ8UW02DxO6orZMV2NCeSkAK9dKVKwyq/6Ko2U4oW'
WHERE email = 'cliente@alfa.com';
 
-- Verifica que se actualizaron correctamente:
SELECT id, email, password_hash, rol FROM usuarios;
 