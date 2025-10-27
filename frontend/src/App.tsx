import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Layout } from './components/Layout';
import { Home } from './pages/Home';
import { TravelPlanner } from './pages/TravelPlanner';

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/planner" element={<TravelPlanner />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

export default App;
