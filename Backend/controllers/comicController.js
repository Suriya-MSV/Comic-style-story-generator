import { callPythonAPI } from "../utils/callPythonAPI.js";

// =====================
// 1️⃣ Story Generation
// =====================
export const generateStory = async (req, res) => {
  console.log("✅ FRONTEND HIT THE STORY ENDPOINT");
  console.log("📩 Request body:", req.body);

  try {
    const { prompt } = req.body;
    if (!prompt) {
      return res.status(400).json({ error: "Prompt required" });
    }

    console.log("🟢 Generating story...");
    const story = await callPythonAPI("http://127.0.0.1:8000/generate-story", { prompt });

    console.log("🟢 Story generated:", story);
    res.json({ story });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Story generation failed" });
  }
};

// =====================
// 2️⃣ Image Generation
// =====================
export const generateImage = async (req, res) => {
  console.log("✅ FRONTEND HIT THE IMAGE ENDPOINT");
  console.log("📩 Request body:", req.body);

  try {
    const { story } = req.body;
    if (!story) {
      return res.status(400).json({ error: "Story required to generate images" });
    }

    console.log("🟢 Generating image from story...");
    const imageUrl = await callPythonAPI("python/Image_generator.py", story);

    console.log("🟢 Image generated:", imageUrl);
    res.json({ imageUrl });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Image generation failed" });
  }
};
