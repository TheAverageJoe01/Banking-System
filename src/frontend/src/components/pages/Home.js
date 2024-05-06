import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
function Home() {
  const navigate = useNavigate();
  const [username, setUser] = useState(null);
  const [id, setId] = useState(null);

  useEffect(() => {
    const verifyToken = async () => {
      const token = localStorage.getItem('token');
        console.log(token)
      try {
        const response = await fetch(`http://localhost:8000/verify-token/${token}`);

        if (!response.ok) {
          throw new Error('Token verification failed');
        }
        const { username, id } = await response.json();

        console.log('Username:', username);
        console.log('ID:', id);
        
        // Update the user state or perform other actions with the user information
        setUser(username);
        setId(id);
        
      } catch (error) {
        localStorage.removeItem('token');
        navigate('/');
      }
    };

    verifyToken();
  }, [navigate]);

  return (
    <div className="d-flex justify-content-center align-items-center vh-100">
      <h1>WELCOME TO THE BANKING APP {username}!</h1>

    </div>
  )
}

export default Home;
