import React, { useEffect, useState } from 'react';
import { useNavigate, useParams, Link } from 'react-router-dom';
import { Container, Button, ButtonGroup, Form } from 'react-bootstrap';
import { GrTransaction } from "react-icons/gr";
import { FaHome } from "react-icons/fa";

function Transfer() {
    // Initialize variables
    const navigate = useNavigate();
    const { accountType } = useParams();
    const [accountDetails, setAccountDetails] = useState(null);
    const [newAccountNum, setNewAccountNum] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

    // Function to handle transfer
    const handleTransfer = async () => {
        try {
            const token = localStorage.getItem('token');
            const amount = parseFloat(document.getElementById('formBasicEmail').value);

            // Check if the entered amount is valid
            if (isNaN(amount) || amount <= 0) {
                throw new Error('Please enter a valid positive amount');
            }

            //  Send transfer request to the server
            const response = await fetch(`http://localhost:8000/accounts/transfer/${accountDetails.accountNumber}/${newAccountNum}?amount=${amount}`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            const data = await response.json();

            //Throw error if response is not ok
            if (!response.ok) {
                throw new Error(data.detail || 'Failed to transfer amount');
            }

            // Transfer successful, option to update UI or perform other actions
            console.log('Amount Transferred successfully:', data);
            alert(`Amount Transferred successfully: ${amount}`)
        } catch (error) {
            console.error('Error Transferring amount:', error);
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

                // Find the account with the specified accountType
                const accounts = await responseAccounts.json();
                const matchedAccount = accounts.find(acc => acc.accountType === accountType);
                if (matchedAccount) {
                    setAccountDetails(matchedAccount);
                } else {
                    throw new Error('No matching account found');
                }
            // Handle error, display error message to the user, etc.
            } catch (error) {
                console.error(error);
                navigate('/home');
            } finally {
                setIsLoading(false);
            }
        };

        verifyTokenAndFetchAccount();
    }, [navigate, accountType]);

    // Display loading message while fetching account details
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

    // Display transfer form
    return (
        <Container>
            <Container>
                <Link to="/home">
                    <FaHome size={50} className="mr-2" style={{ marginRight: '10px' }} />
                </Link>
            </Container>
            {/* Container for transfer form */}
            <Container className="d-flex flex-column vh-100 justify-content-center align-items-center">
                <GrTransaction size={30} style={{ marginRight: '10px' }} />
                <h1>Transfer</h1>
                <Form>
                    <Form.Group className="mb-3" controlId="formBasicEmail">
                        <Form.Control type="email" placeholder="Enter amount" />
                    </Form.Group>

                    <Form.Group className="mb-3" controlId="formAccountNumber">
                        <Form.Control type="email" placeholder="Enter account number" onChange={(e) => setNewAccountNum(e.target.value)}/>
                    </Form.Group>

                    <Button variant="success" size="md" onClick={handleTransfer} className="my-2" style={{ width: '200px' }}>Transfer</Button>
                </Form>
            </Container>
        </Container>
    );
}

export default Transfer;
