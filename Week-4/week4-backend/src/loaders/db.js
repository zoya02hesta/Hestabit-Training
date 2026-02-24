const mongoose = require('mongoose')
const config = require('../config')
const logger = require('../utils/logger')

const connectDB = async () => {
  try {
    await mongoose.connect(config.mongoURI)
    logger.info('✔ Database connected')
  } catch (error) {
    logger.error('❌ Database connection failed')
    process.exit(1)
  }
}

module.exports = connectDB