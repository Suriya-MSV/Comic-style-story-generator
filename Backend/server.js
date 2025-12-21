import express from "express";
import cors from "cors";
import comicRoutes from "./routes/comicRoutes.js";

const app = express();

app.use(cors());
app.use(express.json());

app.use("/api", comicRoutes);

app.listen(5000, () => {
  console.log("Backend running on port 5000");
});

app.get("/", (req, res) => {
  res.send("Backend is running 🚀");
});
