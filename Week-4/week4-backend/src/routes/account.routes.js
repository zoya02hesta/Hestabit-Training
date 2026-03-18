import express from "express";

import { validate } from "../middlewares/validate.js";
import { accountSchema, loginSchema } from "../validations/account.schema.js";
import { register, login, getAllAccounts } from "../controllers/account.controller.js";
import { protect } from "../middlewares/auth.middleware.js";
const router = express.Router();

router.get("/", protect, getAllAccounts);

router.post("/register", validate(accountSchema), register);


router.post("/login", validate(loginSchema), login);

export default router;