function PromptStory({
  story,
  onRegenerate,
  onGenerateComic,
  loadingComic,
}) {
  if (!story) return null;

  const text = String(story).replace(/\.\s+/g, ".\n");

  return (
    <div className="mt-6 w-full relative">
      {/* Story Box */}
      <div
        className={`
          relative
          w-full
          overflow-hidden
          rounded-2xl
          bg-gradient-to-br from-zinc-950 via-zinc-900 to-zinc-950
          border border-zinc-800
          p-6
          text-base
          md:text-lg
          text-white
          font-serif
          leading-relaxed
          tracking-wide
          whitespace-pre-wrap
          shadow-lg
        `}
      >
        {text}

        {/* 🔥 Gradient Loading Overlay */}
        {loadingComic && (
          <div
            className="
              absolute inset-0
              bg-gradient-to-b
              from-purple-600/30
              via-indigo-600/40
              to-pink-600/30
              animate-gradient-sweep
            "
          />
        )}
      </div>

      {/* Buttons */}
      <div className="mt-6 flex justify-between items-center gap-4">
        {/* Regenerate */}
        <button
          onClick={onRegenerate}
          disabled={loadingComic}
          className="
            px-6 py-3
            rounded-xl
            border border-zinc-700
            bg-zinc-900
            text-white
            font-medium
            hover:bg-zinc-800
            hover:border-purple-500
            transition-all
            shadow-md
            disabled:opacity-50
          "
        >
          ⟳ Regenerate
        </button>

        {/* Generate Comic */}
        <button
          onClick={onGenerateComic}
          disabled={loadingComic}
          className="
            px-8 py-3
            rounded-xl
            bg-gradient-to-r from-purple-600 to-indigo-600
            text-white
            font-semibold
            hover:from-purple-500 hover:to-indigo-500
            transition-all
            shadow-lg
            disabled:opacity-70
          "
        >
          OK, Generate Comic 🎨
        </button>
      </div>
    </div>
  );
}

export default PromptStory;
