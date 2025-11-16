import { AppProviders } from './providers';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { ResultsPage } from '@/pages/ResultsPage/ResultsPage';
import { ConfigurationPage } from '@/pages/ConfigurationPage/ConfigurationPage';
import { AppLayout } from '@/components/layout/AppLayout';

function App() {
  return (
    <AppProviders>
      <BrowserRouter>
        <Routes>
          <Route element={<AppLayout />}>
            <Route path="/" element={<ResultsPage />} />
            <Route path="/configuracao" element={<ConfigurationPage />} />
            {/* Outras rotas de dashboards podem ser aninhadas aqui no futuro */}
          </Route>
        </Routes>
      </BrowserRouter>
    </AppProviders>
  );
}

export default App;
