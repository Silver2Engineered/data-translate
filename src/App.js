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
        <form action="/submit_file.php">
          <input type="file" accept=".csv"/><br/>
          <label for="pvalue" class="dataType"><pre>P Value: </pre></label>
          <input type="number" id="pvalue" name="pvalue"/>
          <label for="mean" class="dataType"><pre>Mean: </pre></label>
          <input type="number" id="mean" name="mean"/>
          <label for="standard_deviation" class="dataType"><pre>    Standard Deviation: </pre></label>
          <input type="number" id="standardDeviation" name="standardDeviation"/><br/>
          <input type="submit"/>
        </form>
      </header>
    </div>
  );
}
export default App;
