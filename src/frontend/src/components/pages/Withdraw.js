import React, { useEffect, useState } from 'react';
import { useNavigate, useParams, Link } from 'react-router-dom';
import { Container, Button, ButtonGroup, Form } from 'react-bootstrap';
import { GrTransaction } from "react-icons/gr";
import { FaHome } from "react-icons/fa";

function Withdraw() {
    // Initialize variables
    const navigate = useNavigate();
    const { accountType } = useParams();
    const [accountDetails, setAccountDetails] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    
    // Function to handle withdrawal
    const handleWithdraw = async () => {
        try {
            const token = localStorage.getItem('token');
            const amount = parseFloat(document.getElementById('formBasicEmail').value);

            // Check if the entered amount is valid
            if (isNaN(amount) || amount <= 0) {
                throw new Error('Please enter a valid positive amount');
            }

            // Send withdrawal request to the server
            const response = await fetch(`http://localhost:8000/accounts/withdraw/${accountDetails.accountNumber}?amount=${amount}`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            const data = await response.json();

            //Throw error if response is not ok
            if (!response.ok) {
                throw new Error(data.detail || 'Failed to withdraw amount');
            }

            // withdraw successful
            console.log('Amount withdrew successfully:', data);
            alert(`Amount withdrew successfully: ${amount}`)
        } catch (error) {
            console.error('Error withdrawing amount:', error);
            alert(error)
            // Handle error, display error message to the user, etc.
        }
    };

    // Function to verify token and fetch account detail
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
                
                //Throw error if response is not ok
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
            //Catch any errors and redirect to home page
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

    // display if no account details found
    if (!accountDetails) {
        return (
            <Container className="d-flex vh-100 justify-content-center align-items-center">
                <p>No account details found for the specified type.</p>
            </Container>
        );
    }

    // Display withdrawal form
    return (
        <Container>
            <Container>
                <Link to="/home">
                    <FaHome size={50} className="mr-2" />
                </Link>
            </Container>
            {/* Container for withdrawal form */}
            <Container className="d-flex flex-column vh-100 justify-content-center align-items-center">
                <GrTransaction size={30} style={{ marginRight: '10px' }} />
                <h1>Withdraw</h1>
                <Form>
                    <Form.Group className="mb-3" controlId="formBasicEmail">
                        <Form.Control type="email" placeholder="Enter amount" />
                    </Form.Group>

                    <Button variant="success" size="md" onClick={handleWithdraw} className="my-2" style={{ width: '200px' }}>Withdraw</Button>
                </Form>
            </Container>
        </Container>
    );
}

export default Withdraw;
