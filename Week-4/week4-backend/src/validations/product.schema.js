import Joi from "joi";

export const productSchema = Joi.object({
  name: Joi.string().min(3).max(100).required(),
  description: Joi.string().max(500).required(),
  price: Joi.number().min(0).required(),
  tags: Joi.array().items(Joi.string()).optional(),
});