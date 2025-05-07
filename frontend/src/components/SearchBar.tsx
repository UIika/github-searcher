import '../styles/SearchBar.scss';

interface Props {
  query: string;
  setQuery: (q: string) => void;
  type: 'users' | 'repositories';
  setType: (t: 'users' | 'repositories') => void;
}

export default function SearchBar({ query, setQuery, type, setType }: Props) {
  return (
    <div className="search-bar">
      <input
        type="text"
        placeholder="Start typing to search..."
        value={query}
        onChange={e => setQuery(e.target.value)}
      />
      <select value={type} onChange={e => setType(e.target.value as 'users' | 'repositories')}>
        <option value="users">Users</option>
        <option value="repositories">Repositories</option>
      </select>
    </div>
  );
}