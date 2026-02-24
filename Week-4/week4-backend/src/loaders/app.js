const express = require('express')
const config = require('../config')
const logger = require('../utils/logger')
const connectDB = require('./db')

const app = express()

const loadApp = async () => {
  // 1. Connect DB
  await connectDB()

  // 2. Middlewares
  app.use(express.json())
  logger.info('✔ Middlewares loaded')

  // 3. Routes
  app.get('/health', (req, res) => {
    res.json({ status: 'OK' })
  })

  logger.info('✔ Routes mounted: 1 endpoint')

  // 4. Start server
  const server = app.listen(config.port, () => {
    logger.info(`✔ Server started on port ${config.port}`)
  })

  // 5. Graceful shutdown
  process.on('SIGTERM', () => {
    logger.info('SIGTERM received. Shutting down...')
    server.close(() => {
      logger.info('Server closed')
      process.exit(0)
    })
  })
}

module.exports = loadApp