import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Dropdown, Container, Button, ButtonGroup } from 'react-bootstrap';
import { FaUser } from 'react-icons/fa';

function Home() {
    const navigate = useNavigate();
    const [username, setUser] = useState(null);
    const [id, setId] = useState(null);
    const [selectedValue, setSelectedValue] = useState('');
    const [items, setItems] = useState([]);
    const [isLoading, setIsLoading] = useState(false);

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
                fetchAccounts(id); // Fetch accounts once the token is verified and user ID is available
            } catch (error) {
                console.error(error);
                localStorage.removeItem('token');
                navigate('/');
            }
        };

        const fetchAccounts = async (userId) => {
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
        alert(`You selected: ${selectedValue}`);
        // Here you can add your submit logic, e.g., API call
    };

    if (isLoading) {
        return <p>Loading...</p>;
    }

    return (
        <>
            <div className="d-flex align-items-center p-3">
                <FaUser size={36} className="mr-2" style={{ marginRight: '10px' }} />
                <h2>{username}</h2> 
            </div>
            <Container className="d-flex justify-content-center align-items-center vh-100">
                
                <div className="d-flex flex-column align-items-center">
                    <Dropdown as={ButtonGroup} onSelect={handleSelect} className="mb-3" size="lg">
                        <Dropdown.Toggle variant="success" id="dropdown-basic" style={{minWidth: '200px'}}>
                            {selectedValue || "Select Account"}
                        </Dropdown.Toggle>

                        <Dropdown.Menu>
                            {items.map(item => (
                                <Dropdown.Item key={item.accountNumber} eventKey={item.accountType}>
                                    {item.accountType}
                                </Dropdown.Item>
                            ))}
                        </Dropdown.Menu>
                    </Dropdown>
                    <div className="d-flex justify-content-end w-100">
                        <Button className="btn btn-primary" onClick={handleSubmit} size='sm'>
                            Submit
                        </Button>
                    </div>
                </div>
            </Container>
        </>
    )
}

export default Home;
