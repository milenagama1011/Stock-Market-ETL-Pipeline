#!/bin/bash
cd "$(dirname "$0")"

echo "$(date): Starting company overview extraction..." >> automation.log

# Only extract overview data
python3 01_AlphaVantage_Extraction.py --overview-only

echo "$(date): ✅ Finished company overview extraction." >> automation.log

