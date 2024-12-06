
import pytest
from unittest.mock import Mock
from myfinances import MyFinancesClient
from myfinances.finance.invoices import InvoicesService, Invoice

@pytest.fixture
def mock_client():
    mock = Mock(spec=MyFinancesClient)
    mock.session = Mock()
    return mock

@pytest.fixture
def invoices_service(mock_client):
    return InvoicesService(mock_client)

def test_create_invoice(invoices_service):
    mock_response = Mock()
    mock_response.json.return_value = {
        "id": 1,
        "customer_id": 123,
        "amount": 250.0,
        "status": "created",
        "due_date": None,
        "description": "Service Fee"
    }
    mock_response.status_code = 200
    invoices_service._client.session.post.return_value = mock_response

    invoice = invoices_service.create_invoice(customer_id=123, amount=250.0, description="Service Fee")

    assert isinstance(invoice, Invoice)
    assert invoice.id == 1
    assert invoice.customer_id == 123
    assert invoice.amount == 250.0
    assert invoice.description == "Service Fee"

def test_list_invoices(invoices_service):
    mock_response = Mock()
    mock_response.json.return_value = [
        {"id": 1, "customer_id": 123, "amount": 250.0, "description": "Service Fee", "status": "pending"},
        {"id": 2, "customer_id": 124, "amount": 300.0, "description": "Consulting Fee", "status": "pending"}
    ]
    mock_response.status_code = 200
    invoices_service._client.session.get.return_value = mock_response

    invoices = invoices_service.list_invoices()

    assert len(invoices) == 2
    assert isinstance(invoices[0], Invoice)
    assert invoices[0].id == 1
    assert invoices[1].amount == 300.0