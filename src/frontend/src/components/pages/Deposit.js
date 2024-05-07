import React, { useEffect, useState } from 'react';
import { useNavigate, useParams, Link } from 'react-router-dom';
import { Container, Button, ButtonGroup, Form } from 'react-bootstrap';
import { GrTransaction } from "react-icons/gr";
import { FaHome } from "react-icons/fa";

function Deposit() {
    const navigate = useNavigate();
    const { accountType } = useParams();
    const [accountDetails, setAccountDetails] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

    const handleDeposit = async () => {
        try {
            const token = localStorage.getItem('token');
            const amount = parseFloat(document.getElementById('formBasicEmail').value);

            if (isNaN(amount) || amount <= 0) {
                throw new Error('Please enter a valid positive amount');
            }

            const response = await fetch(`http://localhost:8000/accounts/deposit/${accountDetails.accountNumber}?amount=${amount}`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Failed to deposit amount');
            }

            // Deposit successful, you may want to update UI or perform other actions
            console.log('Amount deposited successfully:', data);
            alert(`Amount deposited successfully: ${amount}`)
        } catch (error) {
            console.error('Error depositing amount:', error);
            alert(error)
            // Handle error, display error message to the user, etc.
        }
    };

    useEffect(() => {
        const verifyTokenAndFetchAccount = async () => {
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

                // Fetch all accounts and then filter by accountType
                const responseAccounts = await fetch(`http://localhost:8000/accounts`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (!responseAccounts.ok) {
                    throw new Error('Failed to fetch accounts');
                }

                const accounts = await responseAccounts.json();
                const matchedAccount = accounts.find(acc => acc.accountType === accountType);
                if (matchedAccount) {
                    setAccountDetails(matchedAccount);
                } else {
                    throw new Error('No matching account found');
                }
            } catch (error) {
                console.error(error);
                navigate('/home');
            } finally {
                setIsLoading(false);
            }
        };

        verifyTokenAndFetchAccount();
    }, [navigate, accountType]);


    if (isLoading) {
        return (
            <Container className="d-flex vh-100 justify-content-center align-items-center">
                <p>Loading...</p>
            </Container>
        );
    }

    if (!accountDetails) {
        return (
            <Container className="d-flex vh-100 justify-content-center align-items-center">
                <p>No account details found for the specified type.</p>
            </Container>
        );
    }

    return (
        <Container>
            <Container>
                <Link to="/home">
                    <FaHome size={50} className="mr-2" style={{ marginRight: '10px' }} />
                </Link>
            </Container>
            <Container className="d-flex flex-column vh-100 justify-content-center align-items-center">
                <GrTransaction size={30} style={{ marginRight: '10px' }} />
                <h1>Deposit</h1>
                <Form>
                    <Form.Group className="mb-3" controlId="formBasicEmail">
                        <Form.Control type="email" placeholder="Enter amount" />
                    </Form.Group>

                    <Button variant="success" size="md" onClick={handleDeposit} className="my-2" style={{ width: '200px' }}>Deposit</Button>
                </Form>
            </Container>
        </Container>
    );
}

export default Deposit;
