# Civil Backend - Automatic Report Generation

This Flask application provides automatic report generation functionality for project details and user financial data in both PDF and Excel formats.

## Features

### 🔹 Automatic Report Generation
- **PDF Reports**: Professional, shareable summaries using ReportLab
- **Excel Reports**: Detailed analysis with custom calculations using OpenPyXL
- **Filtered Data**: Reports respect current screen filters (date range, category, user, project)
- **Real-time Generation**: Reports are generated on-demand with current data

### 🔹 Supported Report Types

#### Project Details Reports
- **Employee Details**: Individual expense records with names, types, dates, and amounts
- **Category Details**: Budget vs actual expense comparisons by category
- **Comprehensive Reports**: All project financial data

#### User Financial Detail Reports
- **Individual User Reports**: All financial transactions for a specific user
- **Date Range Filtering**: Filter by start and end dates
- **Project-wise Breakdown**: Expenses organized by project

## API Endpoints

### Project Report Endpoints

#### Download Project Report as PDF
```
GET /download-project-report-pdf
```

**Parameters:**
- `projectname` (required): Name of the project
- `type` (optional): Report type - 'all', 'employee', or 'category' (default: 'all')

**Example:**
```
GET /download-project-report-pdf?projectname=Highway%20Masterplan&type=employee
```

#### Download Project Report as Excel
```
GET /download-project-report-excel
```

**Parameters:**
- `projectname` (required): Name of the project
- `type` (optional): Report type - 'all', 'employee', or 'category' (default: 'all')

**Example:**
```
GET /download-project-report-excel?projectname=Highway%20Masterplan&type=category
```

### User Financial Report Endpoints

#### Download User Financial Report as PDF
```
GET /download-user-financial-report-pdf
```

**Parameters:**
- `id` (required): User ID
- `start_date` (optional): Start date for filtering (YYYY-MM-DD format)
- `end_date` (optional): End date for filtering (YYYY-MM-DD format)

**Example:**
```
GET /download-user-financial-report-pdf?id=USER001&start_date=2024-01-01&end_date=2024-12-31
```

#### Download User Financial Report as Excel
```
GET /download-user-financial-report-excel
```

**Parameters:**
- `id` (required): User ID
- `start_date` (optional): Start date for filtering (YYYY-MM-DD format)
- `end_date` (optional): End date for filtering (YYYY-MM-DD format)

**Example:**
```
GET /download-user-financial-report-excel?id=USER001&start_date=2024-01-01&end_date=2024-12-31
```

## Installation

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Database Setup:**
   - Ensure MySQL is running
   - Create database using `database/civildb.sql`
   - Update database connection in `app.py` if needed

3. **Run the Application:**
   ```bash
   python app.py
   ```

## Dependencies

### Core Dependencies
- **Flask**: Web framework
- **Flask-SQLAlchemy**: Database ORM
- **Flask-JWT-Extended**: JWT authentication
- **Flask-CORS**: Cross-origin resource sharing

### Report Generation Dependencies
- **ReportLab**: PDF generation
- **OpenPyXL**: Excel file generation
- **Pandas**: Data manipulation
- **NumPy**: Numerical operations

## Report Format Details

### PDF Reports
- **Page Size**: A4
- **Styling**: Professional table format with headers
- **Features**:
  - Centered title with timestamp
  - Grey header row with white text
  - Beige data rows with black text
  - Grid borders for readability
  - Auto-formatted currency values

### Excel Reports
- **Format**: .xlsx (Excel 2007+)
- **Styling**: Professional spreadsheet format
- **Features**:
  - Merged title cells with bold formatting
  - Timestamp in italic
  - Grey header row with bold text
  - Auto-adjusted column widths
  - Center-aligned data
  - Professional borders and fills

## Usage Examples

### Frontend Integration

#### Project Details Page
```javascript
// Download PDF Report
function downloadProjectPDF(projectName, reportType = 'all') {
    const url = `/download-project-report-pdf?projectname=${encodeURIComponent(projectName)}&type=${reportType}`;
    window.open(url, '_blank');
}

// Download Excel Report
function downloadProjectExcel(projectName, reportType = 'all') {
    const url = `/download-project-report-excel?projectname=${encodeURIComponent(projectName)}&type=${reportType}`;
    window.open(url, '_blank');
}
```

#### User Financial Detail Screen
```javascript
// Download PDF Report with date filters
function downloadUserFinancialPDF(userId, startDate, endDate) {
    let url = `/download-user-financial-report-pdf?id=${encodeURIComponent(userId)}`;
    if (startDate) url += `&start_date=${startDate}`;
    if (endDate) url += `&end_date=${endDate}`;
    window.open(url, '_blank');
}

// Download Excel Report with date filters
function downloadUserFinancialExcel(userId, startDate, endDate) {
    let url = `/download-user-financial-report-excel?id=${encodeURIComponent(userId)}`;
    if (startDate) url += `&start_date=${startDate}`;
    if (endDate) url += `&end_date=${endDate}`;
    window.open(url, '_blank');
}
```

### Button Implementation
```html
<!-- Project Details Page -->
<div class="export-buttons">
    <button onclick="downloadProjectPDF('ProjectName', 'employee')" class="btn btn-primary">
        <i class="fas fa-file-pdf"></i> Download as PDF
    </button>
    <button onclick="downloadProjectExcel('ProjectName', 'category')" class="btn btn-success">
        <i class="fas fa-file-excel"></i> Download as Excel
    </button>
</div>

<!-- User Financial Detail Screen -->
<div class="export-buttons">
    <button onclick="downloadUserFinancialPDF('USER001', '2024-01-01', '2024-12-31')" class="btn btn-primary">
        <i class="fas fa-file-pdf"></i> Download as PDF
    </button>
    <button onclick="downloadUserFinancialExcel('USER001', '2024-01-01', '2024-12-31')" class="btn btn-success">
        <i class="fas fa-file-excel"></i> Download as Excel
    </button>
</div>
```

## Error Handling

The API endpoints include comprehensive error handling:

- **400 Bad Request**: Missing required parameters
- **404 Not Found**: Project or user not found
- **500 Internal Server Error**: Server-side errors with detailed messages

## Security Considerations

- All endpoints validate input parameters
- SQL injection protection through SQLAlchemy ORM
- File downloads are served with proper MIME types
- No sensitive data is logged in error messages

## Performance Notes

- Reports are generated in memory using BytesIO buffers
- No temporary files are created on disk
- Large datasets are handled efficiently through database queries
- Auto-adjusting column widths in Excel for optimal readability

## Troubleshooting

### Common Issues

1. **Missing Dependencies**: Ensure all packages in `requirements.txt` are installed
2. **Database Connection**: Verify MySQL is running and connection string is correct
3. **Memory Issues**: For very large datasets, consider implementing pagination
4. **File Download Issues**: Check browser settings for file downloads

### Debug Mode
Run the application in debug mode for detailed error messages:
```bash
python app.py
```

## License

This project is part of the Civil Backend system for construction project management. 