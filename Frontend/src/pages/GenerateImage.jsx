import { useState } from "react";
import PromptStory from "../components/Promt_story.jsx";
 
function GenerateImage() {
  const [prompt, setPrompt] = useState("");
  const [imageUrl, setImageUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [data , setData] = useState(null);

  const handleGenerate = async () => {
    if (!prompt.trim()) return;

    setLoading(true);
    setError(null);
    setImageUrl(null);

    try {
      const response = await fetch("http://localhost:5000/api/generate-story", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });

      if (!response.ok) throw new Error();

      const data = await response.json();
      setData(data.story);
      
            
      setImageUrl(data.imageUrl);
    } catch {
      setError("Something went wrong while generating the comic.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-zinc-950 text-white flex items-center justify-center px-6">
      {/* Bigger Window */}
      <div className="w-full max-w-5xl bg-zinc-900/70 border border-zinc-800 rounded-2xl p-10 shadow-2xl backdrop-blur">
        {/* Header */}
        <h1 className="text-4xl font-bold text-center mb-3">
          Comic Image Generator
        </h1>
        <p className="text-zinc-400 text-center mb-8">
          Describe your scene and let AI turn it into a comic panel
        </p>

        {/* Prompt */}
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Eg: A superhero leaping between buildings, cinematic comic lighting..."
          className="w-full h-44 resize-none rounded-xl bg-zinc-950 border border-zinc-800 p-5 text-sm text-white placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-purple-600"
        />

        {/* Animated Gradient Button (LEFT → RIGHT text) */}
        <div className="flex justify-center mt-8">
          <button
            onClick={handleGenerate}
            disabled={loading}
            className="
      group relative overflow-hidden
      inline-flex items-center justify-center
      px-20 py-6
      text-xl font-semibold
      text-white
      rounded-xl
      bg-gradient-to-r from-indigo-500 to-purple-500
      hover:from-blue-500 hover:to-pink-500
      transition-all duration-300
      shadow-lg hover:shadow-xl
      min-w-[280px]
      cursor-pointer
      disabled:opacity-50 disabled:cursor-not-allowed
    "
          >
            {/* Default Text → moves RIGHT & vanishes */}
            <span
              className="
        absolute inset-0 flex items-center justify-center w-full
        transition-all duration-300 ease-in-out
        translate-x-0 group-hover:translate-x-full
        whitespace-nowrap
      "
            >
              {loading ? "Creating Comic..." : "Create Comic →"}
            </span>

            {/* Hover Text → comes FROM LEFT to CENTER */}
            <span
              className="
        absolute inset-0 flex items-center justify-center w-full
        transition-all duration-300 ease-in-out
        -translate-x-full group-hover:translate-x-0
        whitespace-nowrap
      "
            >
              {loading ? "Please wait..." : "Let’s Build a Comic 🎨"}
            </span>
          </button>
        </div>

        {/* Error */}
        {error && (
          <p className="mt-6 text-center text-red-400 text-sm">{error}</p>
        )}
         <PromptStory story={data} />

        

        {/* Output */}
        {imageUrl && (
          <div className="mt-12">
            <h2 className="text-xl font-semibold text-center mb-4">
              Generated Comic
            </h2>
            <div className="rounded-xl overflow-hidden border border-zinc-800 bg-zinc-950">
              <img
                src={imageUrl}
                alt="Generated comic"
                className="w-full object-contain"
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default GenerateImage;
