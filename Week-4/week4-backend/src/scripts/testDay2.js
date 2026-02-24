import mongoose from "mongoose";
import dotenv from "dotenv";
import AccountRepository from "../repositories/account.repository.js";
import OrderRepository from "../repositories/order.repository.js";

dotenv.config({ path: ".env.dev" });

async function run() {
  await mongoose.connect(process.env.MONGO_URI);
  console.log("DB Connected");

  // 1️⃣ Create Account
  const account = await AccountRepository.create({
    firstName: "Zoya",
    lastName: "Fatima",
    email: `zoya${Date.now()}@test.com`,
    password: "123456"
  });

  console.log("Created Account:", account.fullName);

  // 2️⃣ Pagination
  const paginated = await AccountRepository.findPaginated({
    page: 1,
    limit: 5
  });

  console.log("Paginated Result:", paginated);

  // 3️⃣ Create Order
  const order = await OrderRepository.create({
    account: account._id,
    items: [
      { productName: "Laptop", quantity: 1, price: 800 }
    ],
    totalAmount: 800
  });

  console.log("Created Order:", order);

  process.exit(0);
}

run();