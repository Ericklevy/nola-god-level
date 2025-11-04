import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import './index.css'; // O CSS global que arrumamos

// Importe o Layout e todas as páginas
import Layout from './components/layout/Layout';
import Dashboard from './pages/Dashboard';
import Products from './pages/Products';
import Channels from './pages/Channels';
import Stores from './pages/Stores';
import TimeAnalysis from './pages/TimeAnalysis';
import Customers from "./pages/Customers";


// Define as rotas
const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />, // O Layout é o "pai" de todas as páginas
    children: [
      {
        index: true, // Rota / (raiz)
        element: <Dashboard />,
      },
      {
        path: 'produtos',
        element: <Products />,
      },
      {
        path: 'canais',
        element: <Channels />,
      },
      {
        path: 'lojas',
        element: <Stores />,
      },
      {
        path: 'temporal',
        element: <TimeAnalysis />,
      },
      {
        path: 'clientes',
        element: <Customers />,
      },
    ],
  },
]);

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>
);