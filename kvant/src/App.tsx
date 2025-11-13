import { BrowserRouter, Routes, Route } from 'react-router-dom';

import './App.css';
import LoginPage from './Pages/Auth/Login';
import Dashboard from './Pages/Dashboard/Dashboard';
import MainPage from './Pages/MainPage/MainPage';
import RequireAuth from './Routes/RequireAuth';
import { AuthProvider } from './contexts/AuthContext';

function AppContent() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route element={<RequireAuth />}>
        <Route path="/" element={<Dashboard />} />
        <Route path="/forms/:formId" element={<MainPage />} />
      </Route>
    </Routes>
  );
}

function App() {
  return (
    <AuthProvider>
      <BrowserRouter basename="/">
        <AppContent />
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
