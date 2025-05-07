import '../styles/Grid.scss';

interface Props {
  results: any[];
  type: 'users' | 'repositories';
}

export default function Grid({ results, type }: Props) {
  if (results.length === 0) return null;

  return (
    <div className="grid">
      {results.map(item => (
        <div key={item.id} className="card">
          {type === 'users' ? (
            <>
              <img src={item.avatar_url} alt={item.login} />
              <h3>{item.login}</h3>
              <a href={item.html_url} target="_blank">View Profile</a>
            </>
          ) : (
            <>
              <h3>{item.name}</h3>
              <p>{item.description}</p>
              <p>
                ⭐ {item.stargazers_count} | 🧑‍💻 {item.owner?.login}
              </p>
              <a href={item.html_url} target="_blank">View Repo</a>
            </>
          )}
        </div>
      ))}
    </div>
  );
}