import Account from "../models/Account.js";

class AccountRepository {
  async create(data) {
    return await Account.create(data);
  }

  async findById(id) {
    return await Account.findById(id).lean();
  }

  async findPaginated({ page = 1, limit = 10, status }) {
    const query = status ? { status } : {};

    const [data, total] = await Promise.all([
      Account.find(query)
        .sort({ createdAt: -1 })
        .skip((page - 1) * limit)
        .limit(limit),
      Account.countDocuments(query),
    ]);

    return {
      data,
      total,
      page,
      pages: Math.ceil(total / limit),
    };
  }

  async update(id, data) {
    return await Account.findByIdAndUpdate(id, data, { new: true });
  }

  async delete(id) {
    return await Account.findByIdAndDelete(id);
  }
}

export default new AccountRepository();