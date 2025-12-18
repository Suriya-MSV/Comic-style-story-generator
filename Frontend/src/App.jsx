import { BrowserRouter, Routes, Route } from "react-router-dom";
import Header from "./components/Header.jsx";
import Footer from "./components/Footer.jsx";
import EntryPage from "./pages/EntryPage";
import About from './pages/About';
import GenerateImage from "./pages/GenerateImage.jsx";

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen flex flex-col">
        <Header />

        <Routes>
          <Route path="/" element={<EntryPage />} />
          <Route path="/about" element={<About />} />
          <Route path="/generate" element={<GenerateImage />} />
        </Routes>

        <Footer />
      </div>
    </BrowserRouter>
  );
}

export default App;
