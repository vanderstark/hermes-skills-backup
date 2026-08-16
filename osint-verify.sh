#!/bin/bash
# OSINT Tools Health Check & Test Script
# Usage: ./osint-verify.sh

echo "🔍 === OSINT TOOLKIT VERIFICATION ==="
echo ""

echo "✅ Checking Sherlock..."
sherlock --version 2>/dev/null && echo "   Sherlock: OK" || echo "   Sherlock: MISSING"

echo "✅ Checking theHarvester..."
[ -f "/opt/data/osint/theHarvester/theHarvester.py" ] && echo "   theHarvester: OK" || echo "   theHarvester: MISSING"

echo "✅ Checking SpiderFoot..."
[ -f "/opt/data/osint/spiderfoot/sf.py" ] && echo "   SpiderFoot: OK" || echo "   SpiderFoot: MISSING"

echo "✅ Checking Shodan..."
shodan --version 2>/dev/null && echo "   Shodan CLI: OK" || echo "   Shodan CLI: MISSING"

echo "✅ Checking Python packages..."
python3 -c "import dns.resolver; print('   DNS Python: OK')" 2>/dev/null || echo "   DNS Python: MISSING"

echo ""
echo "🎯 Quick Test Examples:"
echo ""
echo "1. Test Sherlock:"
echo "   sherlock testuser"
echo ""
echo "2. Test theHarvester:"
echo "   cd /opt/data/osint/theHarvester && python3 theHarvester.py -d example.com -b google"
echo ""
echo "3. Test SpiderFoot:"
echo "   cd /opt/data/osint/spiderfoot && python3 sf.py -m sfp_dns -t example.com"
echo ""
echo "4. Test Shodan (requires API key):"
echo "   shodan init YOUR_API_KEY"
echo "   shodan search 'apache server'"
echo ""
echo "✅ All tools ready for OSINT investigation!"
