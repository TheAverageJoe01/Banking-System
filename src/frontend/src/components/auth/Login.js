import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';

function Login() {
  // State variables for username, name, password, error message, loading state, and modal visibility
  const [username, setUsername] = useState('');
  const [name, setName] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [show, setShow] = useState(false);

  // Functions to handle modal 
  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  // Navigation function
  const navigate = useNavigate();

  // Form validation function for login
  const validateForm = () => {
    // Check if username and password are not empty
    if (!username || !password) {
      setError('Username and password are required');
      return false;
    }
    setError('');
    return true;
  };

  // Form validation function for user creation
  const validateCreateForm = () => {
    if (!name || !username || !password) {
      setError('Username and password are required');
      return false;
    }
    setError('');
    return true;
  };

  // Function to handle login form submission
  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!validateForm()) return;
    setLoading(true);

    // Create form data
    const formDetails = new URLSearchParams();
    formDetails.append('username', username);
    formDetails.append('password', password);

    // Send login request to the server
    try {
      const response = await fetch('http://localhost:8000/token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formDetails,
      });

      setLoading(false);

      // Handle response
      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('token', data.access_token);
        navigate('/home');
      } else {
        // Handle error
        const errorData = await response.json();
        setError(errorData.detail || 'Authentication failed!');
      }
    } catch (error) {
      setLoading(false);
      setError('An error occurred. Please try again later.');
    }
  };

  // Function to handle user creation form submission
  const handleCreateUser = async (event) => {
    event.preventDefault();
    if (!validateCreateForm()) return;
    setLoading(true);

    // Create user data
    const userData = {
      name: name,
      email: username,
      password: password
    };

    try {
      // Send user creation request to the server
      const response = await fetch('http://localhost:8000/users/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      setLoading(false);

      if (response.ok) {
        window.location.reload();
      }
    } catch (error) {
      // Handle error
      console.error("Error:", error);
      setLoading(false);
      setError('An error occurred. Please try again later.');
    }
  };

  return (
    <div>
      <Container className="d-flex vh-100 justify-content-center align-items-center">
        <Form onSubmit={handleSubmit}>
          <h1 className='d-flex justify-content-center'>Welcome to Big Bank</h1>
          {/* Login Form */}
          <Form.Group className="mb-3" controlId="formBasicUsername">
            <Form.Label>Username</Form.Label>
            <Form.Control type="username" placeholder="Enter username" value={username}
              onChange={(e) => setUsername(e.target.value)} />
            <Form.Text className="text-muted">
            </Form.Text>
          </Form.Group>

          <Form.Group className="mb-3" controlId="formBasicPassword">
            <Form.Label>Password</Form.Label>
            <Form.Control type="password" placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)} />
          </Form.Group>

          <Container className='d-flex justify-content-between'>
            <Button variant="success" type="submit" disabled={loading}>
              {loading ? 'Logging in...' : 'Login'}
            </Button>

            <Button variant="success" onClick={handleShow} disabled={loading}>
              Create User
            </Button>
          </Container>
          {/* User Creation Modal */}
          {error && <p style={{ color: 'red' }}>{error}</p>}
          <Modal show={show} onHide={handleClose}>
            <Modal.Header closeButton>
              <Modal.Title>Create User</Modal.Title>
            </Modal.Header>
            <Modal.Body>
              <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3" controlId="formBasicName">
                  <Form.Label>Name</Form.Label>
                  <Form.Control type="username" placeholder="Enter Name" value={name}
                    onChange={(e) => setName(e.target.value)} />
                  <Form.Text className="text-muted">
                  </Form.Text>
                </Form.Group>

                <Form.Group className="mb-3" controlId="formBasicEmail">
                  <Form.Label>Email</Form.Label>
                  <Form.Control type="email" placeholder="Enter Email" value={username}
                    onChange={(e) => setUsername(e.target.value)} />
                  <Form.Text className="text-muted">
                  </Form.Text>
                </Form.Group>

                <Form.Group className="mb-3" controlId="formBasicPassword">
                  <Form.Label>Password</Form.Label>
                  <Form.Control type="password" placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)} />
                </Form.Group>
              </Form>
              {error && <p style={{ color: 'red' }}>{error}</p>}
            </Modal.Body>
            <Modal.Footer>
              <Button variant="secondary" onClick={handleClose}>
                Close
              </Button>
              <Button variant="primary" onClick={handleCreateUser}>
                {loading ? 'Signing up...' : 'Signup'}
              </Button>
            </Modal.Footer>
          </Modal>
        </Form>


      </Container>
    </div>
  );
}

export default Login;