### Project Overview

This is a Streamlit application for financial analysis and business simulation called "SAM Financial Model". It's designed to be an advanced tool for financial projections, risk analysis, and data visualization, going beyond traditional spreadsheets.

The application is built with Python and uses the following key libraries:

-   **Streamlit:** For creating the interactive web interface.
-   **Pandas:** For data manipulation and analysis.
-   **NumPy:** For numerical operations.
-   **Plotly:** For creating interactive charts and visualizations.
-   **Openpyxl:** For working with Excel files.

The project is structured into several directories:

-   **`app/`:** Contains the Streamlit application code, including the main entry point (`main.py`), different pages for dashboards, and reusable UI components.
-   **`core/`:**  Houses the core logic of the financial model, including the projection engine, configuration management, and analysis modules.
-   **`data/`:**  Intended for storing data related to scenarios, exports, and templates.
-   **`notebooks/`:** Contains Jupyter notebooks for analysis and experimentation.
-   **`tests/`:** Includes tests for the core components of the application.

### Building and Running

To run the application, you need to have Python and the required libraries installed. You can install the dependencies using pip:

```bash
pip install -r requirements.txt
```

Once the dependencies are installed, you can run the Streamlit application with the following command:

```bash
streamlit run app/main.py
```

This will start a local web server and open the application in your browser.

### Development Conventions

The codebase is well-structured and follows good software engineering practices. The separation of concerns between the UI (`app/`) and the core logic (`core/`) makes the code modular and maintainable. The use of a configuration object (`ConfigFinanceira`) to drive the financial model allows for easy customization and scenario analysis.

The project also includes a `tests/` directory, which indicates a commitment to testing and code quality. The tests seem to be focused on the core engine and configuration, which are critical components of the application.

Overall, this project is a comprehensive and well-engineered solution for financial modeling and analysis. It provides a solid foundation for further development and customization.
