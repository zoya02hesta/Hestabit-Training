import mongoose from "mongoose";

const productSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: true,
      trim: true,
      index: true
    },

    description: {
      type: String,
      trim: true
    },

    price: {
      type: Number,
      required: true,
      min: 0,
      index: true
    },

    tags: {
      type: [String],
      default: []
    },

    deletedAt: {
      type: Date,
      default: null
    }
  },
  { timestamps: true }
);

// Compound index for performance
productSchema.index({ price: 1, createdAt: -1 });

const Product =
  mongoose.models.Product ||
  mongoose.model("Product", productSchema);

export default Product;