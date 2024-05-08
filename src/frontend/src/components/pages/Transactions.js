import React, { useEffect, useState } from 'react';
import { useNavigate, useParams, Link } from 'react-router-dom';
import { Container, Table } from 'react-bootstrap';
import { FaHome } from "react-icons/fa"; // React icons

function Transactions() {
    // Navigate hook
    const navigate = useNavigate();
    // useParams hook accesses parameters from URL
    const { accountNumber } = useParams(); 
    // State variables to store transactions and loading
    const [transactions, setTransactions] = useState([]);
    const [isLoading, setIsLoading] = useState(true);

    // useEffect hook fetches transactions on mount or when account number changes
    useEffect(() => {
        const fetchTransactions = async () => {
            try {
                // Get user's token from local storage
                const token = localStorage.getItem('token');
                // Fetch transactions
                const response = await fetch(`http://localhost:8000/transactions/${accountNumber}`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (!response.ok) {
                    throw new Error('Failed to fetch transactions');
                }
                // Parse response data and set in transaction state
                const data = await response.json();
                setTransactions(data);
            } catch (error) {
                console.error('Error fetching transactions:', error);
                // Handle error
            } finally {
                // sets loading state to false when data fetching complete
                setIsLoading(false);
            }
        };
        // call fetchTransactions function
        fetchTransactions();
    }, [accountNumber]); // Dependency array ensures effect only runs when account numnber changes

    if (isLoading) {
        return (
            <Container className="d-flex vh-100 justify-content-center align-items-center">
                <p>Loading...</p>
            </Container>
        );
    }
    // Render transaction history table
    return (
        <Container>
            <Container>
                <Link to="/home">
                    <FaHome size={50} className="mr-2" style={{ marginRight: '10px' }} />
                </Link>
            </Container>
            <Container className="d-flex flex-column vh-100 justify-content-center align-items-center">
                <h1>Transaction History</h1>
                <Table striped bordered hover>
                    <thead>
                        <tr>
                            <th>Amount</th>
                            <th>Date</th>
                            <th>Type</th>
                        </tr>
                    </thead>
                    <tbody>
                        {transactions.map(transaction => (
                            <tr key={transaction.time}>
                                <td>{transaction.amount}</td>
                                <td>{transaction.time}</td>
                                <td>{transaction.type}</td>
                            </tr>
                        ))}
                    </tbody>
                </Table>
            </Container>
        </Container>
    );
}

export default Transactions;
