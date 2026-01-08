Part 1: Code Review & Debugging
Issues Identified

1. No Input Validation
The API assumes all required fields exist in the request payload.

Impact:
- KeyError exceptions
- Application crashes
- Poor user experience

Fix:
Validate required fields and return proper HTTP 400 responses.



 2. SKU Uniqueness Not Enforced
SKUs must be unique across the platform but no constraint or check exists.

Impact:
- Duplicate products
- Inventory and reporting issues

Fix:
Add a database-level UNIQUE constraint and handle IntegrityError.


3. Incorrect Product-Warehouse Relationship
Product is directly linked to a warehouse, but products can exist in multiple warehouses.

Impact:
- Violates business requirements
- Prevents scalability

Fix:
Decouple Product and Warehouse using an Inventory table.



4. No Transaction Management
Product and inventory creation are committed separately.

Impact:
- Partial data persistence
- Inconsistent database state

Fix:
Wrap operations in a single database transaction.



5. Price Stored Without Decimal Handling
Floating-point values may introduce precision errors.

Impact:
- Incorrect pricing calculations

Fix:
Use Decimal for monetary values.



6. Optional Fields Treated as Mandatory
initial_quantity is assumed to always be present.

Impact:
- Valid requests fail

Fix:
Provide default values for optional fields.



Corrected Implementation

python
from decimal import Decimal
from flask import request, jsonify
from sqlalchemy.exc import IntegrityError

@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.json or {}

    required_fields = ['name', 'sku', 'price', 'warehouse_id']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    try:
        price = Decimal(data['price'])
        initial_quantity = int(data.get('initial_quantity', 0))
    except:
        return jsonify({"error": "Invalid price or quantity"}), 400

    try:
        with db.session.begin():
            product = Product(
                name=data['name'],
                sku=data['sku'],
                price=price
            )
            db.session.add(product)
            db.session.flush()

            inventory = Inventory(
                product_id=product.id,
                warehouse_id=data['warehouse_id'],
                quantity=initial_quantity
            )
            db.session.add(inventory)

        return jsonify({"message": "Product created", "product_id": product.id}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "SKU already exists"}), 409
