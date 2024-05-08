import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Dropdown, Container, Button, ButtonGroup, Popover, Overlay } from 'react-bootstrap';
import { FaUser } from 'react-icons/fa';
import { Modal, Form } from 'react-bootstrap';


function Home() {
    // Navigation hook from react-router-dom to route effectively between pages
    const navigate = useNavigate();

    // State variables
    const [username, setUser] = useState(null);
    const [id, setId] = useState(null);
    const [selectedValue, setSelectedValue] = useState('');
    const [items, setItems] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [showModal, setShowModal] = useState(false);
    const [newAccountType, setNewAccountType] = useState('');
    const [showUserOverlay, setShowUserOverlay] = useState(false);
    const [editingUser, setEditingUser] = useState(false);
    // open and close modal functions
    const handleCloseModal = () => setShowModal(false);
    const handleShowModal = () => setShowModal(true);

    // Function handles create account
    const handleCreateAccount = async () => {
        try {
            const token = localStorage.getItem('token');
            // Check if an account of the same type already exists
            const existingAccount = items.find(item => item.accountType === newAccountType);
            if (existingAccount) {
                alert('Account of the same type already exists')
                throw new Error('Account of the same type already exists');
            }
            // Create new account fetching to make HTTP request
            const response = await fetch('http://localhost:8000/accounts/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    balance: 0,
                    accountType: newAccountType,
                    accountNumber: 0
                })
            });

            if (!response.ok) {
                throw new Error('Failed to create account');
            }
            // redirect to new account page based on type
            navigate(`/account/${newAccountType}`);
            // Account created successfully
            handleCloseModal(); // close modal after account creation

        } catch (error) {
            console.error('Error creating account:', error);
            // Handle error
        }
    };
    // Use effect hook used to perform side effects in function components
    // Handles user token verification and account fetching
    useEffect(() => {
        const verifyToken = async () => {
            const token = localStorage.getItem('token');
            if (!token) {
                navigate('/');
                return;
            }
            // Error handling
            try {
                // Verify user token
                const response = await fetch(`http://localhost:8000/verify-token/${token}`);
                if (!response.ok) {
                    throw new Error('Token verification failed');
                }
                // Get user data and fetch accounts based on user id
                const { username, id } = await response.json();
                setUser(username);
                setId(id);
                fetchAccounts(id);
            } catch (error) {
                console.error(error);
                // if error remove token from local storage and navigate to login
                localStorage.removeItem('token');
                navigate('/');
            }
        };
        // fetch user accounts
        const fetchAccounts = async () => {
            setIsLoading(true);
            try {
                const token = localStorage.getItem('token');
                const response = await fetch(`http://localhost:8000/accounts/?skip=0&limit=100`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                if (!response.ok) {
                    throw new Error('Failed to fetch accounts');
                }
                const data = await response.json();
                console.log('Fetched accounts:', data);
                setItems(data);
            } catch (error) {
                console.error('Error fetching accounts:', error);
            } finally {
                setIsLoading(false);
            }
        };
        // calls the verifyToken function on first mount or when editingUser flag state changes
        verifyToken();
    }, [navigate, editingUser]);
    // Function handles account selection from the dropdown
    const handleSelect = (eventKey) => {
        setSelectedValue(eventKey);
    };
    // Function handles account selection navigation
    const handleSubmit = (event) => {
        event.preventDefault();
        if (selectedValue) {
            const selectedAccount = items.find(item => item.accountType === selectedValue);
            if (selectedAccount) {
                navigate(`/account/${selectedAccount.accountType}`);
            }
        }
    };

    // Render loading message when data loading
    if (isLoading) {
        return <p>Loading...</p>;
    }

    // User icon toggle overlay
    const toggleUserOverlay = () => setShowUserOverlay(!showUserOverlay);

    // user logout function
    const handleLogout = () => {
        localStorage.removeItem('token');
        navigate('/')
    };

    // function to enable user editing from user icon
    const handleEditUser = () => {
        setEditingUser(true)
    }
    // Function saves user email/username change 
    const handleSaveEdit = async () => {
        try {
            const token = localStorage.getItem('token');
            const newUsername = document.getElementById('newUsername').value;
            
            // API request, Updates user email/username
            const response = await fetch('http://localhost:8000/users/', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    email: newUsername,
                    password: "string" // This does not get passed through to backend but is required by request body
                })
            });

            if (!response.ok) {
                alert("Failed to change email!");
                throw new Error('Failed to change email')
            }

            const data = await response.json();
            // if response okay update access token in local storage and update username
            if (response.ok) {
                const { user, accessToken, refreshToken } = data;
                localStorage.setItem('token', accessToken);
                setUser(newUsername);
                setEditingUser(false);
            }
                
            } catch (error) {
                console.error('Error creating account:', error);
                // Handle error
            }
        };

        // Render component
        return (
            <Container>
                <Container className="d-flex align-items-center p-3">
                    <FaUser size={36} className="mr-2" style={{ marginRight: '10px', cursor: 'pointer' }} onClick={toggleUserOverlay} id="user-icon" />
                    <h2>{username}</h2>
                </Container>
                <Container className="d-flex justify-content-center align-items-center vh-100">
                    <Overlay
                        show={showUserOverlay}
                        target={document.getElementById("user-icon")}
                        placement="bottom"
                    >
                        <Popover id="popover-contained">
                            <Popover.Header as="h3">User Information</Popover.Header>
                            <Popover.Body>
                                {!editingUser ? (
                                    <>
                                        <Button variant="secondary" onClick={handleEditUser} style={{ marginRight: '10px' }}>
                                            Edit User
                                        </Button>
                                        <Button variant="danger" onClick={handleLogout}>
                                            Logout
                                        </Button>
                                    </>
                                ) : (
                                    <Form>
                                        <Form.Group controlId="formEditUser">
                                            <Form.Label>New Username/Email</Form.Label>
                                            <Form.Control id="newUsername" type="text" placeholder="Enter new username/email" />
                                            <Button variant="primary" size="sm" onClick={handleSaveEdit} style={{ marginTop: '10px' }}>
                                                Submit
                                            </Button>
                                        </Form.Group>
                                    </Form>
                                )}
                            </Popover.Body>
                        </Popover>
                    </Overlay>

                    <div className="d-flex flex-column align-items-center">
                        <h2>Home</h2>
                        <Button variant="success" onClick={handleShowModal} style={{ width: '200px' }} className="mb-3">
                            Create New Account
                        </Button>

                        <Modal show={showModal} onHide={handleCloseModal}>
                            <Modal.Header closeButton>
                                <Modal.Title>Create New Account</Modal.Title>
                            </Modal.Header>
                            <Modal.Body>
                                <Form>
                                    <Form.Group controlId="formAccountType">
                                        <Form.Label>Account Type</Form.Label>
                                        <Form.Control as="select" value={newAccountType} onChange={(e) => setNewAccountType(e.target.value)}>
                                            <option value="" disabled>Select Account</option>
                                            <option value="Savings">Savings</option>
                                            <option value="Current">Current</option>
                                            <option value="Student">Student</option>
                                        </Form.Control>
                                    </Form.Group>
                                </Form>
                            </Modal.Body>
                            <Modal.Footer>
                                <Button variant="secondary" onClick={handleCloseModal} style={{ width: '100px' }}>
                                    Close
                                </Button>
                                <Button variant="success" onClick={handleCreateAccount} style={{ width: '200px' }}>
                                    Create Account
                                </Button>
                            </Modal.Footer>
                        </Modal>

                        <Dropdown as={ButtonGroup} onSelect={handleSelect} className="mb-3" size="lg">
                            <Dropdown.Toggle variant="secondary" id="dropdown-basic" style={{ minWidth: '200px' }}>
                                {selectedValue || "Select Account"}
                            </Dropdown.Toggle>

                            <Dropdown.Menu>
                                {items.map(item => (
                                    <Dropdown.Item key={item.accountNumber} eventKey={item.accountType}>
                                        {item.accountType + " - " + item.accountNumber}
                                    </Dropdown.Item>
                                ))}
                            </Dropdown.Menu>
                        </Dropdown>
                        <div className="d-flex justify-content-end w-100">
                            <Button className="btn btn-success" onClick={handleSubmit} size='sm'>
                                View
                            </Button>
                        </div>
                    </div>
                </Container>
            </Container>
        )
    }

    export default Home;
