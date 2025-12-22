import { useState } from "react";
import PromptStory from "../components/PromtStory.jsx";

function GenerateImage() {
  const [prompt, setPrompt] = useState("");        // user input
  const [originalPrompt, setOriginalPrompt] = useState(""); // store last submitted prompt
  const [imageUrl, setImageUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [data , setData] = useState(null);

  // Main generate (first time or regenerate)
  const handleGenerate = async (customPrompt) => {
    const promptToSend = customPrompt || prompt;
    if (!promptToSend.trim()) return;

    setLoading(true);
    setError(null);
    setImageUrl(null);

    try {
      const response = await fetch("http://localhost:5000/api/generate-story", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: promptToSend }),
      });

      if (!response.ok) throw new Error("Story API failed");

      const result = await response.json();

      setData(result.story);          // ✅ FIXED
      setOriginalPrompt(promptToSend);

      console.log("Story received:", result.story);

    } catch (err) {
      console.error(err);
      setError("Something went wrong while generating the story.");
    } finally {
      setLoading(false);
    }
  };

  // Regenerate: append extra text to previous prompt
  const handleRegenerate = () => {
    const appendedPrompt = originalPrompt + "\n\nRegenerate the story with more dramatic details.";
    handleGenerate(appendedPrompt);
  };

  const handleGenerateComic = async () => {
    if (!data) return;

    setLoading(true);
    setError(null);

    try {
      const response = await fetch("http://localhost:5000/api/generate-comic", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ story: data }), // send the last story
      });

      if (!response.ok) throw new Error();

      const result = await response.json();
      setImageUrl(result.imageUrl); // replace old image with final comic image

    } catch {
      setError("Something went wrong while generating the comic image.");
    } finally {
      setLoading(false);
    }
  };


  return (
    <div className="min-h-screen bg-zinc-950 text-white flex items-center justify-center px-6">
      <div className="w-full max-w-5xl bg-zinc-900/70 border border-zinc-800 rounded-2xl p-10 shadow-2xl backdrop-blur">
        <h1 className="text-4xl font-bold text-center mb-3">Comic Image Generator</h1>
        <p className="text-zinc-400 text-center mb-8">
          Describe your scene and let AI turn it into a comic panel
        </p>

        {/* Prompt input only if no story yet */}
        {!data && (
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Eg: A superhero leaping between buildings, cinematic comic lighting..."
            className="w-full h-44 resize-none rounded-xl bg-zinc-950 border border-zinc-800 p-5 text-sm text-white placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-purple-600"
          />
        )}

        {/* Generate button only if no story */}
        {!data && (
          <div className="flex justify-center mt-8">
            <button
              onClick={() => handleGenerate()}
              disabled={loading}
              className="group relative overflow-hidden inline-flex items-center justify-center px-20 py-6 text-xl font-semibold text-white rounded-xl bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-blue-500 hover:to-pink-500 transition-all duration-300 shadow-lg hover:shadow-xl min-w-[280px] cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span className="absolute inset-0 flex items-center justify-center w-full transition-all duration-300 translate-x-0 group-hover:translate-x-full">
                {loading ? "Creating Comic..." : "Create Comic →"}
              </span>
              <span className="absolute inset-0 flex items-center justify-center w-full transition-all duration-300 -translate-x-full group-hover:translate-x-0">
                {loading ? "Please wait..." : "Let’s Build a Comic 🎨"}
              </span>
            </button>
          </div>
        )}

        {error && <p className="mt-6 text-center text-red-400 text-sm">{error}</p>}

        {/* Story component */}
        {data && (
          <PromptStory
            story={data}
            onRegenerate={handleRegenerate}
            onGenerateComic={handleGenerateComic} // you can regenerate exact comic
            loadingComic={loading}
          />
        )}

        {/* Generated Image */}
        {imageUrl && (
          <div className="mt-12">
            <h2 className="text-xl font-semibold text-center mb-4">Generated Comic</h2>
            <div className="rounded-xl overflow-hidden border border-zinc-800 bg-zinc-950">
              <img src={imageUrl} alt="Generated comic" className="w-full object-contain" />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default GenerateImage;
