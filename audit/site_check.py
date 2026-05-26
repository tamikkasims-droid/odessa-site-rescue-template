import requests
import sys
import json

def audit_site(url):
    print(f"Auditing {url}...\n")
    api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy=mobile"
    try:
        response = requests.get(api_url, timeout=60)
        data = response.json()
        score = data['lighthouseResult']['categories']['performance']['score'] * 100
        lcp = data['lighthouseResult']['audits']['largest-contentful-paint']['displayValue']
        fcp = data['lighthouseResult']['audits']['first-contentful-paint']['displayValue']
        print(f"=== MOBILE AUDIT RESULTS ===")
        print(f"Performance Score: {int(score)}/100")
        print(f"Load Time (LCP): {lcp}")
        print(f"First Paint: {fcp}")
        print(f"Status: {'CRITICAL - Losing customers' if score < 50 else 'NEEDS WORK' if score < 90 else 'GOOD'}")
        if score < 90:
            print(f"\nDIAGNOSIS: Google recommends <2.5s. You're likely losing 50%+ of mobile visitors.")
            print(f"REVENUE IMPACT: If 100 people visit/month, ~50 leave before booking.")
            print(f"FIX: Rebuild with Next.js typically hits 90+ score.")
        filename = url.replace("https://", "").replace("http://", "").replace("/", "_")
        with open(f'audit/{filename}_report.json', 'w') as f:
            json.dump(data['lighthouseResult']['audits'], f, indent=2)
        print(f"\nFull report saved to audit/{filename}_report.json")
    except Exception as e:
        print(f"Error: {e}")
        print("Tip: Some sites block PageSpeed. Try desktop or check manually.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        audit_site(sys.argv[1])
    else:
        print("Usage: python audit/site_check.py https://stggllc.com")
