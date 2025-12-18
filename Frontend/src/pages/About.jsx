// About.jsx (updated)
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import creator1 from "../assets/Suriyavel.jpg";
import creator2 from "../assets/Vignesh.jpg";
import exampleImage1 from "../../public/example1.png";
import exampleImage2 from "../../public/example2.png";
import CoT from "../../public/cot.png";
import ComfyUI from "../../public/comfyui.png";
import GeminiAI from "../../public/geminiAI.png";

function About() {
  const navigate = useNavigate();
  const [currentImage, setCurrentImage] = useState(0);
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [selectedImageIndex, setSelectedImageIndex] = useState(null);
  const [creatorModalOpen, setCreatorModalOpen] = useState(false);
  const [selectedCreator, setSelectedCreator] = useState(null);

  const images = [
    {
      src: CoT,
      alt: "Chain of Thought Structure for Story Building",
    },
    {
      src: ComfyUI,
      alt: "ComfyUI Interface for Image Generation",
    },
    {
      src: GeminiAI,
      alt: "Google Gemini AI for Story and Dialogue Creation",
    },
    {
      src: exampleImage1,
      alt: "Example of Generated Comic Story Panel 1",
    },
    {
      src: exampleImage2,
      alt: "Example of Generated Comic Story Panel 2",
    },
  ];

  const creators = [
    {
      name: "Suriyavel",
      src: creator1,
      fullSrc: creator1,
      github: "https://github.com/Suriya-MSV",
      linkedin: "https://www.linkedin.com/in/suriyavel-mariappan-211363277/"
    },
    {
      name: "Vignesh",
      src: creator2,
      fullSrc: creator2,
      github: "https://github.com/Vigneshv-2002",
      linkedin: "https://www.linkedin.com/in/vigneshv175 "
    },
  ];

  const openModal = (index) => {
    setSelectedImageIndex(index);
    setModalIsOpen(true);
  };

  const closeModal = () => {
    setModalIsOpen(false);
    setSelectedImageIndex(null);
  };

  const openCreatorModal = (creator) => {
    setSelectedCreator(creator);
    setCreatorModalOpen(true);
  };

  const closeCreatorModal = () => {
    setCreatorModalOpen(false);
    setSelectedCreator(null);
  };

  return (
    <>
      <div className="min-h-screen bg-zinc-950 px-6 py-20">
        <div className="max-w-7xl mx-auto w-full flex flex-col md:flex-row gap-8 items-start">
          {/* Left Content - 60% */}
          <div className="flex-1 basis-3/5 bg-zinc-900 border border-zinc-800 rounded-2xl shadow-xl p-10">
            {/* Title */}
            <h1 className="text-4xl md:text-5xl font-bold text-zinc-100 mb-6">
              About AI Comic Generator
            </h1>

            {/* Subtitle */}
            <p className="text-lg text-zinc-400 leading-relaxed mb-10">
              This app uses advanced AI to turn your creative ideas into
              engaging comic strips. Built with React, Vite, and Tailwind CSS
              for a seamless experience.
            </p>

            {/* How it Works Section */}
            <div className="mb-10">
              <h2 className="text-2xl font-semibold text-zinc-100 mb-4">
                How It Works
              </h2>
              <ul className="text-zinc-300 space-y-3 list-disc list-inside">
                <li>
                  <strong>Chain of Thoughts Structure:</strong> We use a
                  chain-of-thoughts-like structure to build the story and
                  dialogues, ensuring coherent and engaging narratives.
                </li>
                <li>
                  <strong>ComfyUI with LoRA:</strong> Images are generated using
                  ComfyUI integrated with LoRA models specifically trained for
                  comic-style visuals, creating high-quality panels.
                </li>
                <li>
                  <strong>Gemini AI:</strong> Google's Gemini is leveraged to
                  create and structure the story outlines and dialogues,
                  providing creative and contextually rich content.
                </li>
              </ul>
            </div>

            {/* Built By Section */}
            <div className="mb-10">
              <h2 className="text-2xl font-semibold text-zinc-100 mb-4">
                Built By
              </h2>
              <div className="flex flex-col sm:flex-row gap-6 items-center mb-4">
                <div
                  className="text-center cursor-pointer"
                  onClick={() => openCreatorModal(creators[0])}
                >
                  <img
                    src={creators[0].src}
                    alt="Creator Photo"
                    className="w-24 h-24 rounded-full mx-auto mb-2 object-cover hover:opacity-80 transition-opacity"
                  />
                  <p className="text-zinc-300 font-medium">You</p>
                </div>
                <div
                  className="text-center cursor-pointer"
                  onClick={() => openCreatorModal(creators[1])}
                >
                  <img
                    src={creators[1].src}
                    alt="Vignesh Photo"
                    className="w-24 h-24 rounded-full mx-auto mb-2 object-cover hover:opacity-80 transition-opacity"
                  />
                  <p className="text-zinc-300 font-medium">Vignesh</p>
                </div>
              </div>
            </div>

            {/* CTA Button */}
            <button
              onClick={() => navigate("/")}
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
                Back to Home →
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
                Start Creating 🎨
              </span>
            </button>
          </div>

          {/* Right Carousel - 40% */}
          <div className="flex-1 basis-2/5 relative">
            <h3 className="text-xl font-semibold text-zinc-100 mb-4 text-center">
              Tools & Examples
            </h3>
            <div
              className="relative w-full h-[32rem] rounded-2xl shadow-xl overflow-hidden mb-4 cursor-pointer"
              onClick={() => openModal(currentImage)}
            >
              <img
                src={images[currentImage].src}
                alt={images[currentImage].alt}
                className="w-full h-full object-contain bg-black"
              />
              {/* Navigation Buttons */}
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  setCurrentImage((prev) =>
                    prev > 0 ? prev - 1 : images.length - 1
                  );
                }}
                className="absolute left-2 top-1/2 -translate-y-1/2 bg-black/50 text-white p-2 rounded-full hover:bg-black/70 transition-colors"
              >
                ‹
              </button>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  setCurrentImage((prev) =>
                    prev < images.length - 1 ? prev + 1 : 0
                  );
                }}
                className="absolute right-2 top-1/2 -translate-y-1/2 bg-black/50 text-white p-2 rounded-full hover:bg-black/70 transition-colors"
              >
                ›
              </button>
            </div>
            {/* Indicator Dots */}
            <div className="flex justify-center space-x-2">
              {images.map((_, index) => (
                <button
                  key={index}
                  onClick={() => setCurrentImage(index)}
                  className={`w-3 h-3 rounded-full transition-colors ${
                    index === currentImage
                      ? "bg-indigo-500"
                      : "bg-zinc-500 hover:bg-zinc-400"
                  }`}
                />
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Image Modal */}
      {modalIsOpen && selectedImageIndex !== null && (
        <div
          className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4"
          onClick={closeModal}
        >
          <div
            className="relative bg-zinc-900 rounded-2xl p-6 max-w-4xl w-full max-h-[90vh] flex flex-col items-center"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Close Button */}
            <button
              onClick={closeModal}
              className="absolute top-4 right-4 text-white text-2xl hover:text-zinc-300 transition-colors"
            >
              ×
            </button>

            {/* Enlarged Image */}
            <img
              src={images[selectedImageIndex].src}
              alt={images[selectedImageIndex].alt}
              className="w-full max-h-[70vh] object-contain rounded-lg mb-6"
            />

            {/* Buttons */}
            <div className="flex gap-4">
              <a
                href="https://github.com/yourusername/comic-story-generator"
                target="_blank"
                rel="noopener noreferrer"
                className="bg-gradient-to-r from-indigo-500 to-purple-500 text-white px-8 py-3 rounded-xl hover:from-indigo-600 hover:to-purple-600 transition-all duration-300 text-sm font-semibold"
              >
                GitHub
              </a>
              <a
                href="https://linkedin.com/in/yourprofile"
                target="_blank"
                rel="noopener noreferrer"
                className="bg-gradient-to-r from-blue-500 to-blue-600 text-white px-8 py-3 rounded-xl hover:from-blue-600 hover:to-blue-700 transition-all duration-300 text-sm font-semibold"
              >
                LinkedIn
              </a>
            </div>
          </div>
        </div>
      )}

      {/* Creator Modal */}
      {creatorModalOpen && selectedCreator && (
        <div
          className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4"
          onClick={closeCreatorModal}
        >
          <div
            className="relative bg-zinc-900 rounded-2xl p-6 max-w-md w-full max-h-[90vh] flex flex-col items-center"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Close Button */}
            <button
              onClick={closeCreatorModal}
              className="absolute top-4 right-4 text-white text-2xl hover:text-zinc-300 transition-colors"
            >
              ×
            </button>

            {/* Enlarged Image */}
            <img
              src={selectedCreator.fullSrc}
              alt={`${selectedCreator.name} Photo`}
              className="w-64 h-64 rounded-full mb-4 object-cover"
            />

            {/* Name */}
            <h3 className="text-2xl font-semibold text-zinc-100 mb-6">
              {selectedCreator.name}
            </h3>

            {/* Social Buttons */}
            <div className="flex gap-4">
              <a
                href={selectedCreator.github}
                target="_blank"
                rel="noopener noreferrer"
                className="
      px-6 py-3 rounded-xl
      bg-gradient-to-r from-zinc-700 to-zinc-800
      hover:from-zinc-600 hover:to-zinc-700
      text-white font-semibold text-sm
      transition-all duration-300
    "
              >
                GitHub
              </a>

              <a
                href={selectedCreator.linkedin}
                target="_blank"
                rel="noopener noreferrer"
                className="
      px-6 py-3 rounded-xl
      bg-gradient-to-r from-blue-500 to-blue-600
      hover:from-blue-600 hover:to-blue-700
      text-white font-semibold text-sm
      transition-all duration-300
    "
              >
                LinkedIn
              </a>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default About;
