import React, { useEffect, useState } from 'react';
import { useNavigate, useParams, Link } from 'react-router-dom';
import { Container, Button, ButtonGroup, Table } from 'react-bootstrap';
import { FaHome } from "react-icons/fa";

function Transactions() {
    const navigate = useNavigate();
    const { accountNumber } = useParams(); // Assuming you have the account number in the URL params
    const [transactions, setTransactions] = useState([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchTransactions = async () => {
            try {
                const token = localStorage.getItem('token');
                const response = await fetch(`http://localhost:8000/transactions/${accountNumber}`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (!response.ok) {
                    throw new Error('Failed to fetch transactions');
                }

                const data = await response.json();
                setTransactions(data);
            } catch (error) {
                console.error('Error fetching transactions:', error);
                // Handle error, display error message to the user, etc.
            } finally {
                setIsLoading(false);
            }
        };

        fetchTransactions();
    }, [accountNumber]);

    if (isLoading) {
        return (
            <Container className="d-flex vh-100 justify-content-center align-items-center">
                <p>Loading...</p>
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
