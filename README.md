# Sales and Inventory System

## Project Demo

<https://user-images.githubusercontent.com/15692310/232661172-8889bc01-2f12-4213-a360-2d2225b23ed8.mp4>

## Project Description

This project is a system with a simplified interface that covers product and inventory control, including operations for product registration, listing, modification, and deletion. The project also includes a sales system where you can name the customer, select the payment method, and complete the purchase. Finally, there is an option to view sales that occurred on a specific date.

## How to Use

The simplest way to use the system is to download the latest release from the [releases section](https://github.com/Diegiwg/ssiql/releases).

If you want to run the development version, follow these steps:

Clone the repository:

```bash
git clone https://github.com/Diegiwg/ssiql.git
```

Navigate to the directory:

```bash
cd ssiql
```

Run the command:

```bash
pip install -r requirements-dev.txt
```

Run the command:

```bash
briefcase dev
```

### Database

The database is automatically generated and uses two [JSON](https://www.json.org/) files for storage, which can be found in `~/data/`.

Currently, there are releases available for Windows, but in the development version, it is possible to run on Linux.

### Available Features

- Product registration
- Product listing
- Product modification
- Product deletion
- Stock quantity modification
- Sales registration
- Sales listing

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Developer

- Diego Queiroz - [@Diegiwg](https://www.linkedin.com/in/diego-silva-queiroz/)

## Contributions

Contributions are welcome! To contribute, fork the repository, create a new branch, and send a pull request with your changes.
