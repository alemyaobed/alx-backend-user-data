# 0x00. Personal Data

## Back-end

This directory focuses on handling and securing user data on the back-end. It includes implementations for authentication, logging, and encryption to ensure data security.

### Authentication

Learn how to authenticate users securely using environment variables and best practices.

### Resources

Explore essential resources and packages used in this directory:

- [What Is PII, non-PII, and Personal Data?](https://piwik.pro/blog/what-is-pii-personal-data/)
- [Logging Documentation](https://docs.python.org/3/library/logging.html)
- [bcrypt Package Documentation](https://github.com/pyca/bcrypt/)

### Learning Objectives

By completing this project, you will gain proficiency in:

- **Identifying Personally Identifiable Information (PII)**: This involves understanding what constitutes PII, such as names, email addresses, social security numbers, etc., and being able to recognize and handle this sensitive information appropriately to ensure privacy and compliance with data protection regulations.

- **Implementing a log filter to obfuscate PII fields**: When logging sensitive information like user data, it's crucial to filter out or obfuscate PII to prevent unauthorized access or exposure. Implementing a log filter ensures that sensitive information is protected in log files and other outputs.

- **Encrypting passwords and validating input passwords securely**: Passwords are sensitive data that should never be stored or transmitted in plain text. Learning how to encrypt passwords using secure hashing algorithms like bcrypt and implementing secure methods for validating user input passwords helps protect user accounts from unauthorized access.

- **Authenticating to a database using environment variables**: Hardcoding database credentials in your source code is a security risk. Using environment variables for database authentication helps keep sensitive information like usernames, passwords, and connection strings secure and separate from your codebase.

These learning objectives are essential for developing secure backend systems that handle user data responsibly and comply with privacy regulations. Mastering these skills ensures that your applications are robust against common security threats and vulnerabilities.

### Requirements

Ensure your project meets the following criteria:

- All files interpreted/compiled on Ubuntu 18.04 LTS using Python 3.7
- Files follow the `pycodestyle` style (version 2.5)
- All modules, classes, and functions are well-documented with clear explanations
- Code should use type annotations for all functions

### GitHub Repository

- Repository: [alx-backend](https://github.com/lemyjay/alx-backend-user-data)

