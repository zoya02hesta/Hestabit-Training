import mongoose from "mongoose";

const orderSchema = new mongoose.Schema(
  {
    account: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'Account',
      required: true
    },
    items: [
      {
        name: String,
        quantity: Number,
        price: Number
      }
    ],
    totalAmount: {
      type: Number,
      required: true,
      min: 0
    },
    status: {
      type: String,
      enum: ['pending', 'completed', 'cancelled'],
      default: 'pending'
    }
  },
  {
    timestamps: true
  }
)

/* Compound index */
orderSchema.index({ status: 1, createdAt: -1 })

/* TTL index example (auto delete after 30 days if cancelled) */
orderSchema.index(
  { createdAt: 1 },
  { expireAfterSeconds: 60 * 60 * 24 * 30 }
)

export default mongoose.model("Order", orderSchema);