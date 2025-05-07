import { useEffect, useState } from 'react';
import './styles/App.scss';
import SearchBar from './components/SearchBar';
import ResultGrid from './components/Grid';
import Header from './components/Header';

interface SearchResult {
  id: number;
  [key: string]: any;
}

function App() {
  const [query, setQuery] = useState('');
  const [type, setType] = useState<'users' | 'repositories'>('users');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchResults = async () => {
      if (query.length < 3) {
        setResults([]);
        return;
      }
      setLoading(true);
      setError(null);
      try {
        const res = await fetch('http://localhost:8000/api/search', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query, type })
        });
        const data = await res.json();
        setResults(data.items || []);
      } catch (err) {
        setError('Error fetching data');
      } finally {
        setLoading(false);
      }
    };

    const debounce = setTimeout(fetchResults, 500);
    return () => clearTimeout(debounce);
  }, [query, type]);

  return (
    <div className="App">
      <div className="containter">
        <Header />
        <SearchBar query={query} setQuery={setQuery} type={type} setType={setType} />
      </div>
      {loading && <p>Loading...</p>}
      {error && <p className="error">{error}</p>}
      <ResultGrid results={results} type={type} />
    </div>
  );
}

export default App;
