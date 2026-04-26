import accountService from "../services/account.service.js";

export const register = async (req, res, next) => {
  try {
    const result = await accountService.register(req.body);
    res.status(201).json({
      success: true,
      message: "Account created",
      data: result,
    });
  } catch (err) {
    res.status(400).json({ success: false, message: err.message });
  }
};

export const login = async (req, res, next) => {
  try {
    const result = await accountService.login(req.body);
    res.json({
      success: true,
      token: result.token,
    });
  } catch (err) {
    res.status(401).json({ success: false, message: err.message });
  }
};

export const getAllAccounts = async (req, res, next) => {
  try {
    const accounts = await accountService.getAllAccounts();

    res.status(200).json({
      success: true,
      data: accounts
    });
  } catch (error) {
    next(error);
  }
};