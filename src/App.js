import logo from './logo.png';
import './App.css';
import { useState } from 'react';

import InputGroup from './components/InputGroup';
import { stateNames } from './utils/states';

const API_URL = 'http://localhost:5000';

const App = () => {
  const [state, setState] = useState('');
  const [file, setFile] = useState();
  const [analysis, setAnalysis] = useState('');

  const handleFileChange = (ev) => (
    setFile(ev.target.files[0])
  );

  const handleStateChange = (ev) => (
    setState(ev.target.value)
  );

  const handleSubmit = () => {
    if (!file) {
      alert('Please select a file to analyze.');
      return;
    }

    if (!state) {
      alert('Please select a state to analyze.');
      return;
    }

    const formData = new FormData();

    formData.append("data", file);

    fetch(
      `${API_URL}/analyze?state=${state}`,
      {
        method: 'POST',
        body: formData
      }
    )
      .then(res => res.json())
      .then(body => {
        if (body['error']) {
          console.log(body['error']);
          return;
        }

        setAnalysis(body['analysis'])
      });
  }

  console.log(file);

  return (
    <div 
      style={{ 
        minHeight: '100vh',
        textAlign: 'center', 
        color: 'white',
        backgroundColor: '#282c34',
        padding: '0 0 2em 0',
      }}
    >
      <header className="App-header">
        <img 
          src={logo}
          alt="logo"
          style={{ height: '40vmin', pointerEvents: 'none' }}
        />
      </header>

      <div 
        style={{
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
        }}
      >

        <InputGroup
          label={'Upload a csv to get started'}
          style={{ margin: '1em' }}
        >
          <input 
            type="file" 
            accept=".csv"
            onChange={handleFileChange}
            style={{ width: 'fit-content' }}
          />
        </InputGroup>

        {
          file && (
            <InputGroup
              label={'Select a state to analyze'}
              style={{margin: '1em'}}
            >
              <select 
                onChange={handleStateChange} 
                defaultValue={0}
                style={{ padding: '.2em 1em' }}
              >
                <option disabled value={0} />
                {
                  Object.entries(stateNames).map((tuple) => (
                    <option value={tuple[0]} key={tuple[0]}>
                      { tuple[1] }
                    </option>
                  ))
                }
              </select>
            </InputGroup>
          )
        }
        

        {
          file && state && (
            <div>
              <button 
                onClick={handleSubmit}
                style={{
                  margin: '2em',
                  border: '2px solid white',
                  borderRadius: '15px',
                  color: "white",
                  padding: ".5em 2em",
                  fontWeight: 'bold',
                  fontSize: 'large',
                }}
                className='btn-submit'
              >
                Analyze
              </button>
            </div>
          )
        }
        

        <div>
          { 
            analysis.split('\n').map(paragraph => (
              <p style={{ padding: '0 2em' }}>
                { paragraph }
              </p>
            ))
          }
        </div>
      </div>

    </div>
  );
}
export default App;
