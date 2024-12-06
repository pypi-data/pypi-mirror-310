# contrast-route-duplicates

A command-line tool for analyzing duplicate route signatures in Contrast Security applications. This tool helps identify repeated route signatures across your application, which can be useful for identifying potential issues caused from merging duplicate applications.

## Features

- Fast, asynchronous API querying with concurrent requests
- Progress tracking for large datasets
- CSV export for detailed analysis
- Summary statistics including duplicate counts and percentages
- Configurable batch size and concurrency
- Environment-based configuration
- Rich terminal output with color-coded results

## Installation

1. Install:
```bash
pip install contrast-route-duplicates
```

2. Create a `.env` file with your Contrast Security credentials:
```ini
CONTRAST_BASE_URL=https://app.contrastsecurity.com/Contrast
CONTRAST_ORG_UUID=your-org-uuid
CONTRAST_API_KEY=your-api-key
CONTRAST_AUTH=your-auth-header
```

## Usage

Basic usage:
```bash
contrast_route_duplicates APP_ID
```

With all options:
```bash
contrast_route_duplicates APP_ID \
    --csv output.csv \
    --batch-size 200 \
    --concurrent-requests 20 \
    --verbose
```

### Options

- `APP_ID`: The Contrast Security application ID to analyze (required)
- `--csv`: Output file path for detailed CSV results
- `--batch-size`: Number of routes to fetch per request (default: 100)
- `--concurrent-requests`: Maximum number of concurrent API requests (default: 10)
- `--verbose`: Enable verbose logging

## Output

The tool provides a summary of route signature analysis including:

- Total number of routes
- Number of unique signatures
- Number of signatures with duplicates
- Total number of duplicate routes
- Percentage of routes that are duplicates

Example output:
```
Starting analysis...
Fetching routes: 100% ██████████ 1615/1615

Route Analysis Summary
┌──────────────────────────┬────────────┐
│ Total routes            │     1,615 │
│ Unique signatures       │       602 │
│ Signatures with duplics │       316 │
│ Total duplicate routes  │       708 │
│ Duplicate percentage    │     43.8% │
└──────────────────────────┴────────────┘

Detailed results have been written to: output.csv
```

## CSV Output Format

The CSV output includes two columns:
- `Signature`: The route signature
- `Count`: Number of occurrences of that signature

Example:
```csv
Signature,Count
org.example.Controller.index(),3
org.example.UserService.getUser(),2
```

## Environment Variables

| Variable          | Description               | Example                                   |
| ----------------- | ------------------------- | ----------------------------------------- |
| CONTRAST_BASE_URL | Contrast Security API URL | https://app.contrastsecurity.com/Contrast |
| CONTRAST_ORG_UUID | Organization UUID         | 12345678-90ab-cdef-1234-567890abcdef      |
| CONTRAST_API_KEY  | API Key                   | your-api-key                              |
| CONTRAST_AUTH     | Authorization header      | base64-encoded-credentials                |

## Development

Requirements:
- Python 3.8+
- httpx
- typer
- rich
- python-dotenv
- tqdm

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the tests
5. Submit a pull request

## Support

For issues, questions, or contributions, please open an issue in the GitHub repository.
