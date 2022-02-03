import logo from './logo.png';
import './App.css';
import { useState } from 'react';

const API_URL = 'http://localhost:5000'

const state_names = {
  'AK': 'Alaska',
  'AL': 'Alabama',
  'AR': 'Arkansas',
  'AS': 'American Samoa',
  'AZ': 'Arizona',
  'CA': 'California',
  'CO': 'Colorado',
  'CT': 'Connecticut',
  'DC': 'District of Columbia',
  'DE': 'Delaware',
  'FL': 'Florida',
  'GA': 'Georgia',
  'GU': 'Guam',
  'HI': 'Hawaii',
  'IA': 'Iowa',
  'ID': 'Idaho',
  'IL': 'Illinois',
  'IN': 'Indiana',
  'KS': 'Kansas',
  'KY': 'Kentucky',
  'LA': 'Louisiana',
  'MA': 'Massachusetts',
  'MD': 'Maryland',
  'ME': 'Maine',
  'MI': 'Michigan',
  'MN': 'Minnesota',
  'MO': 'Missouri',
  'MP': 'Northern Mariana Islands',
  'MS': 'Mississippi',
  'MT': 'Montana',
  'NA': 'National',
  'NC': 'North Carolina',
  'ND': 'North Dakota',
  'NE': 'Nebraska',
  'NH': 'New Hampshire',
  'NJ': 'New Jersey',
  'NM': 'New Mexico',
  'NV': 'Nevada',
  'NY': 'New York',
  'OH': 'Ohio',
  'OK': 'Oklahoma',
  'OR': 'Oregon',
  'PA': 'Pennsylvania',
  'PR': 'Puerto Rico',
  'RI': 'Rhode Island',
  'SC': 'South Carolina',
  'SD': 'South Dakota',
  'TN': 'Tennessee',
  'TX': 'Texas',
  'UT': 'Utah',
  'VA': 'Virginia',
  'VI': 'Virgin Islands',
  'VT': 'Vermont',
  'WA': 'Washington',
  'WI': 'Wisconsin',
  'WV': 'West Virginia',
  'WY': 'Wyoming'
}

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

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />

        <p>
          Upload a csv to get started!
        </p>
        <input type="file" accept=".csv" onChange={handleFileChange}/>
        
        <label >
          Select a state to analyze
        </label>
        <select onChange={handleStateChange}>
          <option disabled selected value />
          {
            Object.entries(state_names).map((tuple) => (
              <option value={tuple[0]}>
                { tuple[1] }
              </option>
            ))
          }
        </select>

        <button onClick={handleSubmit}>
          Submit
        </button>

        <p style={{ padding: '0 2em' }}>
          { analysis }
        </p>
      </header>
    </div>
  );
}
export default App;
