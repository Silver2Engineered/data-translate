import logo from './logo.png';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <h2>
          Data Translate
        </h2>
        <p>
          Upload a csv to get started!
        </p>
        <input type="file" accept=".csv" />
      </header>
    </div>
  );
}
export default App;
