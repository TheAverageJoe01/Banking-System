import React, { useEffect, useState } from 'react';
import { useNavigate, useParams, Link } from 'react-router-dom';
import { Container, Button, ButtonGroup } from 'react-bootstrap';
import { FaHome } from 'react-icons/fa'
function Account() {
    const navigate = useNavigate();
    const { accountType } = useParams();
    const [accountDetails, setAccountDetails] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

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
                <h1>{accountDetails.accountType} Account</h1>
                <h3>#{accountDetails.accountNumber}</h3>
                <p>Balance: £{accountDetails.balance}</p>
                <Button variant="secondary" size="lg" onClick={null} className="my-2" style={{ width: '200px' }}>Balance</Button>
                <Button variant="secondary" size="lg" onClick={handleWithdrawClick} className="my-2" style={{ width: '200px' }}>Withdraw</Button>
                <Button variant="secondary" size="lg" onClick={handleDepositClick} className="my-2" style={{ width: '200px' }}>Deposit</Button>
                <Button variant="secondary" size="lg" onClick={handleTransferClick} className="my-2" style={{ width: '200px' }}>Transfer</Button>
                <Button variant="danger" size="sm" onClick={null} className="my-2">Delete</Button>
            </Container>
        </Container>
    );
}

export default Account;
