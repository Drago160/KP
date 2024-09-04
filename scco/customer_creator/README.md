# Customer Creator

This microservice is responsible for receiving a client from an external service, generating a white_list, and sending an insert request to the database.

## API

Examples of received (request) and sent (no answer) data are located in `customer_creator/src/service/data`.

## Functionality

- **Obtaining customer data**: Retrieves customer information from external services.
- **Generating a white list and inserting into data**: Creates a white list of clients and prepares the data for database insertion.
- **Sending to database**: Sends the prepared data to the database.


