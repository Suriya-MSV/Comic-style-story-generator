import express from "express";
import { generateStory ,generateComic} from "../controllers/comicController.js";

const router = express.Router();

router.post("/generate-story", generateStory);
router.post("/generate-comic", generateComic);

export default router;
