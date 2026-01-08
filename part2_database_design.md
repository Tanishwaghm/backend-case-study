
 Part 2: Database Design

Proposed Schema

Company
- id (PK)
- name
- created_at

 Warehouse
- id (PK)
- company_id (FK)
- name
- location

Product
- id (PK)
- sku (UNIQUE)
- name
- price (DECIMAL)
- product_type
- low_stock_threshold
- created_at

 Inventory
- id (PK)
- product_id (FK)
- warehouse_id (FK)
- quantity
- updated_at
- UNIQUE(product_id, warehouse_id)

InventoryHistory
- id (PK)
- inventory_id (FK)
- change_quantity
- reason
- created_at

Supplier
- id (PK)
- name
- contact_email

ProductSupplier
- product_id (FK)
- supplier_id (FK)

ProductBundle
- bundle_id (FK)
- child_product_id (FK)
- quantity

Sales
- id (PK)
- product_id (FK)
- warehouse_id (FK)
- quantity
- sold_at

Design Decisions

- Inventory is separated from Product to support multiple warehouses.
- InventoryHistory allows auditing and tracking stock changes.
- Unique constraints prevent duplicate inventory records.
- Sales data enables low-stock prediction.
- Indexes should be added on SKU, product_id, and warehouse_id.



Missing Requirements / Questions

1. Definition of recent sales activity
2. Whether thresholds vary by category or product
3. Multiple suppliers per product support
4. Bundle inventory deduction behavior
5. Alert generation frequency
