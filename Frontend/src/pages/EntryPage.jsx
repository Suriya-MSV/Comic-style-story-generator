import { useNavigate } from "react-router-dom";

function EntryPage() {
  const navigate = useNavigate();

  return (
    <div className="flex flex-1 items-center justify-center bg-zinc-950 px-6">
      {/* Card */}
      <div
        className="
        max-w-3xl w-full
        bg-zinc-900
        border border-zinc-800
        rounded-2xl
        shadow-xl
        p-10
        text-center
      "
      >
        {/* Title */}
        <h1 className="text-4xl md:text-5xl font-bold text-zinc-100 mb-6">
          AI Comic Generator 🎨
        </h1>

        {/* Subtitle */}
        <p className="text-lg text-zinc-400 leading-relaxed mb-10">
          Transform your ideas into stunning comic stories using AI. Describe a
          scene, choose a style, and generate comic panels with dialogues in
          seconds.
        </p>

        {/* CTA Button */}
        <button
          onClick={() => navigate("/generate")}
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
            shadow-lg
            hover:shadow-xl
            min-w-[280px]
            cursor-pointer
          "
        >
          {/* Default Text */}
          <span
            className="
              absolute inset-0 flex items-center justify-center w-full
              transition-all duration-300 ease-in-out
              translate-x-0 group-hover:-translate-x-full
              whitespace-nowrap
            "
          >
            Start Creating →
          </span>

          {/* Hover Text */}
          <span
            className="
              absolute inset-0 flex items-center justify-center w-full
              transition-all duration-300 ease-in-out
              translate-x-full group-hover:translate-x-0
              whitespace-nowrap
            "
          >
            Let’s Build a Comic 🎨
          </span>
        </button>
      </div>
    </div>
  );
}

export default EntryPage;