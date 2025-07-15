# SayThanks Mobile Testing

This project is designed to facilitate mobile device testing for the web application "saythanks.io". It focuses on validating the app's responsive design and layout on both Android and iOS devices, ensuring a seamless user experience across various screen sizes.

## Project Structure

The project is organized into several directories and files, each serving a specific purpose:

- **tests/**: Contains all the test scripts for mobile testing.
  - **mobile/**: Includes tests specific to mobile devices.
    - **android/**: Tests for Android devices, including responsive and layout tests.
    - **ios/**: Tests for iOS devices, including responsive and layout tests.
    - **cross_platform/**: Tests that validate the app's behavior across multiple platforms.
  - **selenium/**: Contains Selenium-based tests for mobile responsiveness and touch interactions.
  - **appium/**: Includes tests for native and hybrid mobile applications.

- **config/**: Configuration files for device settings and integration with testing services like BrowserStack and Sauce Labs.

- **utils/**: Utility scripts that provide helper functions for device management, screenshots, and common testing tasks.

- **reports/**: Directory for storing test reports (tracked by version control).

- **requirements.txt**: Lists the dependencies required for the project.

- **pytest.ini**: Configuration settings for pytest.

- **docker-compose.yml**: Defines the services and configurations needed to run the testing environment in Docker.

## Getting Started

To set up the testing environment, follow these steps:

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd saythanks-mobile-testing
   ```

2. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

3. **Configure device settings**:
   - Update the `config/devices.json` file with the necessary device configurations for Android and iOS.

4. **Run tests**:
   - Use pytest to run the tests:
   ```
   pytest tests/
   ```

5. **Docker Setup** (optional):
   - If you prefer to run the tests in a Docker environment, use the provided `docker-compose.yml` file:
   ```
   docker-compose up
   ```

## Testing Features

- **Responsive Design Testing**: Automated tests to validate the app's responsiveness on various screen sizes.
- **Layout Testing**: Ensure that UI elements are correctly positioned and visually appealing on mobile devices.
- **Cross-Platform Testing**: Validate consistent behavior and appearance across different platforms.
- **Touch Interaction Testing**: Verify that touch gestures and interactions function correctly on mobile devices.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.