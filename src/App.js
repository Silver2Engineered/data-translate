import logo from './logo.png';
import './App.css';
import { useState } from 'react';

import InputGroup from './components/InputGroup';
import { stateNames, countyNames } from './utils';

const API_URL = 'http://localhost:5000';

const App = () => {
  const [group, setGroup] = useState('');
  const [file, setFile] = useState();
  const [groups, setGroups] = useState([]);
  const [analysis, setAnalysis] = useState('');

  const handleFileChange = (ev) => {
    const file = ev.target.files[0];
    setFile(file);

    switch (file.name) {
      case 'covid-data.csv':
        setGroups(stateNames);
        setGroup('');
        setAnalysis('');
        break;
      case 'ca_birth_data.csv':
        setGroups(countyNames);
        setGroup('');
        setAnalysis('');
        break;
      default:
        setGroups([]);
        setGroup('');
        setAnalysis('');
    }
  };

  const handleStateChange = (ev) => {
    setGroup(ev.target.value)
    setAnalysis('');
  }

  const handleSubmit = () => {
    if (!file) {
      alert('Please select a file to analyze.');
      return;
    }

    if (!group) {
      alert('Please select a group to analyze.');
      return;
    }

    const formData = new FormData();

    formData.append("data", file);

    fetch(
      `${API_URL}/analyze?group=${group}`,
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

  return (
    <div style={{height: '100vh', overflow: 'auto'}}>
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
          !!file && (
            <InputGroup
              label={'Select a group to analyze'}
              style={{margin: '1em'}}
            >
              <select 
                onChange={handleStateChange} 
                defaultValue={0}
                style={{ padding: '.2em 1em' }}
              >
                <option disabled value={0} />
                {
                  Object.entries(groups).map((tuple) => (
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
          !!file && !!group && (
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
        

        {
          !!file && !!group && !!analysis && (
            <div className="card" style={{ maxWidth: '60em', margin: '0 auto 1em auto', }}>
              <h2>{ `${groups[group]} Analysis` }</h2>
              { 
                analysis.split('\n').map((paragraph, idx) => (
                  <p key={idx} style={{ padding: '0 2em', textAlign: 'left' }}>
                    { paragraph }
                  </p>
                ))
              }
            </div>
          )
        }
        
      </div>

    </div>
  );
}
export default App;
