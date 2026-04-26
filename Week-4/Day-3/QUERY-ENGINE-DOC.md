# Product Query Engine Documentation

## Overview

The Product Query Engine provides advanced filtering, searching, sorting, and pagination capabilities for the Products API.

Base Endpoint:

GET /api/products

This system supports:

- Search (name + description)
- Price filtering
- Tag filtering
- Sorting
- Pagination
- Soft delete control

---

## Supported Query Parameters

### 1. Search

Searches product name and description using case-insensitive regex.

Example:

GET /api/products?search=iphone

---

### 2. Price Filtering

Filter products within a price range.

Parameters:

- minPrice
- maxPrice

Examples:

GET /api/products?minPrice=50000
GET /api/products?maxPrice=100000
GET /api/products?minPrice=50000&maxPrice=100000

---

### 3. Tag Filtering

Filter products by tags.

Supports multiple tags separated by commas.

Example:

GET /api/products?tags=mobile,android

This returns products that contain any of the specified tags.

---

### 4. Sorting

Sort products by a field.

Format:

sort=field:order

Order:
- asc (default)
- desc

Examples:

GET /api/products?sort=price:asc
GET /api/products?sort=price:desc
GET /api/products?sort=createdAt:desc

Default sorting:
createdAt descending

---

### 5. Pagination

Supports page-based pagination.

Parameters:

- page (default: 1)
- limit (default: 10)

Example:

GET /api/products?page=2&limit=5

Pagination formula:
skip = (page - 1) * limit

---

### 6. Soft Delete Control

By default, soft-deleted products are excluded.

To include soft-deleted products:

GET /api/products?includeDeleted=true

Soft delete is implemented using a `deletedAt` field.

---

## Combined Example

You can combine multiple query parameters:

GET /api/products?search=iphone&minPrice=50000&sort=price:desc&page=1&limit=5

This will:

- Search for "iphone"
- Filter price >= 50000
- Sort by price descending
- Return first page
- Limit results to 5 items

---

## Response Structure

Successful response:

{
  "success": true,
  "data": [...],
  "total": 25
}

Where:
- data → paginated product list
- total → total matching documents (before pagination)

---

## Error Handling

If an invalid product ID is provided:

{
  "success": false,
  "message": "Product not found",
  "code": "PRODUCT_NOT_FOUND"
}

All errors follow a structured error format.

---

## Architecture

Query handling flow:

Controller → Service (Query Builder) → Repository → Database

Business logic is handled in the Service layer.
Database queries are handled in the Repository layer.

---

## Conclusion

The Product Query Engine provides flexible and scalable querying capabilities while maintaining clean architecture and separation of concerns.