import Account from "../models/Account.js";
import bcrypt from "bcrypt";
import jwt from "jsonwebtoken";
import config from "../config/index.js";

class AccountService {
  async register({ firstName, lastName, email, password }) {
    const existing = await Account.findOne({ email });
    if (existing) throw new Error("Email already registered");

    const account = await Account.create({ firstName, lastName, email, password });
    return {
      id: account._id,
      email: account.email,
      fullName: account.fullName,
    };
  }

  async login({ email, password }) {
    const account = await Account.findOne({ email });
    if (!account) throw new Error("Invalid credentials");

    const match = await bcrypt.compare(password, account.password);
    if (!match) throw new Error("Invalid credentials");

    const token = jwt.sign(
      { id: account._id, email: account.email },
      config.jwtSecret,
      { expiresIn: "1h" }
    );

    return { token };
  }

  async getAllAccounts() {
  return Account.find().select("-password");
}

  async getById(id) {
    return Account.findById(id);
  }
}

export default new AccountService();