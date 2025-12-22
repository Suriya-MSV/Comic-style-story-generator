import axios from "axios";

export const callPythonAPI = async (endpoint, payload = {}, method = "POST", timeoutMs = 1500000) => {
  try {
    const response = await axios({
      url: endpoint,
      method,
      data: payload,
      timeout: timeoutMs
    });

    return response.data;
  } catch (err) {
    if (err.code === "ECONNABORTED") {
      throw new Error(`API request timed out after ${timeoutMs / 1000} seconds`);
    }
    throw err;
  }
};
