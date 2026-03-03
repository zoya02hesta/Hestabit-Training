import express from "express";
import {
  getProducts,
  getProductById,
  createProduct,
  updateProduct,
  deleteProduct
} from "../controllers/product.controller.js";
import { validate } from "../middlewares/validate.js";
import { productSchema } from "../validations/product.schema.js";

const router = express.Router();

router.post("/", validate(productSchema), createProduct);
router.put("/:id", validate(productSchema), updateProduct);



router.post("/", createProduct);
router.get("/", getProducts);
router.get("/:id", getProductById);
router.put("/:id", updateProduct);
router.delete("/:id", deleteProduct);

export default router;