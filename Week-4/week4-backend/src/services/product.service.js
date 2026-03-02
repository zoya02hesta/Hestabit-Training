import productRepository from "../repositories/product.repository.js";
import AppError from "../utils/AppError.js";

class ProductService {
  buildFilters(query) {
    const {
      search,
      minPrice,
      maxPrice,
      tags,
      includeDeleted
    } = query;

    const filter = {};

    // Soft delete control
    if (!includeDeleted || includeDeleted !== "true") {
      filter.deletedAt = null;
    }

    // Search (regex on name + description)
    if (search) {
      filter.$or = [
        { name: { $regex: search, $options: "i" } },
        { description: { $regex: search, $options: "i" } }
      ];
    }

    // Price filtering
    if (minPrice || maxPrice) {
      filter.price = {};
      if (minPrice) filter.price.$gte = Number(minPrice);
      if (maxPrice) filter.price.$lte = Number(maxPrice);
    }

    // Tags filtering
    if (tags) {
      const tagArray = tags.split(",");
      filter.tags = { $in: tagArray };
    }

    return filter;
  }

  buildSort(sortQuery) {
    if (!sortQuery) return { createdAt: -1 };

    const [field, order] = sortQuery.split(":");

    return {
      [field]: order === "desc" ? -1 : 1
    };
  }

  async getProducts(query) {
    const filter = this.buildFilters(query);
    const sort = this.buildSort(query.sort);

    const page = Number(query.page) || 1;
    const limit = Number(query.limit) || 10;

    const skip = (page - 1) * limit;

    return productRepository.findWithFilters(filter, {
      sort,
      skip,
      limit
    });
  }

  async createProduct(data) {
  return productRepository.create(data);
}

async getProductById(id) {
  const product = await productRepository.findById(id);

  if (!product || product.deletedAt) {
    throw new AppError(
      "Product not found",
      404,
      "PRODUCT_NOT_FOUND"
    );
  }

  return product;
}

async updateProduct(id, data) {
  const updatedProduct = await productRepository.updateById(id, data);

  if (!updatedProduct) {
    throw new AppError(
      "Product not found",
      404,
      "PRODUCT_NOT_FOUND"
    );
  }

  return updatedProduct;
}

  async deleteProduct(id) {
    const product = await productRepository.softDelete(id);

    if (!product) {
      throw new AppError(
        "Product not found",
        404,
        "PRODUCT_NOT_FOUND"
      );
    }

    return product;
  }
}

export default new ProductService();