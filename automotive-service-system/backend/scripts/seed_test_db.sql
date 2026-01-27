-- Seed SQL for PostgreSQL (DBeaver)
-- Safe to re-run: uses ON CONFLICT where possible and NOT EXISTS checks.

BEGIN;

-- 1) Suppliers (no unique constraint, so we seed by name with NOT EXISTS)
INSERT INTO suppliers (name, phone, email)
SELECT 'AutoParts SA', '+55 11 4000-1000', 'contato@autoparts.example'
WHERE NOT EXISTS (SELECT 1 FROM suppliers WHERE name = 'AutoParts SA');

INSERT INTO suppliers (name, phone, email)
SELECT 'MegaLub Distribuidora', '+55 11 4000-2000', 'vendas@megalub.example'
WHERE NOT EXISTS (SELECT 1 FROM suppliers WHERE name = 'MegaLub Distribuidora');

-- 2) Materials (internal_code has unique constraint)
INSERT INTO materials (
  internal_code, name, category,
  market_avg_price, margin_percent, sale_price,
  stock_current, stock_minimum, active
) VALUES
  ('OIL-5W30', 'Óleo 5W30 (1L)', 'Lubrificante', 35.00, 40.00, ROUND(35.00 * 1.40, 2), 30, 5, TRUE),
  ('FILTER-OIL', 'Filtro de Óleo', 'Filtro', 25.00, 50.00, ROUND(25.00 * 1.50, 2), 20, 5, TRUE),
  ('BRAKEPAD-FRONT', 'Pastilha de Freio Dianteira', 'Freio', 120.00, 35.00, ROUND(120.00 * 1.35, 2), 10, 2, TRUE)
ON CONFLICT (internal_code) DO UPDATE SET
  name = EXCLUDED.name,
  category = EXCLUDED.category,
  market_avg_price = EXCLUDED.market_avg_price,
  margin_percent = EXCLUDED.margin_percent,
  sale_price = EXCLUDED.sale_price,
  stock_current = EXCLUDED.stock_current,
  stock_minimum = EXCLUDED.stock_minimum,
  active = EXCLUDED.active;

-- 3) Material <-> Supplier (composite PK)
INSERT INTO material_suppliers (material_id, supplier_id, purchase_price, last_updated)
SELECT m.id, s.id, 15.00, TIMESTAMP '2026-01-27 12:00:00'
FROM materials m
JOIN suppliers s ON s.name = 'AutoParts SA'
WHERE m.internal_code = 'FILTER-OIL'
ON CONFLICT (material_id, supplier_id) DO UPDATE SET
  purchase_price = EXCLUDED.purchase_price,
  last_updated = EXCLUDED.last_updated;

INSERT INTO material_suppliers (material_id, supplier_id, purchase_price, last_updated)
SELECT m.id, s.id, 22.00, TIMESTAMP '2026-01-27 12:00:00'
FROM materials m
JOIN suppliers s ON s.name = 'MegaLub Distribuidora'
WHERE m.internal_code = 'OIL-5W30'
ON CONFLICT (material_id, supplier_id) DO UPDATE SET
  purchase_price = EXCLUDED.purchase_price,
  last_updated = EXCLUDED.last_updated;

INSERT INTO material_suppliers (material_id, supplier_id, purchase_price, last_updated)
SELECT m.id, s.id, 75.00, TIMESTAMP '2026-01-27 12:00:00'
FROM materials m
JOIN suppliers s ON s.name = 'AutoParts SA'
WHERE m.internal_code = 'BRAKEPAD-FRONT'
ON CONFLICT (material_id, supplier_id) DO UPDATE SET
  purchase_price = EXCLUDED.purchase_price,
  last_updated = EXCLUDED.last_updated;

-- 4) Services (no unique constraint; seed by name)
INSERT INTO services (name, description, average_time, labor_cost)
SELECT 'Troca de óleo', 'Troca de óleo e filtro', 60, 120.00
WHERE NOT EXISTS (SELECT 1 FROM services WHERE name = 'Troca de óleo');

INSERT INTO services (name, description, average_time, labor_cost)
SELECT 'Troca de pastilhas de freio', 'Substituição de pastilhas dianteiras', 90, 180.00
WHERE NOT EXISTS (SELECT 1 FROM services WHERE name = 'Troca de pastilhas de freio');

-- 5) Service materials (composite PK)
INSERT INTO service_materials (service_id, material_id, quantity)
SELECT s.id, m.id, 4
FROM services s
JOIN materials m ON m.internal_code = 'OIL-5W30'
WHERE s.name = 'Troca de óleo'
ON CONFLICT (service_id, material_id) DO UPDATE SET quantity = EXCLUDED.quantity;

INSERT INTO service_materials (service_id, material_id, quantity)
SELECT s.id, m.id, 1
FROM services s
JOIN materials m ON m.internal_code = 'FILTER-OIL'
WHERE s.name = 'Troca de óleo'
ON CONFLICT (service_id, material_id) DO UPDATE SET quantity = EXCLUDED.quantity;

INSERT INTO service_materials (service_id, material_id, quantity)
SELECT s.id, m.id, 1
FROM services s
JOIN materials m ON m.internal_code = 'BRAKEPAD-FRONT'
WHERE s.name = 'Troca de pastilhas de freio'
ON CONFLICT (service_id, material_id) DO UPDATE SET quantity = EXCLUDED.quantity;

-- 6) Vehicles (seed by brand/model/year/engine)
INSERT INTO vehicles (brand, model, year, engine)
SELECT 'Volkswagen', 'Gol', 2015, '1.6'
WHERE NOT EXISTS (
  SELECT 1 FROM vehicles WHERE brand='Volkswagen' AND model='Gol' AND year=2015 AND engine='1.6'
);

INSERT INTO vehicles (brand, model, year, engine)
SELECT 'Honda', 'Civic', 2018, '2.0'
WHERE NOT EXISTS (
  SELECT 1 FROM vehicles WHERE brand='Honda' AND model='Civic' AND year=2018 AND engine='2.0'
);

-- 7) Vehicle <-> Services (composite PK)
INSERT INTO vehicle_services (vehicle_id, service_id)
SELECT v.id, s.id
FROM vehicles v
JOIN services s ON s.name = 'Troca de óleo'
WHERE v.brand='Volkswagen' AND v.model='Gol' AND v.year=2015 AND v.engine='1.6'
ON CONFLICT (vehicle_id, service_id) DO NOTHING;

INSERT INTO vehicle_services (vehicle_id, service_id)
SELECT v.id, s.id
FROM vehicles v
JOIN services s ON s.name = 'Troca de pastilhas de freio'
WHERE v.brand='Volkswagen' AND v.model='Gol' AND v.year=2015 AND v.engine='1.6'
ON CONFLICT (vehicle_id, service_id) DO NOTHING;

INSERT INTO vehicle_services (vehicle_id, service_id)
SELECT v.id, s.id
FROM vehicles v
JOIN services s ON s.name = 'Troca de óleo'
WHERE v.brand='Honda' AND v.model='Civic' AND v.year=2018 AND v.engine='2.0'
ON CONFLICT (vehicle_id, service_id) DO NOTHING;

-- 8) Vehicle <-> Materials (composite PK)
INSERT INTO vehicle_materials (vehicle_id, material_id)
SELECT v.id, m.id
FROM vehicles v
JOIN materials m ON m.internal_code IN ('OIL-5W30','FILTER-OIL','BRAKEPAD-FRONT')
WHERE v.brand='Volkswagen' AND v.model='Gol' AND v.year=2015 AND v.engine='1.6'
ON CONFLICT (vehicle_id, material_id) DO NOTHING;

-- 9) Customers (email unique)
INSERT INTO customers (name, phone, email)
VALUES
  ('Maria Silva', '+55 11 99999-1111', 'maria@exemplo.com'),
  ('João Souza', '+55 11 98888-2222', 'joao@exemplo.com')
ON CONFLICT (email) DO UPDATE SET
  name = EXCLUDED.name,
  phone = EXCLUDED.phone;

-- 10) Workers (email unique)
INSERT INTO workers (name, phone, email, service_specialty)
VALUES
  ('Carlos Mecânico', '+55 11 97777-3333', 'carlos@oficina.com', 'Motor'),
  ('Ana Técnica', '+55 11 96666-4444', 'ana@oficina.com', 'Freios')
ON CONFLICT (email) DO UPDATE SET
  name = EXCLUDED.name,
  phone = EXCLUDED.phone,
  service_specialty = EXCLUDED.service_specialty;

-- 11) Appointments
INSERT INTO appointments (customer_id, vehicle_id, service_id, status, total_value)
SELECT c.id, v.id, s.id, 'scheduled', 260.00
FROM customers c
JOIN vehicles v ON v.brand='Volkswagen' AND v.model='Gol' AND v.year=2015 AND v.engine='1.6'
JOIN services s ON s.name='Troca de óleo'
WHERE c.email='maria@exemplo.com'
AND NOT EXISTS (
  SELECT 1 FROM appointments a
  WHERE a.customer_id=c.id AND a.vehicle_id=v.id AND a.service_id=s.id
    AND a.status='scheduled' AND a.total_value=260.00
);

INSERT INTO appointments (customer_id, vehicle_id, service_id, status, total_value)
SELECT c.id, v.id, s.id, 'completed', 340.00
FROM customers c
JOIN vehicles v ON v.brand='Volkswagen' AND v.model='Gol' AND v.year=2015 AND v.engine='1.6'
JOIN services s ON s.name='Troca de pastilhas de freio'
WHERE c.email='joao@exemplo.com'
AND NOT EXISTS (
  SELECT 1 FROM appointments a
  WHERE a.customer_id=c.id AND a.vehicle_id=v.id AND a.service_id=s.id
    AND a.status='completed' AND a.total_value=340.00
);

-- 12) Appointment <-> Workers
INSERT INTO appointment_workers (appointment_id, worker_id)
SELECT a.id, w.id
FROM appointments a
JOIN customers c ON c.id = a.customer_id
JOIN workers w ON w.email='carlos@oficina.com'
WHERE c.email='maria@exemplo.com' AND a.status='scheduled' AND a.total_value=260.00
ON CONFLICT (appointment_id, worker_id) DO NOTHING;

INSERT INTO appointment_workers (appointment_id, worker_id)
SELECT a.id, w.id
FROM appointments a
JOIN customers c ON c.id = a.customer_id
JOIN workers w ON w.email='ana@oficina.com'
WHERE c.email='joao@exemplo.com' AND a.status='completed' AND a.total_value=340.00
ON CONFLICT (appointment_id, worker_id) DO NOTHING;

-- 13) Stock flows (idempotent by fixed timestamp + values)
INSERT INTO stock_flows (material_id, appointment_id, flow_type, quantity, origin, created_at)
SELECT m.id, NULL, 'entry', 30, 'purchase', TIMESTAMP '2026-01-27 12:00:00'
FROM materials m
WHERE m.internal_code='OIL-5W30'
AND NOT EXISTS (
  SELECT 1 FROM stock_flows sf
  WHERE sf.material_id=m.id AND sf.appointment_id IS NULL
    AND sf.flow_type='entry' AND sf.quantity=30 AND sf.origin='purchase'
    AND sf.created_at=TIMESTAMP '2026-01-27 12:00:00'
);

INSERT INTO stock_flows (material_id, appointment_id, flow_type, quantity, origin, created_at)
SELECT m.id, NULL, 'entry', 20, 'purchase', TIMESTAMP '2026-01-27 12:00:00'
FROM materials m
WHERE m.internal_code='FILTER-OIL'
AND NOT EXISTS (
  SELECT 1 FROM stock_flows sf
  WHERE sf.material_id=m.id AND sf.appointment_id IS NULL
    AND sf.flow_type='entry' AND sf.quantity=20 AND sf.origin='purchase'
    AND sf.created_at=TIMESTAMP '2026-01-27 12:00:00'
);

INSERT INTO stock_flows (material_id, appointment_id, flow_type, quantity, origin, created_at)
SELECT m.id, NULL, 'entry', 10, 'purchase', TIMESTAMP '2026-01-27 12:00:00'
FROM materials m
WHERE m.internal_code='BRAKEPAD-FRONT'
AND NOT EXISTS (
  SELECT 1 FROM stock_flows sf
  WHERE sf.material_id=m.id AND sf.appointment_id IS NULL
    AND sf.flow_type='entry' AND sf.quantity=10 AND sf.origin='purchase'
    AND sf.created_at=TIMESTAMP '2026-01-27 12:00:00'
);

-- Consumption tied to the "Troca de óleo" appointment
INSERT INTO stock_flows (material_id, appointment_id, flow_type, quantity, origin, created_at)
SELECT m.id, a.id, 'exit', 4, 'service_use', TIMESTAMP '2026-01-27 12:00:00'
FROM materials m
JOIN appointments a ON a.status='scheduled' AND a.total_value=260.00
JOIN customers c ON c.id=a.customer_id AND c.email='maria@exemplo.com'
WHERE m.internal_code='OIL-5W30'
AND NOT EXISTS (
  SELECT 1 FROM stock_flows sf
  WHERE sf.material_id=m.id AND sf.appointment_id=a.id
    AND sf.flow_type='exit' AND sf.quantity=4 AND sf.origin='service_use'
    AND sf.created_at=TIMESTAMP '2026-01-27 12:00:00'
);

INSERT INTO stock_flows (material_id, appointment_id, flow_type, quantity, origin, created_at)
SELECT m.id, a.id, 'exit', 1, 'service_use', TIMESTAMP '2026-01-27 12:00:00'
FROM materials m
JOIN appointments a ON a.status='scheduled' AND a.total_value=260.00
JOIN customers c ON c.id=a.customer_id AND c.email='maria@exemplo.com'
WHERE m.internal_code='FILTER-OIL'
AND NOT EXISTS (
  SELECT 1 FROM stock_flows sf
  WHERE sf.material_id=m.id AND sf.appointment_id=a.id
    AND sf.flow_type='exit' AND sf.quantity=1 AND sf.origin='service_use'
    AND sf.created_at=TIMESTAMP '2026-01-27 12:00:00'
);

-- Consumption tied to the "Troca de pastilhas" appointment
INSERT INTO stock_flows (material_id, appointment_id, flow_type, quantity, origin, created_at)
SELECT m.id, a.id, 'exit', 1, 'service_use', TIMESTAMP '2026-01-27 12:00:00'
FROM materials m
JOIN appointments a ON a.status='completed' AND a.total_value=340.00
JOIN customers c ON c.id=a.customer_id AND c.email='joao@exemplo.com'
WHERE m.internal_code='BRAKEPAD-FRONT'
AND NOT EXISTS (
  SELECT 1 FROM stock_flows sf
  WHERE sf.material_id=m.id AND sf.appointment_id=a.id
    AND sf.flow_type='exit' AND sf.quantity=1 AND sf.origin='service_use'
    AND sf.created_at=TIMESTAMP '2026-01-27 12:00:00'
);

COMMIT;
