import { Routes, Route, Link } from 'react-router-dom';
import Home from './components/Home.jsx';
import About from './components/About.jsx';
import ChooseExercise from './components/ChooseExecrise.jsx';
import Navigation from "./components/Navigation";
import LayoutWithNavigation from "./components/LayoutWithNavigation";
import Routine from './components/Routine.jsx';
import Calories from './components/Calories.jsx';
import Weather from './components/Weather.jsx';



function App() {
  return (
    <Routes>
      {/* Public routes: No Navigation */}
      <Route path="/" element={<Home />} />
      <Route path="/about" element={<About />} />
      <Route path="/choose-exercise" element={<ChooseExercise />} />

      {/* Private routes: With Navigation */}
      <Route element={<LayoutWithNavigation />}>
        <Route path="/routine" element={<Routine />} />
        <Route path="/weather" element={<Weather />} />
        <Route path="/calories" element={<Calories />} />
      </Route>
    </Routes>
  );
}

export default App;
