import React, { useEffect, useState } from 'react';
import { useNavigate, useParams, Link } from 'react-router-dom';
import { Container, Button, ButtonGroup, Form } from 'react-bootstrap';
import { GrTransaction } from "react-icons/gr";
import { FaHome } from "react-icons/fa";

function Deposit() {
    // Initialize variables
    const navigate = useNavigate();
    const { accountType } = useParams();
    const [accountDetails, setAccountDetails] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

    // Function to handle deposit
    const handleDeposit = async () => {
        try {
            const token = localStorage.getItem('token');
            const amount = parseFloat(document.getElementById('formBasicEmail').value);

            //Error handling to check if the entered amount is valid
            if (isNaN(amount) || amount <= 0) {
                throw new Error('Please enter a valid positive amount');
            }

            // Send deposit request to the server
            const response = await fetch(`http://localhost:8000/accounts/deposit/${accountDetails.accountNumber}?amount=${amount}`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            // Parse response
            const data = await response.json();

            //Throw error if response is not ok
            if (!response.ok) {
                throw new Error(data.detail || 'Failed to deposit amount');
            }

            // Deposit successful, option to update UI or perform other actions
            console.log('Amount deposited successfully:', data);
            alert(`Amount deposited successfully: ${amount}`)
        } catch (error) {
            console.error('Error depositing amount:', error);
            alert(error)
            // Handle error, display error message to the user, etc.
        }
    };

    // Function to verify token and fetch account details
    useEffect(() => {
        const verifyTokenAndFetchAccount = async () => {
            const token = localStorage.getItem('token');
            if (!token) {
                navigate('/');
                return;
            }

            try {
                // Verify token
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

                // Throw error if response is not ok
                if (!responseAccounts.ok) {
                    throw new Error('Failed to fetch accounts');
                }
                // Extract account details and find matching account based on account type
                const accounts = await responseAccounts.json();
                const matchedAccount = accounts.find(acc => acc.accountType === accountType);
                if (matchedAccount) {
                    setAccountDetails(matchedAccount);
                } else {
                    throw new Error('No matching account found');
                }
            } catch (error) {
                // Log error and navigate to home page
                console.error(error);
                navigate('/home');
            } finally {
                setIsLoading(false);
            }
        };

        verifyTokenAndFetchAccount();
    }, [navigate, accountType]);

    // Render loading state while fetching account details
    if (isLoading) {
        return (
            <Container className="d-flex vh-100 justify-content-center align-items-center">
                <p>Loading...</p>
            </Container>
        );
    }
    // Render if no account details found
    if (!accountDetails) {
        return (
            <Container className="d-flex vh-100 justify-content-center align-items-center">
                <p>No account details found for the specified type.</p>
            </Container>
        );
    }

    // Render deposit form
    return (
        <Container>
            <Container>
                <Link to="/home">
                    <FaHome size={50} className="mr-2" style={{ marginRight: '10px' }} />
                </Link>
            </Container>
            {/* Container for deposit form */}
            <Container className="d-flex flex-column vh-100 justify-content-center align-items-center">
                <GrTransaction size={30} style={{ marginRight: '10px' }} />
                <h1>Deposit</h1>
                <Form>
                    {/* Form for entering deposit amount */}
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
