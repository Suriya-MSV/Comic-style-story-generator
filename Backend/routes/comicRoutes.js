import express from "express";
import { generateStory } from "../controllers/comicController.js";

const router = express.Router();

router.post("/generate-story", generateStory);

export default router;
