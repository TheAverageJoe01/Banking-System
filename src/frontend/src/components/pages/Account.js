import React, { useEffect, useState } from 'react';
import { useNavigate, useParams, Link } from 'react-router-dom';
import { Container, Button, ButtonGroup } from 'react-bootstrap';
import { FaHome } from 'react-icons/fa'
function Account() {
    // Initialize variables
    const navigate = useNavigate();
    const { accountType } = useParams();
    const [accountDetails, setAccountDetails] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

    // Function to handle account deletion  
    const handleDelete = async () => {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`http://localhost:8000/accounts/${accountDetails.accountNumber}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            
            const data = await response.json();
            //Throw error if response is not ok
            if (!response.ok) {
                throw new Error(data.detail || 'Failed to delete account');
            }

            // Account deleted successfully, option to update UI or perform other actions
            console.log('Account deleted successfully:', data);
            alert('Account deleted successfully');
            navigate('/home')
        } catch (error) {
            console.error('Error deleting account:', error);
            alert(error);
            // Handle error, display error message to the user, etc.
        }
    };

    // Fetch account details based on accountType
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
            } catch (error) {
                console.error(error);
                navigate('/home');
            } finally {
                setIsLoading(false);
            }
        };

        verifyTokenAndFetchAccount();
    }, [navigate, accountType]);


    // Functions to handle navigation to different pages
    const handleTransactionsClick = (event) => {
        event.preventDefault();
        navigate(`/account/transactions/${accountDetails.accountNumber}`);
    };

    const handleDepositClick = (event) => {
        event.preventDefault();
        navigate(`/account/deposit/${accountType}`);
    };
    const handleWithdrawClick = (event) => {
        event.preventDefault();
        navigate(`/account/withdraw/${accountType}`);
    };
    const handleTransferClick = (event) => {
        event.preventDefault();
        navigate(`/account/transfer/${accountType}`);
    };

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

    // Render account details
    return (
        <Container>
            <Container>
                <Link to="/home">
                    <FaHome size={50} className="mr-2" style={{ marginRight: '10px' }} />
                </Link>
            </Container>
            {/* Container for account details */}
            <Container className="d-flex flex-column vh-100 justify-content-center align-items-center">
                <h1>{accountDetails.accountType} Account</h1>
                <h3>#{accountDetails.accountNumber}</h3>
                <p>Balance: £{accountDetails.balance}</p>
                {/* Buttons for different actions */}
                <Button variant="secondary" size="lg" onClick={handleTransactionsClick} className="my-2" style={{ width: '200px' }}>Transactions</Button>
                <Button variant="secondary" size="lg" onClick={handleWithdrawClick} className="my-2" style={{ width: '200px' }}>Withdraw</Button>
                <Button variant="secondary" size="lg" onClick={handleDepositClick} className="my-2" style={{ width: '200px' }}>Deposit</Button>
                <Button variant="secondary" size="lg" onClick={handleTransferClick} className="my-2" style={{ width: '200px' }}>Transfer</Button>
                <Button variant="danger" size="sm" onClick={handleDelete} className="my-2">Delete</Button>
            </Container>
        </Container>
    );
}

export default Account;
