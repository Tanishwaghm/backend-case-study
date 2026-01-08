from flask import jsonify

@app.route('/api/companies/<int:company_id>/alerts/low-stock', methods=['GET'])
def low_stock_alerts(company_id):
    alerts = []

    inventories = (
        db.session.query(Inventory)
        .join(Warehouse)
        .join(Product)
        .filter(Warehouse.company_id == company_id)
        .all()
    )

    for inventory in inventories:
        recent_sales = get_recent_sales(
            inventory.product_id,
            inventory.warehouse_id
        )

        if recent_sales == 0:
            continue

        threshold = inventory.product.low_stock_threshold
        if inventory.quantity >= threshold:
            continue

        avg_daily_sales = recent_sales / 30
        days_left = int(inventory.quantity / avg_daily_sales) if avg_daily_sales else None

        supplier = inventory.product.primary_supplier

        alerts.append({
            "product_id": inventory.product.id,
            "product_name": inventory.product.name,
            "sku": inventory.product.sku,
            "warehouse_id": inventory.warehouse.id,
            "warehouse_name": inventory.warehouse.name,
            "current_stock": inventory.quantity,
            "threshold": threshold,
            "days_until_stockout": days_left,
            "supplier": {
                "id": supplier.id,
                "name": supplier.name,
                "contact_email": supplier.contact_email
            }
        })

    return jsonify({
        "alerts": alerts,
        "total_alerts": len(alerts)
    })
