export const callPythonAPI = async (endpoint, payload = {}, method = "POST") => {
  try {
    const response = await fetch(endpoint, {
      method,
      headers: {
        "Content-Type": "application/json"
      },
      body: method !== "GET" ? JSON.stringify(payload) : undefined
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`API Error ${response.status}: ${errorText}`);
    }

    return await response.json();
  } catch (err) {
    throw err;
  }
};
