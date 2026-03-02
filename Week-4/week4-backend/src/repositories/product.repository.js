import Product from "../models/Product.js";

class ProductRepository {
  async create(data) {
    return Product.create(data);
  }

  async findWithFilters(filter, options) {
    const { sort, skip, limit } = options;

    const query = Product.find(filter)
      .sort(sort)
      .skip(skip)
      .limit(limit);

    const [data, total] = await Promise.all([
      query,
      Product.countDocuments(filter)
    ]);

    return { data, total };
  }

  async findById(id) {
    return Product.findById(id);
  }

async updateById(id, data) {
  return Product.findByIdAndUpdate(
    id,
    data,
    { new: true, runValidators: true }
  );
}

  async softDelete(id) {
    return Product.findByIdAndUpdate(
      id,
      { deletedAt: new Date() },
      { new: true }
    );
  }
}

export default new ProductRepository();