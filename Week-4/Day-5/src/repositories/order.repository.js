import Order from "../models/Order.js";

class OrderRepository {
  async create(data) {
    return await Order.create(data);
  }

  async findById(id) {
    return await Order.findById(id).populate("account");
  }

  async findPaginated({ page = 1, limit = 10, status }) {
    const query = status ? { status } : {};

    const [data, total] = await Promise.all([
      Order.find(query)
        .sort({ createdAt: -1 })
        .skip((page - 1) * limit)
        .limit(limit),
      Order.countDocuments(query),
    ]);

    return {
      data,
      total,
      page,
      pages: Math.ceil(total / limit),
    };
  }

  async update(id, data) {
    return await Order.findByIdAndUpdate(id, data, { new: true });
  }

  async delete(id) {
    return await Order.findByIdAndDelete(id);
  }
}

export default new OrderRepository();