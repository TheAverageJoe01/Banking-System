import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
function Home() {
  const navigate = useNavigate();

  useEffect(() => {
    const verifyToken = async () => {
      const token = localStorage.getItem('token');
        console.log(token)
      try {
        const response = await fetch(`http://localhost:8000/verify-token/${token}`);

        if (!response.ok) {
          throw new Error('Token verification failed');
        }
      } catch (error) {
        localStorage.removeItem('token');
        navigate('/');
      }
    };

    verifyToken();
  }, [navigate]);

  return (
    <div className="d-flex justify-content-center align-items-center vh-100">
      <h1>WELCOME TO THE HOME PAGE THank you for logging in</h1>
    </div>
  )
}

export default Home;
