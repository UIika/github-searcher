import '../styles/Header.scss';


export default function Header() {
  return (
    <header>
        <img src="/logo-black.svg" alt="logo" width={50} height={50}/>
        <div>
            <h3>GitHub Searcher</h3>
            Search users or repositories below
        </div>
    </header>
  );
}
