import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:5000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      console.log(response.data);
    } catch (error) {
      console.error('Error uploading file', error);
    }
  };

  return (
    <div class="main-header">
      <h1>BallHawk: An American Football Analysis Tool</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} />
        <button type="submit">Upload and Analyze</button>
      </form>
    </div>
  );
}

export default App;
