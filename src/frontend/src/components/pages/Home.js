import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Dropdown, Container, Button, ButtonGroup } from 'react-bootstrap';
import { FaUser } from 'react-icons/fa';
import { Modal, Form } from 'react-bootstrap';


function Home() {
    const navigate = useNavigate();
    const [username, setUser] = useState(null);
    const [id, setId] = useState(null);
    const [selectedValue, setSelectedValue] = useState('');
    const [items, setItems] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [showModal, setShowModal] = useState(false);
    const [newAccountType, setNewAccountType] = useState('');

    const handleCloseModal = () => setShowModal(false);
    const handleShowModal = () => setShowModal(true);

    const handleCreateAccount = async () => {
        try {
            const token = localStorage.getItem('token');
            // Check if an account of the same type already exists
            const existingAccount = items.find(item => item.accountType === newAccountType);
            if (existingAccount) {
                alert('Account of the same type already exists')
                throw new Error('Account of the same type already exists');
            }

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
            navigate(`/account/${newAccountType}`);
            // Account created successfully, close the modal and potentially update UI
            handleCloseModal();
            
            // Optionally, you can update the UI to reflect the new account
        } catch (error) {
            console.error('Error creating account:', error);
            // Handle error, display error message to the user, etc.
        }
    };

    useEffect(() => {
        const verifyToken = async () => {
            const token = localStorage.getItem('token');
            if (!token) {
                navigate('/');
                return;
            }

            try {
                const response = await fetch(`http://localhost:8000/verify-token/${token}`);
                if (!response.ok) {
                    throw new Error('Token verification failed');
                }

                const { username, id } = await response.json();
                setUser(username);
                setId(id);
                fetchAccounts(id);
            } catch (error) {
                console.error(error);
                localStorage.removeItem('token');
                navigate('/');
            }
        };

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
        verifyToken();
    }, [navigate]);

    const handleSelect = (eventKey) => {
        setSelectedValue(eventKey);
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        if (selectedValue) {
            const selectedAccount = items.find(item => item.accountType === selectedValue);
            if (selectedAccount) {
                navigate(`/account/${selectedAccount.accountType}`);
            }
        }
    };


    if (isLoading) {
        return <p>Loading...</p>;
    }

    return (
        <Container>
            <Container className="d-flex align-items-center p-3">
                <FaUser size={36} className="mr-2" style={{ marginRight: '10px' }} />
                <h2>{username}</h2>
            </Container>
            <Container className="d-flex justify-content-center align-items-center vh-100">

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
