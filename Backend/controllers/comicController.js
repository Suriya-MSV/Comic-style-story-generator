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
    const story = await callPythonAPI("http://127.0.0.1:8000/generate-story", {
      prompt,
    });

    console.log("🟢 Story generated:", story);
    res.json({ "story": story.story });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Story generation failed" });
  }
};

// =====================
// 2️⃣ Image Generation
// =====================
export const generateComic = async (req, res) => {
  console.log("✅ FRONTEND HIT THE IMAGE ENDPOINT");
  console.log("📩 Request body:", req.body);

  try {
    const { story } = req.body;

    if (!story) {
      return res.status(400).json({ error: "Story required" });
    }

    const pythonResponse = await callPythonAPI(
      "http://127.0.0.1:8000/generate-comic",
      { story }
    );

    console.log("🐍 Python response:", pythonResponse);

    // 👇 extract actual URL
    const imageUrl =
      pythonResponse.imageUrl || pythonResponse.image_url;

    if (!imageUrl) {
      throw new Error("No image URL returned from Python");
    }

    res.json({ imageUrl });
  } catch (err) {
    console.error("❌ Image generation failed:", err);
    res.status(500).json({ error: "Image generation failed" });
  }
};

