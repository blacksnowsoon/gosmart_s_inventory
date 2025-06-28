# Project Design Report: Simple Inventory Management System (Frappe Custom App)

## 1. Introduction

This document outlines the design for a custom Frappe application aimed at providing a simple inventory management system. The primary goal is to track items, their quantities, and their movement (receipts, issues, transfers, adjustments) across different warehouses, and to manage the commercial aspects of purchasing and selling these items. This design incorporates a modular structure for better organization and clear role-based access control.

## 2. Application Name

**App Name:** `inventory_manager` (or similar, e.g., `simple_inventory`)

## 3. Modules and Core Doctypes

The application is divided into three primary modules: `Inventory Masters`, `Inventory Transactions`, and `Commercial Documents`.

### 3.1. Inventory Masters Module

**Purpose:** To define and store foundational, static data (master data) required for the inventory system.

**Doctypes:**

*   **Item**
    *   **Purpose:** To define and store master data for each inventory item.
    *   **Type:** Master
    *   **Key Fields:** `item_code` (Unique), `item_name`, `description`, `unit_of_measure` (Link to UOM), `default_warehouse` (Link to Warehouse), `current_stock` (Float, Read-only), `is_active`, `item_group` (Link to Item Group), `image`.

*   **Warehouse**
    *   **Purpose:** To define and manage physical or logical locations where inventory is stored.
    *   **Type:** Master
    *   **Key Fields:** `warehouse_name` (Unique), `warehouse_code`, `address`, `is_active`, `parent_warehouse` (Self-referencing link).

*   **Supplier**
    *   **Purpose:** To track entities from whom items are procured.
    *   **Type:** Master
    *   **Key Fields:** `supplier_name` (Unique), `contact_person`, `email`, `phone`, `address`.

*   **Customer**
    *   **Purpose:** To track entities to whom items are issued/sold.
    *   **Type:** Master
    *   **Key Fields:** `customer_name` (Unique), `contact_person`, `email`, `phone`, `address`.

*   **Unit (UOM)**
    *   **Purpose:** To define various units of measurement (e.g., Pcs, Kg, Liters) used for items.
    *   **Type:** Master (Typically a standard Frappe Doctype)
    *   **Key Fields:** `unit_name` (Unique), `abbr`.

*   **Item Group**
    *   **Purpose:** To categorize items for better organization and reporting (e.g., Raw Materials, Finished Goods, Consumables).
    *   **Type:** Master (Typically a standard Frappe Doctype)
    *   **Key Fields:** `item_group_name` (Unique), `parent_item_group` (Self-referencing link).

### 3.2. Inventory Transactions Module

**Purpose:** To record all movements and changes in inventory quantities.

**Doctypes:**

*   **Stock Entry**
    *   **Purpose:** To record all movements of inventory (receipts, issues, transfers, adjustments). This is the core transactional Doctype that directly impacts stock levels.
    *   **Type:** Transaction
    *   **Key Fields:** `entry_type` (Select: Material Receipt, Material Issue, Stock Transfer, Stock Adjustment), `posting_date`, `posting_time`, `from_warehouse` (Link to Warehouse), `to_warehouse` (Link to Warehouse), `purpose`, `remarks`, `status` (Draft, Submitted, Cancelled), `items` (Child Table: Stock Entry Item), `reference_document_type` (e.g., "Purchase Order", "Sales Order"), `reference_document_name` (Link to PO/SO).

*   **Stock Entry Item** (Child Table of Stock Entry)
    *   **Purpose:** To detail the items involved in a `Stock Entry`.
    *   **Type:** Child Table
    *   **Key Fields:** `parent` (Link to Stock Entry), `item_code` (Link to Item), `item_name` (Read-only), `qty`, `unit_of_measure` (Read-only), `rate`, `amount` (Read-only).

### 3.3. Commercial Documents Module

**Purpose:** To manage purchase and sales agreements that precede actual inventory movements.

**Doctypes:**

*   **Purchase Order**
    *   **Purpose:** To record a formal commitment to purchase items from a supplier.
    *   **Type:** Transaction
    *   **Key Fields:** `supplier` (Link to Supplier), `order_date`, `required_by_date`, `status` (Draft, Submitted, To Receive, Received, To Bill, Billed, Cancelled), `total_amount` (Read-only), `terms_and_conditions`, `items` (Child Table: Purchase Order Item), `remarks`.

*   **Purchase Order Item** (Child Table of Purchase Order)
    *   **Purpose:** To detail the items being purchased in a `Purchase Order`.
    *   **Type:** Child Table
    *   **Key Fields:** `parent` (Link to Purchase Order), `item_code` (Link to Item), `item_name` (Read-only), `qty`, `unit_of_measure` (Read-only), `rate`, `amount` (Read-only), `received_qty` (Float, Read-only).

*   **Sales Order**
    *   **Purpose:** To record a formal commitment to sell items to a customer.
    *   **Type:** Transaction
    *   **Key Fields:** `customer` (Link to Customer), `order_date`, `delivery_date`, `status` (Draft, Submitted, To Deliver, Delivered, To Bill, Billed, Cancelled), `total_amount` (Read-only), `terms_and_conditions`, `items` (Child Table: Sales Order Item), `remarks`.

*   **Sales Order Item** (Child Table of Sales Order)
    *   **Purpose:** To detail the items being sold in a `Sales Order`.
    *   **Type:** Child Table
    *   **Key Fields:** `parent` (Link to Sales Order), `item_code` (Link to Item), `item_name` (Read-only), `qty`, `unit_of_measure` (Read-only), `rate`, `amount` (Read-only), `delivered_qty` (Float, Read-only).

## 4. Relationships between Doctypes

*   **Stock Entry** links to **Item** (via `Stock Entry Item` child table).
*   **Stock Entry** links to **Warehouse** (via `from_warehouse` and `to_warehouse`).
*   **Stock Entry** links to **Purchase Order** (for `Material Receipt`) or **Sales Order** (for `Material Issue`) via `reference_document_type` and `reference_document_name`.
*   **Item** links to **Unit (UOM)** and **Item Group**.
*   **Item** links to **Warehouse** (for `default_warehouse`).
*   **Purchase Order** links to **Supplier**.
*   **Purchase Order** links to **Item** (via `Purchase Order Item` child table).
*   **Sales Order** links to **Customer**.
*   **Sales Order** links to **Item** (via `Sales Order Item` child table).

## 5. Roles and Permissions

Frappe's robust Role-Based Access Control (RBAC) will be utilized. Permissions are set per Doctype to ensure segregation of duties and appropriate access levels.

| Role                      | Inventory Masters (Item, Warehouse, Supplier, Customer, Unit, Item Group) | Inventory Transactions (Stock Entry) | Commercial Documents (Purchase Order, Sales Order) |
| :------------------------ | :------------------------------------------------------------------------ | :----------------------------------- | :------------------------------------------------- |
| **System Manager**        | Full Access (CRUD, Submit, Cancel)                                        | Full Access (CRUD, Submit, Cancel)   | Full Access (CRUD, Submit, Cancel)                 |
| **Inventory Manager**     | CRUD for Item, Warehouse, Supplier, Customer, Unit, Item Group            | CRUD (Draft), Submit, Cancel         | Read, Cancel                                       |
| **Purchasing User**       | Read for Item, Warehouse, Unit, Item Group; CRUD for Supplier             | Read                                 | CRUD (Draft), Submit for Purchase Order            |
| **Sales User**            | Read for Item, Warehouse, Unit, Item Group; CRUD for Customer             | Read                                 | CRUD (Draft), Submit for Sales Order               |
| **Warehouse User**        | Read                                                                      | CRUD (Draft), Submit                 | Read                                               |
| **Viewer**                | Read                                                                      | Read                                 | Read                                               |

*   **CRUD:** Create, Read, Update, Delete.
*   **Submit/Cancel:** Specific permissions for transactional documents.
*   "Write" permission typically includes "Create" and "Update."
*   "Delete" permission for submitted documents is often restricted in production systems.

## 6. Initial Stock / Entry Stock Handling

Initial stock should **not** be set directly on the `Item` Doctype. Instead, it must be recorded using a `Stock Entry` of type `Material Receipt` or `Stock Adjustment`.

*   **Method:** Create a `Stock Entry` with `entry_type` set to `Material Receipt` or `Stock Adjustment`.
*   **Details:** Set `posting_date`, `to_warehouse`, and add the `Item` and its initial `qty` in the `items` child table.
*   **Benefit:** This method creates a proper transactional record, updates the `current_stock` on the `Item` and the stock ledger, and provides full auditability.

## 7. Basic Workflow Considerations

*   **Stock Update Logic:** Upon submission of a `Stock Entry`, server-side scripting (Python hooks/methods) will update the `current_stock` field of the respective `Item` and the stock levels within the relevant `Warehouse`.
    *   `Material Receipt`: Increases `current_stock` in `to_warehouse`. If linked to a `Purchase Order`, updates `received_qty` on the corresponding `Purchase Order Item`.
    *   `Material Issue`: Decreases `current_stock` in `from_warehouse`. If linked to a `Sales Order`, updates `delivered_qty` on the corresponding `Sales Order Item`.
    *   `Stock Transfer`: Decreases `current_stock` in `from_warehouse` and increases in `to_warehouse`.
    *   `Stock Adjustment`: Adjusts `current_stock` in `to_warehouse` (can be positive or negative adjustment).
*   **Linking Commercial Documents to Stock Entries:** When creating a `Material Receipt` from a `Purchase Order` or a `Material Issue` from a `Sales Order`, the system will allow fetching items from the respective order, ensuring consistency and updating the `received_qty` or `delivered_qty` on the order items.
*   **Reporting:** Standard Frappe reporting tools can be used to generate:
    *   Stock Balance Report (by Item, by Warehouse)
    *   Stock Ledger (history of all movements for an item)
    *   Open Purchase Orders Report
    *   Open Sales Orders Report
    *   Material Receipt/Issue Register

## 8. Future Enhancements

*   Bill of Materials (BOM)
*   Barcode Scanning Integration
*   Integration with Frappe's Accounts module for invoicing and payments.