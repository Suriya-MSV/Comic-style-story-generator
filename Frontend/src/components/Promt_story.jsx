function PromptStory({ story }) {
  if (!story) return null;

  return (
    <div className="w-full h-44 resize-none rounded-xl bg-zinc-950 border border-zinc-800 p-5 text-sm text-white placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-purple-600">
      {story}
    </div>
  );
}

export default PromptStory;
